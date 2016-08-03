from PIL import Image
from PIL import ImageGrab
import PIL
import numpy as np

# Convert Image to array
img = PIL.Image.open("DrivingData2/0.png")
arr = np.array(img)
print(arr)
print(len(arr)," ",type(arr))
print(len(arr[0])," ",type(arr[0]))
print(len(arr[0][0])," ",type(arr[0][0]))

img = PIL.Image.fromarray(arr)



'''

#im=ImageGrab.grab(bbox=(255,147,355,247))
x = 8
y = 53
w = 614
h = 462

im=ImageGrab.grab(bbox=(x,y,w+x,h+y))
im.show()

center_x = (w+x)/2
center_y = (h+y)/2



im1=ImageGrab.grab(bbox=(center_x-100,center_y-100,center_x+100,center_y+100))
im2 = im1.resize((50,50))
 
im2.show()


im3=ImageGrab.grab(bbox=(center_x-200,center_y-200,center_x+200,center_y+200))
  
im4 = im3.resize((50,50))


#305, 197

'''
#text_file = open("DrivingData\\car_traning_data_1.txt", "w")
#text_file.write("dafadf")
#text_file.close()