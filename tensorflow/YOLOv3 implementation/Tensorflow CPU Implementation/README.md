# Tensorflow CPU Implementation on CPU
A realtime YOLO3 object detection of webcam stream in python3.

This YOLO3 implementation is a fork from developer heartkilla.
I have done some minor changes.
Find original code here:

https://github.com/heartkilla/yolo-v3

Checkout his awesome tutorial here:

https://www.kaggle.com/aruchomu/yolo-v3-object-detection-in-tensorflow

## Getting started
Follow these instructions to run this implementation!

1. Install needed Python3 packages from requirements.txt by running:

```
pip install -r requirements.txt
```

2. Download pretrained weigthts on COCO dataset for darknet implementation.

Link : https://pjreddie.com/media/files/yolov3.weights

3. Transform downloaded weights to tensorflow format by running `transform_weights.py` in same folder as `yolov3.weights`

4. Run program by running `main.py`, be sure to check path to model!

## Acknowledgments
* [Yolo v3 official paper](https://arxiv.org/abs/1804.02767)
* [A Tensorflow Slim implementation](https://github.com/mystic123/tensorflow-yolo-v3)
* [ResNet official implementation](https://github.com/tensorflow/models/tree/master/official/resnet)
* [DeviceHive video analysis repo](https://github.com/devicehive/devicehive-video-analysis)
* [A Street Walk in Shinjuku, Tokyo, Japan](https://www.youtube.com/watch?v=kZ7caIK4RXI)
