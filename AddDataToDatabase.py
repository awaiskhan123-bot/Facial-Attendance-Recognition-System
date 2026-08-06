#
# from dotenv import load_dotenv
# from supabase import create_client
# import os
#
# load_dotenv("secrete.env")
#
# url = os.getenv("SUPABASE_URL")
# key = os.getenv("SUPABASE_KEY")
#
# supabase = create_client(url, key)
#
# data = [
#     {
#         "id": 234532,
#         "name": "Awais Afridi",
#         "major": "Machine Learning",
#         "starting_year": 2023,
#         "total_attendance":8,
#         "standing": "G",
#         "year": 4,
#         "last_attendance_time": "2023-12-11 00:54:34"
#     },
#     {
#         "id": 321645,
#         "name": "Saifullah",
#         "major": "Website Dev",
#         "starting_year": 2022,
#         "total_attendance": 12,
#         "standing": "B",
#         "year": 1,
#         "last_attendance_time": "2022-10-11 00:52:34"
#     },
#     {
#         "id": 852741,
#         "name": "Uqaab Haider",
#         "major": "Game Dev",
#         "starting_year": 2024,
#         "total_attendance": 7,
#         "standing": "G",
#         "year": 2,
#         "last_attendance_time": "2024-12-11 00:54:34"
#     },
#     {
#         "id": 963852,
#         "name": "Rehan Khan",
#         "major": "Generative AI",
#         "starting_year": 2025,
#         "total_attendance": 26,
#         "standing": "G",
#         "year": 1,
#         "last_attendance_time": "2024-12-11 02:50:34"
#     }
# ]
#
# # response = supabase.table("students").insert(data).execute()
# response = supabase.table("students").upsert(data).execute()
# print(response)
# print("Connected Successfully")
from dotenv import load_dotenv
from supabase import create_client
import os

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
# STUDENT DATA
# =========================
data = [
        {
            "id": 234532,
            "name": "Awais Afridi",
            "major": "Machine Learning",
            "starting_year": 2023,
            "total_attendance":8,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2023-12-11 00:54:34"
        },
        {
            "id": 321645,
            "name": "Saifullah",
            "major": "Website Dev",
            "starting_year": 2022,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-10-11 00:52:34"
        },
        {
            "id": 852741,
            "name": "Uqaab Haider",
            "major": "Game Dev",
            "starting_year": 2024,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2024-12-11 00:54:34"
        },
        {
            "id": 963852,
            "name": "Rehan Khan",
            "major": "Generative AI",
            "starting_year": 2025,
            "total_attendance": 26,
            "standing": "G",
            "year": 1,
            "last_attendance_time": "2024-12-11 02:50:34"
        }
]

# =========================
# INSERT / UPDATE DATA
# =========================
response = supabase.table("students") \
    .upsert(data) \
    .execute()

print(response)

print("Connected Successfully")
