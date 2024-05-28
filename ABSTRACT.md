The **TuSimple: Lane Detection dataset** consists of 6,408 annotated road images on US highways. The resolution of the image is 1280×720. The dataset is composed of 3,626 for training and 2,782 for testing of which the annotated images are under different weather conditions. In total, the training dataset contains 72520 images, test dataset - 46470. Only each 20th frame is annotated.

## Motivation

Objects on the road can be divided into two main groups: static objects and dynamic objects. Lane markings are the main static component on the highway. They instruct the vehicles to interactively and safely drive on the highway.

## Dataset description

To encourage efforts in solving the lane detection problem on highways, the authors are releasing approximately 7,000 one-second-long video clips, each consisting of 20 frames. Lane detection is a crucial task in autonomous driving, providing essential localization information for vehicle control. The last frame of each clip includes labeled lanes, which can help algorithms produce more accurate lane detection results.

By providing these video clips, the authors aim to inspire competitors to develop more efficient algorithms. In the context of autonomous driving, an algorithm that is time and memory efficient allows more resources to be allocated to other algorithms and engineering processes. Additionally, the authors encourage competitors to consider the semantic meaning of lanes for autonomous driving, rather than merely detecting every single lane marking on the road. Consequently, the annotations and testing are focused on the current lane and the adjacent left and right lanes.

<img src="https://github.com/dataset-ninja/tu-simple/assets/120389559/3c4bfdd8-3271-4609-b26f-e177715bebe7" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">TuSimple dataset annotated example.</span>
