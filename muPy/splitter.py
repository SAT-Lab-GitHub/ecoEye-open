#this splits jpegs present on the board, optionally with overlapping window, and exports them to new jpeg files

#import libraries
import sensor, image, time, os, tf, pyb, machine, sys

######### USER-DEFINED SETTINGS
#scale(s) to split at
scales=(0.5,0.125)
overlap=True
offset=0.5
######### END of USER-DEFINED SETTINGS

#set constants
BLUE_LED_PIN = 3
GREEN_LED_PIN = 2

if not "split" in os.listdir(): os.mkdir("split")

for scale in scales:
    if not str(scale) in os.listdir("split"): os.mkdir("split/"+str(scale))

#scan jpegs on card
files=os.listdir()
jpegs=[files for files in files if "jpg" in files]

#open each jpeg
for jpeg in jpegs:
    print("######### Loading:",jpeg)
    img=image.Image(jpeg,copy_to_fb=True)

    for scale in scales:
        width_temp=int(img.width()*scale)
        height_temp=int(img.height()*scale)
        print("### Scale:",scale,", new width:",width_temp,", new height:",height_temp)
        #define x and y ranges depending on overlap
        if overlap:
            x_range = list(range(0,int(img.width()-width_temp),int(width_temp*offset)))
            y_range = list(range(0,int(img.height()-height_temp),int(height_temp*offset)))
        else:
            x_range = list(range(0,int(img.width()-width_temp),width_temp))
            y_range = list(range(0,int(img.height()-height_temp),height_temp))
        print("x range:",x_range)
        print("y range:",y_range)

        for x in x_range:
            for y in y_range:

                #try:
                    #img_s
                #except NameError:
                    #img_s_exists = False
                #else:
                    #img_s_exists = True
                #if(not img_s_exists):
                    #img_s=image.Image(width_temp,height_temp,sensor.RGB565,copy_to_fb = True)

                #re-load image TODO: needs to be more efficient but previous quoted code does not work anymore
                img=image.Image(jpeg,copy_to_fb=True)
                #extracting subset of image
                img.to_rgb565(roi=(int(x),int(y),int(width_temp),int(height_temp)))

                #saving scaled picture
                pyb.LED(BLUE_LED_PIN).on()
                img.save("split/"+str(scale)+"/x"+str(x)+"_y"+str(y)+"_w"+str(width_temp)+"_h"+str(height_temp)+"_"+jpeg)
                pyb.LED(BLUE_LED_PIN).off()
                pyb.delay(200)
