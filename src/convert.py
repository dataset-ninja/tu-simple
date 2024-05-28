import os, ast, glob
import shutil

import supervisely as sly
from supervisely.io.fs import (
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s
from dataset_tools.convert import unpack_if_archive


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # Possible structure for bbox case. Feel free to modify as you needs.

    train_images_path = "/home/alex/DATASETS/IMAGES/TuSimple/TUSimple/train_set/clips"
    test_images_path = "/home/alex/DATASETS/IMAGES/TuSimple/TUSimple/test_set/clips"
    test_ann_path = "/home/alex/DATASETS/IMAGES/TuSimple/test_label_new.json"
    train_ann_pathes = [
        "/home/alex/DATASETS/IMAGES/TuSimple/TUSimple/train_set/label_data_0313.json",
        "/home/alex/DATASETS/IMAGES/TuSimple/TUSimple/train_set/label_data_0531.json",
        "/home/alex/DATASETS/IMAGES/TuSimple/TUSimple/train_set/label_data_0601.json",
    ]
    batch_size = 30
    group_tag_name = "im_id"

    ds_name_to_data = {
        "train": (train_images_path, train_ann_pathes),
        "test": (test_images_path, [test_ann_path]),
    }


    def create_ann(image_name):
        labels = []
        tags = []

        im_id_value = image_name.split("_")[0] + "_" + image_name.split("_")[1]
        group_tag = sly.Tag(group_tag_meta, value=im_id_value)
        tags.append(group_tag)

        seq_value = image_name.split("_")[0]
        subfolder = sly.Tag(seq_meta, value=seq_value)
        tags.append(subfolder)

        # image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = 720  # image_np.shape[0]
        img_wight = 1280  # image_np.shape[1]

        curr_ann = im_name_to_anns.get(image_name)
        if curr_ann is not None:
            y_coords = curr_ann["h_samples"]
            for x_coord in curr_ann["lanes"]:
                exterior = []
                for y, x in zip(y_coords, x_coord):
                    if x < 0:
                        continue
                    exterior.append([y, x])
                if len(exterior) > 1:
                    polyline = sly.Polyline(exterior)
                    label_poly = sly.Label(polyline, obj_class)
                    labels.append(label_poly)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)


    obj_class = sly.ObjClass("lane", sly.Polyline)

    seq_meta = sly.TagMeta(
        "sequence",
        sly.TagValueType.ONEOF_STRING,
        possible_values=["0313-1", "0313-2", "0530", "0531", "0601"],
    )

    group_tag_meta = sly.TagMeta(group_tag_name, sly.TagValueType.ANY_STRING)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[obj_class],
        tag_metas=[group_tag_meta, seq_meta],
    )
    api.project.update_meta(project.id, meta.to_json())
    api.project.images_grouping(id=project.id, enable=True, tag_name=group_tag_name)

    for ds_name, ds_data in ds_name_to_data.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        images_path, ann_pathes = ds_data

        im_name_to_anns = {}

        for ann_path in ann_pathes:
            with open(ann_path) as f:
                content = f.read().split("\n")
                for line in content:
                    if len(line) == 0:
                        continue
                    ann = ast.literal_eval(line)
                    curr_im_name = ann["raw_file"]
                    full_im_name = (
                        curr_im_name.split("/")[-3]
                        + "_"
                        + curr_im_name.split("/")[-2]
                        + "_"
                        + get_file_name(curr_im_name)
                    )
                    im_name_to_anns[full_im_name] = ann

        images_pathes = glob.glob(images_path + "/*/*/*.jpg")

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

        for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
            img_names_batch = [
                im_path.split("/")[-3]
                + "_"
                + im_path.split("/")[-2]
                + "_"
                + get_file_name_with_ext(im_path)
                for im_path in img_pathes_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(get_file_name(image_name)) for image_name in img_names_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(img_names_batch))
    return project
