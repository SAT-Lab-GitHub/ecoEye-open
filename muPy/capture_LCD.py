# Take pictures with openMV board connected to a battery and LCD shield- By: kdarras - 21 Feb 2022

import sensor, image, time, pyb, os, lcd

#### START of USER-defined settings ####

#enabling/disabling fully manual control of exposure (time in milliseconds) and gain (dB)
lens_aperture=2
#this must be in quotes because some are zooms
lens_focal_length_mm="12"
exposure_control=False
exposure_ms=10
gain_dB=12

#### END of user-defined settings ####

#initialize picture count
picture_count = 0

#get folder list inside jpegs folder
if not "jpegs" in os.listdir():
    os.mkdir("jpegs")
    folder_number=0
else:
    files_jpegs_folder=os.listdir("jpegs")
    folders=[files_jpegs_folder for files_jpegs_folder in files_jpegs_folder if "jpg" not in files_jpegs_folder]
    #print("folders:"+str(folders))
    if(len(folders)>0):
        folder_number=len(folders)
    else: folder_number=0

#incrementing folder number
new_folder=int(int(folder_number)+1)

#create folder
folder_created=False
while (not folder_created):
    try:
        os.mkdir("jpegs/"+str(new_folder))
        print("Created new folder: "+str(new_folder)+"...")
        folder_created=True
    except:
        #increment by 1 if folder already exists, until it doesn't
        new_folder=new_folder+1

#initialise LCD and sensor
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.WQXGA2)
sensor.set_windowing(1944,1944)
sensor.skip_frames(time = 2000)

#apply manual exposure if enabled
if(exposure_control):
    sensor.set_auto_exposure(False, exposure_us = exposure_ms*1000)
    sensor.set_auto_gain(False, gain_db = gain_dB)

clock = time.clock()

while(True):
    clock.tick()

    #get expsoure and gain values
    current_exposure_ms=round(sensor.get_exposure_us()/1000)
    current_gain_dB=round(sensor.get_gain_db())

    #set smaller sensor size to be compatible with LCD
    sensor.set_framesize(sensor.QQVGA2)
    lcd.display(sensor.snapshot().draw_string((10,140,"%sms-%sdB" % (current_exposure_ms,current_gain_dB))))
    #revert to full resolution
    sensor.set_framesize(sensor.WQXGA2)
    img = sensor.snapshot()

    #save pictures
    picture_count += 1
    img.save("jpegs/%d/%d %sms_%sdB_F%d_%smm.jpg" % (new_folder,picture_count,current_exposure_ms,current_gain_dB,lens_aperture,lens_focal_length_mm),quality=95)
    print(clock.fps(),"fps")
