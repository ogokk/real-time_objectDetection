## Real-time Pepper Peduncle Detection & Segmentation
The objective of this project is to develop a software system for automated detection, segmentation, and relay trigger-based actuation module for determining pepper peduncle pose and orientation. The system is designed to accurately identify the position and alignment of the peduncle and initiate corrective actions through image-guided robotic platform. 

The system processes image captured by a stationary Basler industrial camera positioned above a conveyor belt, on which peppers are continuously transported. Utilizing the camera interfaced with the Raspberry Pi via the pypylon that is the official python wrapper for the Basler pylon camera access, real-time image acquisition is performed to detect the peduncle and determine its relative orientation. 

The acquired images are processed using image segmentation and contour analysis techniques using OpenCV library to extract geometric features indicative of the peduncle's location. To do this, morphological filter-based methods and a specialized HSV color-thresholding method optimized for darker peduncles are developed. Based on the spatial analysis of contour centroids and bounding rectangles, the system determines if the pepper's peduncle is oriented to the left or right. This directional data is used to trigger GPIO-controlled relays, actuating motors to adjust the pepper’s alignment for optimal robotic handling. Configurable parameters, such as HSV bounds and relay trigger times, are loaded from an external configuration file, enhancing the system’s adaptability to varying environmental and lighting conditions. The system logs runtime errors with timestamps to ensure maintainability and operational traceability. (The duration from image acquisition to actuation is 1.5 seconds)

This project contributes toward automating labor-intensive agricultural tasks by integrating computer vision and robotic control for real-time decision-making in smart industrial IoT (IIoT) applications.


![multi-sensor system](https://github.com/user-attachments/assets/8f9fce95-7c58-4c3b-9f88-ab64a3192059)

## Image Segmentation & Pose Detection Results


![basler_1](https://github.com/user-attachments/assets/d5e3c321-a545-43e2-a8d5-110d9e277c9a)


![basler_2](https://github.com/user-attachments/assets/df3aef58-0d3a-41c8-b9b0-d14e35ba0702)


## Demo

![peduncle_gif](https://github.com/user-attachments/assets/79d08d38-2888-4ea2-bb02-1661fc45b9e4)


## Citation

If you use this software in your research, please cite it as:

```bibtex
@software{gokkan_2021_real_time_pose,
  author       = {Ozan Gökkan},
  title        = {Real-time Pepper Peduncle Detection & Segmentation},
  year         = {2021},
  url          = {https://github.com/ogokk/real-time_objectDetection}, 
  version      = {1.0.0},
}
