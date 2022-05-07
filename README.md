# ForensicNet : Modern CNN-based Image Forgery Detection Network
# Abstract

The advancements in Image editing techniques produce realistic-looking artificial images with ease. These images can easily circumvent the forensic systems making the authentication process more tedious and difficult. To overcome this problem, we introduce a modern Convolutional Neural network named ForensicNet inspired by the recent developments in the Computer vision field such as Data augmentation, etc. The three major contributions of our CNNs are inverted bottleneck (inspired by Transformers), separate downsampling layers (inspired by ResNets), and using depthwise convolutions for mixing information in the spatial dimension (inspired by MobileNetV2). 
The inverted bottlenecks help improve the accuracy and even reduce the network parameters/FLOPs. The separate downsampling layers help converge the network. The normalization layers also help in stabilizing training whenever the spatial resolution is changed. The depthwise convolution is a grouped convolution where the number of groups and the number of channels are the same. The experiments show that ForensicNet outperforms the state-of-the-art methods by a large margin.


Accuracy and loss graphs of (a) CASIA and (b) RFF datasets are shown below: 

![AL_Graph](https://user-images.githubusercontent.com/37774749/167248461-5638b678-b48f-4cf2-a627-7f3c5866d618.jpg)



The Confusion matrix of CASIA (left) and RFF (right) datasets is shown below.

![CM](https://user-images.githubusercontent.com/37774749/167248464-d14d7b92-3304-4e9b-be7d-a9149532f32e.jpg)
