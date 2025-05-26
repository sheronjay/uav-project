'''import cv2
import cv2.aruco as aruco

cap = cv2.VideoCapture(0)
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
        print("Detected Marker IDs:", ids)

    cv2.imshow('Landing Pad Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()'''
import cv2
import numpy as np
from picamera2 import Picamera2
import time

#Initializing camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
picam2.start()
time.sleep(2) #let the cam warm up

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict,aruco_params)

def detect_markers(frame):
    #convert to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) 

    #detect marker
    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None and len(ids) > 0:
        #draw the marker
        cv2.aruco.drawDetectedMarkers(frame, corners, ids) #boundries

        marker_id = ids[0][0]
        marker_corners = corners[0][0]

        #center of the marker
        center_x = int(np.mean(marker_corners[:, 0]))
        center_y = int(np.mean(marker_corners[:, 1]))

        #draw center
        cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

        #marker id tag
        cv2.putText(frame, f"ID: {marker_id}", 
                    (center_x - 20, center_y - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        print(f"Marker ID: {marker_id}, Center: ({center_x}, {center_y})")

    else:
        print("No markers detected")

    return corners, ids, frame

def run_aruco_detector():
    try:
        while True:
            # Capture frame from camera
            frame = picam2.capture_array()

            # Detect markers in current frame
            corners, ids, processed_frame = detect_markers(frame)

            # Display the frame
            cv2.imshow("UAV Project: ArUco Marker Detection", processed_frame)

            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("Detection interrupted by user")
    finally:
        # Cleanup
        picam2.stop()
        cv2.destroyAllWindows()
        print("Camera stopped and windows closed")

if __name__ == "__main__":
    run_aruco_detector()