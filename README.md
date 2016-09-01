# Python Neural Network

## Real world lane deteciton
![](https://github.com/InderPabla/PythonNeuralNetwork/blob/master/Images/15.gif)
![](https://github.com/InderPabla/PythonNeuralNetwork/blob/master/Images/16.gif)
- Image size 100x56
- Neural network output are 4 numbers.
- Each number represents x values on a preset y axis. Each pair of numbers make 1 line.
- RED line is prediction by network, GREEN line is give traning data.


## Basic Self Driving Car 
- Basic concept of self driving car using Convolutional Neural Networks 
- CNN was trained using 500, 50x50 pixel images. 
- Each image was followed by a output of 2 neurons representing left and right turn 

### GIF of self driving car
![](https://github.com/InderPabla/PythonNeuralNetwork/blob/master/Images/3.gif)

### GIF of self driving car as seen through view of Convolution Layer 6 - Local receptive field 0
![](https://github.com/InderPabla/PythonNeuralNetwork/blob/master/Images/2.gif)
- It can be seen that by the 6th layer, the network has learnt to respond with high activation on edges , curves, and the car

### GIF of self driving car as seen through view of Convolution Layer 2 - Local receptive field 3
![](https://github.com/InderPabla/PythonNeuralNetwork/blob/master/Images/4.gif)

## Advanced Self Driving Car 
- Convolutional neural network takes additional inputs of steering angle, current velocity and turn speed 
- Car must also learn to avoid obstacles as it drives on the track

### GIF of self driving car with obsticals 
![](https://github.com/InderPabla/PythonNeuralNetwork/blob/master/Images/7.gif)

### GIF of self driving car as seen through view of Convolution Layer 4 - Local receptive field 4
![](https://github.com/InderPabla/PythonNeuralNetwork/blob/master/Images/8.gif)
- Layer has the highest activation when detecting obsticals infront of the car 
- This shows, by the 4th layers, neural network can identify a safe path to take if presented with obstacles 

### GIF of self driving car as seen through view of Convolution Layer 6 - Local receptive field 3
![](https://github.com/InderPabla/PythonNeuralNetwork/blob/master/Images/6.gif)

### Good quality GIF of car in action
![](https://github.com/InderPabla/PythonNeuralNetwork/blob/master/Images/5.gif)

## Self driving car learns to drive on one lane
![](https://github.com/InderPabla/PythonNeuralNetwork/blob/master/Images/10.gif)
![](https://github.com/InderPabla/PythonNeuralNetwork/blob/master/Images/9.gif)
- Neural network is only taught to stay in the right lane, and cannot drive on the left lane

## Self driving car learns to drive on both left and right
- Neural network is taught to stay exclusively in left or right lane when driving

### Right lane
![](https://github.com/InderPabla/PythonNeuralNetwork/blob/master/Images/11.gif)
![](https://github.com/InderPabla/PythonNeuralNetwork/blob/master/Images/12.gif)

### Left lane
![](https://github.com/InderPabla/PythonNeuralNetwork/blob/master/Images/13.gif)
![](https://github.com/InderPabla/PythonNeuralNetwork/blob/master/Images/14.gif)

## Video Demo Of Neural Network Trained To Recognize Numbers:
[![ScreenShot](https://github.com/InderPabla/PythonNeuralNetwork/blob/master/Images/1.PNG)](http://youtu.be/yt6k5CD7e6M)


