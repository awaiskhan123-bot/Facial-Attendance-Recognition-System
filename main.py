import cv2
import os
import pickle
import numpy as np
import face_recognition
import cvzone
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv("secrete.env")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Connect to Supabase
supabase = create_client(url, key)

# Start webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(3, 640)
cap.set(4, 480)

# Background image path
backgroundPath = 'Resources/background.png'

# Load mode images
folderModePath = 'Resources/Modes'

modePathList = os.listdir(folderModePath)

imgModeList = []

for path in modePathList:
    imgModeList.append(
        cv2.imread(
            os.path.join(folderModePath, path)
        )
    )

print(modePathList)

# Load face encodings
print("Loading Encode File ...")

with open('EncodeFile.p', 'rb') as file:
    encodeListKnownWithIds = pickle.load(file)

encodeListKnown, studentIds = encodeListKnownWithIds

print("Encode File Loaded")

# Variables
modeType = 0
counter = 0
id = -1

studentInfo = {}
imgStudent = np.zeros((216, 216, 3), dtype=np.uint8)

# Main loop
while True:

    success, img = cap.read()

    if not success:
        print("Camera frame not received")
        continue

    # Reload background every frame
    imgBackground = cv2.imread(backgroundPath)

    # Resize webcam frame
    imgS = cv2.resize(
        img,
        (0, 0),
        fx=0.25,
        fy=0.25
    )

    # Convert BGR to RGB
    imgS = cv2.cvtColor(
        imgS,
        cv2.COLOR_BGR2RGB
    )

    # Detect faces
    faceCurFrame = face_recognition.face_locations(imgS)

    # Encode faces
    encodeCurFrame = face_recognition.face_encodings(
        imgS,
        faceCurFrame
    )

    # Put webcam frame on background
    imgBackground[
        162:162 + 480,
        55:55 + 640
    ] = img

    # Draw current mode image
    imgBackground[
        44:44 + 633,
        808:808 + 414
    ] = imgModeList[modeType]

    # Face recognition
    if faceCurFrame:

        for encodeFace, faceLoc in zip(
                encodeCurFrame,
                faceCurFrame
        ):

            # Compare faces
            matches = face_recognition.compare_faces(
                encodeListKnown,
                encodeFace
            )

            faceDis = face_recognition.face_distance(
                encodeListKnown,
                encodeFace
            )

            matchIndex = np.argmin(faceDis)

            # # If face matched
            # if matches[matchIndex]:
            #
            #     id = studentIds[matchIndex]
            #
            #     print("Known Face Detected")
            #     print(id)

            # Print confidence distance
            print(faceDis[matchIndex])

            # Strong face match only
            if matches[matchIndex] and faceDis[matchIndex] < 0.5:

                id = studentIds[matchIndex]

                print("Known Face Detected")
                print(id)

                # Face location
                y1, x2, y2, x1 = faceLoc

                y1, x2, y2, x1 = (
                    y1 * 4,
                    x2 * 4,
                    y2 * 4,
                    x1 * 4
                )

                bbox = (
                    55 + x1,
                    162 + y1,
                    x2 - x1,
                    y2 - y1
                )

                # Draw rectangle around face
                imgBackground = cvzone.cornerRect(
                    imgBackground,
                    bbox,
                    rt=0
                )

                # Load data only once
                if counter == 0:

                    cvzone.putTextRect(
                        imgBackground,
                        "Loading",
                        (275, 400)
                    )

                    cv2.imshow(
                        "Face Attendance",
                        imgBackground
                    )

                    cv2.waitKey(1)

                    counter = 1
                    modeType = 1

                    # Fetch student data
                    response = supabase.table("students") \
                        .select("*") \
                        .eq("id", str(id)) \
                        .execute()

                    if len(response.data) > 0:

                        studentInfo = response.data[0]

                        print(studentInfo)

                        # Load student image
                        imagePath = f"Images/{id}.png"

                        if os.path.exists(imagePath):

                            imgStudent = cv2.imread(imagePath)

                            imgStudent = cv2.resize(
                                imgStudent,
                                (216, 216)
                            )

                        else:

                            imgStudent = np.zeros(
                                (216, 216, 3),
                                dtype=np.uint8
                            )

                        # Check attendance timing
                        last_attendance = studentInfo.get(
                            'last_attendance_time',
                            '2023-01-01 00:00:00'
                        )

                        datetimeObject = datetime.strptime(
                            last_attendance,
                            "%Y-%m-%d %H:%M:%S"
                        )

                        secondsElapsed = (
                            datetime.now() - datetimeObject
                        ).total_seconds()

                        print(secondsElapsed)

                        # Update attendance if more than 30 seconds
                        if secondsElapsed > 30:

                            newAttendance = (
                                studentInfo['total_attendance'] + 1
                            )

                            supabase.table("students") \
                                .update({
                                    "total_attendance": newAttendance,
                                    "last_attendance_time":
                                        datetime.now().strftime(
                                            "%Y-%m-%d %H:%M:%S"
                                        )
                                }) \
                                .eq("id", str(id)) \
                                .execute()

                            studentInfo['total_attendance'] = newAttendance

                        else:

                            modeType = 3
                            counter = 0

                    else:

                        print("Student not found")

                        modeType = 3
                        counter = 0

    else:

        modeType = 0
        counter = 0

    # Show student information
    if counter != 0:

        if modeType != 3:

            # Fix overlap issue
            if counter <= 10:
                modeType = 1
            else:
                modeType = 2

            # Redraw mode image
            imgBackground[
                44:44 + 633,
                808:808 + 414
            ] = imgModeList[modeType]

            # Show student data
            if counter <= 10:

                cv2.putText(
                    imgBackground,
                    str(studentInfo['total_attendance']),
                    (861, 125),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (255, 255, 255),
                    1
                )

                cv2.putText(
                    imgBackground,
                    str(studentInfo['major']),
                    (1006, 550),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.5,
                    (255, 255, 255),
                    1
                )

                cv2.putText(
                    imgBackground,
                    str(id),
                    (1006, 493),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.5,
                    (255, 255, 255),
                    1
                )

                cv2.putText(
                    imgBackground,
                    str(studentInfo['standing']),
                    (910, 625),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.6,
                    (100, 100, 100),
                    1
                )

                cv2.putText(
                    imgBackground,
                    str(studentInfo['year']),
                    (1025, 625),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.6,
                    (100, 100, 100),
                    1
                )

                cv2.putText(
                    imgBackground,
                    str(studentInfo['starting_year']),
                    (1125, 625),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.6,
                    (100, 100, 100),
                    1
                )

                # Center student name
                (w, h), _ = cv2.getTextSize(
                    studentInfo['name'],
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    1
                )

                offset = (414 - w) // 2

                cv2.putText(
                    imgBackground,
                    str(studentInfo['name']),
                    (808 + offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (50, 50, 50),
                    1
                )

                # Show student image
                imgBackground[
                    175:175 + 216,
                    909:909 + 216
                ] = imgStudent

            counter += 1

            # Reset system
            if counter >= 20:

                counter = 0
                modeType = 0
                studentInfo = {}

                imgStudent = np.zeros(
                    (216, 216, 3),
                    dtype=np.uint8
                )

    # Show window
    cv2.imshow(
        "Face Attendance",
        imgBackground
    )

    key = cv2.waitKey(1)

    # Press any key to exit
    if key != -1:
        break

# Release camera
cap.release()

cv2.destroyAllWindows()