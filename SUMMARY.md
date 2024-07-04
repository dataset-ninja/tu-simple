**TuSimple: Lane Detection** is a dataset for instance segmentation, semantic segmentation, and object detection tasks. It is used in the automotive industry. 

The dataset consists of 48900 images with 9220 labeled objects belonging to 1 single class (*lane*).

Images in the TuSimple dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. There are 46462 (95% of the total) unlabeled images (i.e. without annotations). There is 1 split in the dataset: *train* (48900 images). Additionally, every image marked with its ***sequence*** and ***im_id*** tags. The dataset was released in 2020 by the <span style="font-weight: 600; color: grey; border-bottom: 1px dashed #d3d3d3;">Qualcomm YH, South Korea</span>.

<img src="https://github.com/dataset-ninja/tu-simple/raw/main/visualizations/poster.png">
