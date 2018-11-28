import xlsxwriter
import cv2
from cv2 import __version__
import time
import datetime
import serial
import json
from dropbox.client import DropboxOAuth2FlowNoRedirect
from dropbox.client import DropboxClient
import sys
import os
import numpy as np
import imutils


def authentification():
    global client
    conf = json.load(open('conf.json'))
    client = None

    if conf["use_dropbox"]:
        # connect to dropbox and start the session authorization process
        flow = DropboxOAuth2FlowNoRedirect(conf["dropbox_key"], conf["dropbox_secret"])
        print "[INFO] Authorize this application: {}".format(flow.start())
        authCode = raw_input("Enter auth code here: ").strip()

        # finish the authorization and grab the Dropbox client
        (accessToken, userID) = flow.finish(authCode)
        client = DropboxClient(accessToken)
        print "[SUCCESS] dropbox account linked"


def upload_file():
    global client
    # load the image
    conf = json.load(open('conf.json'))
        
    if conf["use_dropbox"]:
        # write the image to temporary file
        f = open('attendance_sheet.xlsx', 'rb')
                
        timestamp = datetime.datetime.now()
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")

        # upload the image to Dropbox and cleanup the tempory image
        print "[UPLOAD] {}".format(ts)

        client.put_file('/attendance_sheet.xlsx', f, overwrite=True)


def get_images(frame, faces_coord, shape):
    
    if shape == "rectangle":
        faces_img = op.cut_face_rectangle(frame, faces_coord)
        frame = op.draw_face_rectangle(frame, faces_coord)
    elif shape == "ellipse":
        faces_img = op.cut_face_ellipse(frame, faces_coord)
        frame = op.draw_face_ellipse(frame, faces_coord)
    faces_img = op.normalize_intensity(faces_img)
    faces_img = op.resize(faces_img)
    return (frame, faces_img)

def add_person(people_folder, shape):
    global frame
    person_name = raw_input('What is the name of the new person: ').lower()
    folder = people_folder + person_name
    if not os.path.exists(folder):
        raw_input("I will now take 20 pictures. Press ENTER when ready.")
        os.mkdir(folder)
        video = VideoCamera()
        detector = FaceDetector('haarcascade_frontalface_default.xml')
        counter = 1
        timer = 0
        cv2.namedWindow('Video Feed', cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow('Saved Face', cv2.WINDOW_NORMAL)
        while counter < 21:
            frame = video.get_frame()
            face_coord = detector.detect(frame)
            if len(face_coord):
                frame, face_img = get_images(frame, face_coord, shape)
                # save a face every second, we start from an offset '5' because
                # the first frame of the camera gets very high intensity
                # readings.
                if timer % 100 == 5:
                    cv2.imwrite(folder + '/' + str(counter) + '.jpg',
                                face_img[0])
                    print 'Images Saved:' + str(counter)
                    counter += 1
                    cv2.imshow('Saved Face', face_img[0])

            cv2.imshow('Video Feed', frame)
            cv2.waitKey(50)
            timer += 5
    else:
        print "This name already exists."
        sys.exit()

def recognize_people(people_folder, shape):
    global value
    try:
        import os
        people = [person for person in os.listdir(people_folder)]
    except:
        print "Have you added at least one person to the system?"
        sys.exit()

    print 30*'-'
    print "This are the people in the Recognition System:"
    first_db()
    for person in people:
        print "-" + person
        
    print 'Dtabase Created Successfully'

    print 30*'-'

    print 30 * '-'
    print "   POSSIBLE RECOGNIZERS TO USE"
    print 30 * '-'
    print "1. EigenFaces"
    print "2. FisherFaces"
    print "3. LBPHFaces"
    print 30 * '-'

    choice = check_choice()

    detector = FaceDetector('haarcascade_frontalface_default.xml')
    if choice == 1:
        recognizer = cv2.createEigenFaceRecognizer()
        threshold = 4000
    elif choice == 2:
        recognizer = cv2.createFisherFaceRecognizer()
        threshold = 300
    elif choice == 3:
        recognizer = cv2.createLBPHFaceRecognizer()
        threshold = 105
    images = []
    labels = []
    labels_people = {}
    for i, person in enumerate(people):
        labels_people[i] = person

    try:
        recognizer.train(images, np.array(labels))
    except:
        print "\nOpenCV Error: Do you have at least two people in the database?\n"
        sys.exit()

    video = VideoCamera()
    while True:
        global frame,c
        frame = video.get_frame()
        faces_coord = detector.detect(frame, False)
        c=1
        if len(faces_coord):
            frame, faces_img = get_images(frame, faces_coord, shape)
            for i, face_img in enumerate(faces_img):
                if __version__ == "3.1.0":
                    collector = cv2.face.MinDistancePredictCollector()
                    recognizer.predict(face_img, collector)
                    conf = collector.getDist()
                    pred = collector.getLabel()
                else:
                    pred, conf = recognizer.predict(face_img)
                print "Prediction: " + str(pred)
                print 'Confidence: ' + str(round(conf))
                print 'Threshold: ' + str(threshold)
                if conf < threshold:
                    cv2.putText(frame, labels_people[pred].capitalize(),
                                (faces_coord[i][0], faces_coord[i][1] - 2),
                                cv2.FONT_HERSHEY_PLAIN, 1.7, (206, 0, 209), 2)

                    #print labels_people[pred],'hihi'

                    update_db('P',labels_people[pred])
                    
                else:
                    cv2.putText(frame, "Unknown",
                                (faces_coord[i][0], faces_coord[i][1]),
                                cv2.FONT_HERSHEY_PLAIN, 1.7, (206, 0, 209), 2)
                    
        cv2.putText(frame, "ESC to exit- End of Attendance System", (5, frame.shape[0] - 5),cv2.FONT_HERSHEY_PLAIN, 1.2, (206, 0, 209), 2)
        
        cv2.namedWindow('Recognise', cv2.WINDOW_NORMAL)
        cv2.imshow('Recognise', frame)
        if cv2.waitKey(100) & 0xFF == 27:
            mysqltoexcel()
            upload_file()
            print 'Attendance Sheet Uploaded Successfully'
            sys.exit()

def check_choice():
    is_valid = 0
    while not is_valid:
        try:
            choice = int(raw_input('Enter your choice [1-3] : '))
            if choice in [1, 2, 3]:
                is_valid = 1
            else:
                print "'%d' is not an option.\n" % choice
        except ValueError, error:
            print "%s is not an option.\n" % str(error).split(": ")[1]
    return choice


def funtion_run():
    authentification()
    
    print 30 * '-'
    print "   POSSIBLE ACTIONS"
    print 30 * '-'
    print "1. Add person to the recognizer system"
    print "2. Start recognizer"
    print "3. Exit"
    print 30 * '-'

    CHOICE = check_choice()

    PEOPLE_FOLDER = "face_recognition_system/people/"
    SHAPE = "rectangle"

    if CHOICE == 1:
        if not os.path.exists(PEOPLE_FOLDER):
            os.makedirs(PEOPLE_FOLDER)
        add_person(PEOPLE_FOLDER, SHAPE)
    elif CHOICE == 2:
        recognize_people(PEOPLE_FOLDER, SHAPE)
    elif CHOICE == 3:
        sys.exit()
    

if __name__ == '__main__':
    funtion_run()
    
