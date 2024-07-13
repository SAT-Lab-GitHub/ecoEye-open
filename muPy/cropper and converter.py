#this converts to grayscale and/or crops (based on user-given coordinates) images present on the board and exports them
#if none of the options are chosen, images will be re-saved by the openMV board as JPEGs (useful for externally-obtained images that are to be used for training models)

#import libraries
import sensor, image, time, os, pyb, machine, sys

######### USER-DEFINED SETTINGS
#whether to crop (True) or not (False)
crop=True
#indicate x,y,w,h (x,y,width,height) rectangle tuple to crop images from that region-of-interest (ROI)
roi_rect=(0,0,1500,1000)
#whether to convert to grayscale
convert_gray=False
# turn photo (clockwise) by 90 degrees or not
angle_rotation_90=False
#JPEG quality (0-100)
jpeg_quality=95
######### END of USER-DEFINED SETTINGS

#create directory
if not "export" in os.listdir():
    os.mkdir("export")
    print("Created export directory")

#scan jpegs on card
files=os.listdir()
jpegs=[files for files in files if "jpg" in files]

#open each jpeg
for jpeg in jpegs:
    print("Loading:",jpeg,"...")
    pic_id = jpeg.split('.')[0]
    img=image.Image(jpeg,copy_to_fb=True)

    #we need to crop while converting to uncompressed image because:
    #1)image.crop function does not re-encode the image so it does not work with jpeg
    #2)img.save does not seem to export ROI even if given
    if convert_gray:
        print("Converting to grayscale...")
        if crop:
            print("Cropping ROI:",roi_rect)
            img.to_grayscale(roi=roi_rect)
        else:
            img.to_grayscale()
    else:
        print("Converting to RGB565...")
        if crop:
            print("Cropping ROI:",roi_rect)
            img.to_rgb565(roi=roi_rect)
        else:
            img.to_rgb565()

    #rotate if required
    if angle_rotation_90:
        print("Rotating...")
        img.replace(vflip=True, hmirror=False, transpose=True)

    #saving picture
    if crop:
        img.save("export/"+pic_id+"_"+str(roi_rect[0])+"_"+str(roi_rect[1])+"_"+str(roi_rect[2])+"_"+str(roi_rect[3])+"_crop.jpg",quality=jpeg_quality)
    else:
        img.save("export/"+pic_id+"_converted.jpg",quality=jpeg_quality)
    print(img)
