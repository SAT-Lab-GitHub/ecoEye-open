#this crops and exports images present on the board based on user-given coordinates

#import libraries
import sensor, image, time, os, pyb, machine, sys

#START of user-defined settings
#delay between consecutively loaded pictures, in milliseconds
delay_ms=0
#END of user-defined settings

#scan jpegs on card
files=os.listdir()
jpegs=[files for files in files if "jpg" in files]

#open each jpeg and display in preview pane
for jpeg in jpegs:
    print("Loading:",jpeg)
    img=image.Image(jpeg,copy_to_fb=True)
    if delay_ms>0: print("You have",delay_ms,"seconds to measure your histogram.")
    pyb.delay(delay_ms)

