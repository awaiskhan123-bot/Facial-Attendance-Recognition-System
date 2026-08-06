# import cv2
# import face_recognition
# import os
# import cv2
# from dotenv import load_dotenv
# from supabase import create_client
#
# # Load environment variables
# load_dotenv("secrete.env")
#
# url = os.getenv("SUPABASE_URL")
# key = os.getenv("SUPABASE_KEY")
#
# # Connect to Supabase
# supabase = create_client(url, key)
#
# # Importing student images
# folderPath = 'Images'
#
# pathList = os.listdir(folderPath)
# print(pathList)
#
# imgList = []
# studentIds = []
#
# for path in pathList:
#
#     # Read image
#     imgList.append(cv2.imread(os.path.join(folderPath, path)))
#
#     # Get student ID from image name
#     studentIds.append(os.path.splitext(path)[0])
#
#     # File path
#     fileName = f'{folderPath}/{path}'
#
#     # Upload image to Supabase Storage Bucket: Attendace
#     with open(fileName, "rb") as f:
#         supabase.storage.from_("Attendace").upload(
#             path=fileName,
#             file=f,
#             file_options={
#                 "content-type": "image/png",
#                 "upsert": "true"
#             }
#         )
#
#     print(f"Uploaded: {fileName}")
#
# print(studentIds)
# import pickle
#
#
#
#
#
#
#
#
# #
# # # Importing student images
# # folderPath = 'Resources/Modes'
# # PathList = os.listdir(folderPath)
# # print(PathList)
# #
# # imgList = []
# # studentIds = []
# #
# # for path in PathList:
# #     img = cv2.imread(os.path.join(folderPath, path))
# #
# #     if img is None:
# #         print(f"⚠️ Could not read image: {path}")
# #         continue
# #
# #     imgList.append(img)
# #
# #     print(path)
# #     studentId = os.path.splitext(path)[0]
# #     studentIds.append(studentId)
# #
# #     print(studentIds)
# #
#
# def findEncodings(imagesList):
#     encodeList = []
#
#     for img in imagesList:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#
#         encodings = face_recognition.face_encodings(img)
#
#         if len(encodings) > 0:
#             encodeList.append(encodings[0])
#         else:
#             print("⚠️ Face not detected in one image, skipping")
#
#     return encodeList
#
#
# print("Encoding Started ...")
#
# encodeListKnown = findEncodings(imgList)
#
# encodeListKnownWithIds = [encodeListKnown, studentIds]
#
# print("Encoding Complete")
#
# file = open("EncodeFile.p", 'wb')
# pickle.dump(encodeListKnownWithIds, file)
# file.close()
#
# print("File Saved")





import cv2
import face_recognition
import pickle
import os
from dotenv import load_dotenv
from supabase import create_client

# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================
load_dotenv("secrete.env")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# =========================
# CONNECT TO SUPABASE
# =========================
supabase = create_client(url, key)

# =========================
# IMPORT STUDENT IMAGES
# =========================
folderPath = 'Images'

pathList = os.listdir(folderPath)

print(pathList)

imgList = []
studentIds = []

for path in pathList:

    img = cv2.imread(
        os.path.join(folderPath, path)
    )

    if img is None:
        print(f"Image not found: {path}")
        continue

    imgList.append(img)

    studentIds.append(
        os.path.splitext(path)[0]
    )

    fileName = f'{folderPath}/{path}'

    # =========================
    # UPLOAD IMAGE TO SUPABASE
    # =========================
    try:

        with open(fileName, "rb") as f:

            supabase.storage.from_("Attendace").upload(
                path=fileName,
                file=f,
                file_options={
                    "content-type": "image/png",
                    "upsert": "true"
                }
            )

        print(f"Uploaded: {fileName}")

    except Exception as e:

        print(f"Upload Error: {e}")

print(studentIds)

# =========================
# FIND ENCODINGS
# =========================
def findEncodings(imagesList):

    encodeList = []

    for img in imagesList:

        img = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2RGB
        )

        encodings = face_recognition.face_encodings(img)

        if len(encodings) > 0:

            encodeList.append(
                encodings[0]
            )

        else:

            print(
                "Face not detected in one image, skipping"
            )

    return encodeList

# =========================
# ENCODING START
# =========================
print("Encoding Started ...")

encodeListKnown = findEncodings(imgList)

encodeListKnownWithIds = [
    encodeListKnown,
    studentIds
]

print("Encoding Complete")

# =========================
# SAVE ENCODE FILE
# =========================
with open("EncodeFile.p", 'wb') as file:

    pickle.dump(
        encodeListKnownWithIds,
        file
    )

print("File Saved")
