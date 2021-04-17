#importing neccessary packages
import os
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
import urllib.request
from playsound import playsound

class Drowsiness_detection: 
    def assure_path_exists(path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    def eye_aspect_ratio(self,eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        C = dist.euclidean(eye[0], eye[3])

        ear = (A + B) / (2.0 * C)

        return ear

    def final_ear(self,shape):
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        leftEAR = self.eye_aspect_ratio(leftEye)
        rightEAR = self.eye_aspect_ratio(rightEye)

        ear = (leftEAR + rightEAR) / 2.0
        return (ear, leftEye, rightEye)

    def lip_distance(self,shape):
        top_lip = shape[50:53]
        top_lip = np.concatenate((top_lip, shape[61:64]))

        low_lip = shape[56:59]
        low_lip = np.concatenate((low_lip, shape[65:68]))

        top_mean = np.mean(top_lip, axis=0)
        low_mean = np.mean(low_lip, axis=0)

        distance = abs(top_mean[1] - low_mean[1])
        return distance
    def __init__(self):
        # assure_path_exists("dataset/")
        EYE_AR_THRESH = 0.27
        EYE_AR_CONSEC_FRAMES = 15
        YAWN_THRESH = 30
        
        COUNTER = 0

        print("-> Loading the predictor and detector...")
        #detector = dlib.get_frontal_face_detector()
        detector = cv2.CascadeClassifier(r"haarcascade_frontalface_default.xml")    #Faster but less accurate
        predictor = dlib.shape_predictor(r"shape_predictor_68_face_landmarks.dat")
     
        print("-> Starting Video Stream")
        vs = VideoStream().start()
        #vs=VideoStream('http://192.168.1.68:8080/video').start() # IP webcam APP
        #vs= VideoStream(usePiCamera=True).start()       //For Raspberry Pi
        mailing=True
       

        while True:

            frame = vs.read()
            frame = imutils.resize(frame, width=450)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #rects = detector(gray, 0)
            rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
                minNeighbors=5, minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE)

            #for rect in rects:
            for (x, y, w, h) in rects:
                rect = dlib.rectangle(int(x), int(y), int(x + w),int(y + h))
                
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                eye = self.final_ear(shape)
                ear = eye[0]
                leftEye = eye [1]
                rightEye = eye[2]

                distance = self.lip_distance(shape)

                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

                lip = shape[48:60]
                cv2.drawContours(frame, [lip], -1, (0, 255, 0), 1)

                if ear < EYE_AR_THRESH:
                    COUNTER += 1

                    if COUNTER >= EYE_AR_CONSEC_FRAMES:
                        cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
						
						
                        
                        playsound('sound files/alarm.mp3')
                        if mailing==True:
                            cv2.imwrite("dataset/frame_sleep%d.jpg" % COUNTER, frame)
                            
                            os.system("start \"\" http://localhost/email/email/")
                           

                else:
                    COUNTER = 0

                if (distance > YAWN_THRESH):
                        cv2.putText(frame, "Yawn Alert", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        
                cv2.imwrite("dataset/frame_yawn%d.jpg" % COUNTER, frame)
                cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "YAWN: {:.2f}".format(distance), (300, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				


            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or  key == ord("Q"):
                break

        cv2.destroyAllWindows()

        vs.stop()
object_trigger=Drowsiness_detection()
