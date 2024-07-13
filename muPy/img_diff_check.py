#this crops and exports images present on the board based on user-given coordinates

#import libraries
import sensor, image, time, os, pyb, machine, sys

######### USER-DEFINED SETTINGS
#define reference imace path
ref_image="2410_reference.jpg"
######### END of USER-DEFINED SETTINGS

if not "diffs" in os.listdir():
    os.mkdir("diffs")
    print("Created directory for image differences")

#scan jpegs on card
files=os.listdir()
jpegs=[files for files in files if "jpg" in files]

#de-allocate frame buffer just in case
sensor.dealloc_extra_fb()
# Take from the main frame buffer's RAM to allocate a second frame buffer.
img_ref_fb = sensor.alloc_extra_fb(2592, 1944, sensor.RGB565)
img_ref=image.Image(ref_image,copy_to_fb=True)
#we need RGB565 to compute image diffs
img_ref.to_rgb565()
#replace frame buffer with reference image
img_ref_fb.replace(img_ref)

#open each jpeg
for jpeg in jpegs:
    print("Loading:",jpeg)
    img=image.Image(jpeg,copy_to_fb=True)
    img.to_rgb565()
    #compute absolute image difference
    img.difference(img_ref_fb)
    #save difference image
    img.save("diffs/"+jpeg+"_diff.jpg",quality=95)

