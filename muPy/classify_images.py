#import libraries
import image, os, tf, pyb, math

# USER PARAMETERS ######
#import mobilenet model and labels
net = "trained.tflite"
labels = [line.rstrip('\n') for line in open("labels.txt")]
model_type="object_detection"
#export images as JPG after classification?
export=False
#threshold confidence level above which we log detections
min_confidence=0.3
colors = [ # Add more colors if you are detecting more than 7 types of classes at once.
    (255,   0,   0),
    (  0, 255,   0),
    (255, 255,   0),
    (  0,   0, 255),
    (255,   0, 255),
    (  0, 255, 255),
    (255, 255, 255),
]

# END of USER PARAMETERS ######

detection_count=0
minimum_image_scale=1

#scan jpegs on card
files=os.listdir()
jpegs=[files for files in files if "jpg" in files]

# create detection file and "out" folder if required
if(not 'detections.csv' in os.listdir()):
        with open('detections.csv', 'a') as detectionlog:
            detectionlog.write("picture" + ',' + "detection" +  ',' + "label1" + ',' "confidence1" + ',' + "x_top_left" + ',' + "y_top_left" + ',' + "width" + ',' + "height" +  ',' + "label2" + ',' "confidence2" + '\n')
if (export and not "out" in os.listdir()): os.mkdir("out")

#open and classify each jpeg
for jpeg in jpegs:
    print("Loading:",jpeg)
    img=image.Image(jpeg,copy_to_fb=True)

    print("Converting to RGB565:",jpeg)
    img.to_rgb565()
    print("Image details:",img)

    #starting classification
    pyb.LED(2).on()
    print("LED on: classifying image", jpeg,"\n**************")

    #classify
    #try:
    #object detection
    if (model_type=="object_detection") :
        for i, detection_list in enumerate(tf.detect(net,img, thresholds=[(math.ceil(min_confidence * 255), 255)])):
            if (i == 0): continue # background class
            if (len(detection_list) == 0): continue # no detections for this class?

            print("********** %s centroids **********" % labels[i])
            for d in detection_list:
                detection_count+=1
                #draw centroids
                [x, y, w, h] = d.rect()
                center_x = math.floor(x + (w / 2))
                center_y = math.floor(y + (h / 2))
                print('x %d\ty %d' % (center_x, center_y))
                img.draw_circle((center_x, center_y, 12), color=colors[i], thickness=2)
                with open('detections.csv', 'a') as detectionlog:
                    detectionlog.write(str(jpeg) + ',' + str(detection_count) + ',' + str(labels[i]) + ',' + str(d[4]) + ',' + str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) + ',' + str(d[3]) + '\n')
    #image classification
    if (model_type=="image_classification"):
        for obj in tf.classify(net, img, min_scale=minimum_image_scale, scale_mul=0.5, x_overlap=0.5, y_overlap=0.5):
            detection_count+=1
            predictions_list = list(zip(labels, obj.output()))
            print(predictions_list)
            with open('detections.csv', 'a') as detectionlog:
                detectionlog.write(str(jpeg) + ',' + str(detection_count) + ',' + str(predictions_list[1][0]) + ',' + str(predictions_list[1][1]) + ',' + str(obj.rect()[0]) + ',' + str(obj.rect()[1]) + ',' + str(obj.rect()[2]) + ',' + str(obj.rect()[3]) + ',' + str(predictions_list[0][0]) + ',' + str(predictions_list[0][1]) + '\n')
    #except:
        #print("Error with TFLite execution")
    #turn off green LED
    pyb.LED(2).off()

    #optionally save image (for diagnostics)
    if export : img.save("out/"+jpeg+"_rgb565.jpg")
