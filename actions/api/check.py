import requests 

p = {
      "studentSubmittedAssignmentFile":"None",
      "grade":"None",
      "remarks":"None",
      "assignmentGraded":"None",
      "assignmentSubmitted":"None",
      "assignment":{
         "id":"60181de9c70cd4004ddc8c08",
         "assignmentTitle":"test open assignment 1",
         "files":[
            
         ],
         "deadLine":1612280701000,
         "totalGrade":10,
         "instructions":"<p>description test&nbsp;</p>\n",
         "programId":"5edb3aab5188c800428ea2d4",
         "batchId":"5edb40415188c800428ea326"
      }
}
print(p["assignment"]["assignmentTitle"])
print(p["assignment"]["totalGrade"])


# import requests


# headers = {
# "Authorization": "p = {
#       "studentSubmittedAssignmentFile":"None",
#       "grade":"None",
#       "remarks":"None",
#       "assignmentGraded":"None",
#       "assignmentSubmitted":"None",
#       "assignment":{
#          "id":"60181de9c70cd4004ddc8c08",
#          "assignmentTitle":"test open assignment 1",
#          "files":[

#          ],
#          "deadLine":1612280701000,
#          "totalGrade":10,
#          "instructions":"<p>description test&nbsp;</p>\n",
#          "programId":"5edb3aab5188c800428ea2d4",
#          "batchId":"5edb40415188c800428ea326"
#       }
# }
# print(p["assignment"]["assignmentTitle"])
# print(p["assignment"]["totalGrade"])


# # import requests


# # headers = {
# # "Authorization": "bearer eyJraWQiOiJ0cW1iYTVRSW95TjErMXRNb3R5MG9ibktSaldNTlpGOTFhNDVcL3ZuZlh1dz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJkZDNlZmJkMC04NTUwLTQ0OTMtYTNlNC1hNTIyMjg2NWMxNDEiLCJjb2duaXRvOmdyb3VwcyI6WyJBQ0FERU1ZX1NUVURFTlQiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLXdlc3QtMi5hbWF6b25hd3MuY29tXC91cy13ZXN0LTJfc3RrRzlhckc0IiwidmVyc2lvbiI6MiwiY2xpZW50X2lkIjoiNGhidDNvNW5mdHFrcjAxN2p1ajlsdm5nNnIiLCJldmVudF9pZCI6Ijg3MzZlMjYxLWNlZWItNDVlZS1iYjY2LWZlZTg0MjNlN2ZmYyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE2MTMxMTY0OTIsImV4cCI6MTYxMzM4Mzc2OCwiaWF0IjoxNjEzMzgwMTY5LCJqdGkiOiI5MzM5YTY5Zi05ZjY4LTQxNDctYTYzNS0zN2U0OTc4NzljMDIiLCJ1c2VybmFtZSI6ImRkM2VmYmQwLTg1NTAtNDQ5My1hM2U0LWE1MjIyODY1YzE0MSJ9.LrzIXXZCSFUl1Xo1J0Z9J1bvhwCd_HRtZ4vKHvXX8m4HqNsAtadgLkeWEenUOMBWvZoNvkQAs2s32JqtIUe4DBNSVFTh5h4piho3QlnwTKQxqjprHfGOVXsQLzzpKe6HcfMdKdnT9pE_xVLXb6iYija515Xou03owJAr2GFgjs853ZXHwtbLF2JHKaZPGuCO3efRn7VWT7Wilb7PAdeH9tIktkyqvzvp2ewV1cEleIcCs5hVuIRjf9yZuwfrMyH9ASrebsGho22sZUzoKVjYISL6xcNjgTYa5e-RTRyh6lQYHO-Aw48V9GJFBzz-IiJjgvoNG2VCrp-gUJg8V1Us0g",
# # "Origin": "https://thames-stage.fuseclassroom.com",
# # "idToken": "eyJraWQiOiIycWxrSjRleFl1eHNKRWJFUElBaHh2dnMxZ1pvY2Fpa2RaQ1JXbU5UbWtnPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoibERyRFRfOHk5UWNwN0ZaeGxmcXJidyIsInN1YiI6ImRkM2VmYmQwLTg1NTAtNDQ5My1hM2U0LWE1MjIyODY1YzE0MSIsImNvZ25pdG86Z3JvdXBzIjpbIkFDQURFTVlfU1RVREVOVCJdLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLXdlc3QtMi5hbWF6b25hd3MuY29tXC91cy13ZXN0LTJfc3RrRzlhckc0IiwiY29nbml0bzp1c2VybmFtZSI6ImRkM2VmYmQwLTg1NTAtNDQ5My1hM2U0LWE1MjIyODY1YzE0MSIsImF1ZCI6IjRoYnQzbzVuZnRxa3IwMTdqdWo5bHZuZzZyIiwiZXZlbnRfaWQiOiI4NzM2ZTI2MS1jZWViLTQ1ZWUtYmI2Ni1mZWU4NDIzZTdmZmMiLCJ0b2tlbl91c2UiOiJpZCIsInNjaG9vbElkIjoiNWViZTI1ZDE1MjZhODMwMDQyZWEyNzk1IiwiYXV0aF90aW1lIjoxNjEzMTE2NDkyLCJleHAiOjE2MTMzODM3NjgsImlhdCI6MTYxMzM4MDE2OCwiZW1haWwiOiJuaXJhamFuaHVtYWdhaW4uc0B5b3BtYWlsLmNvbSJ9.dX6sNxOm5IVYLmbGTpBe3zZFueZlLUv4iXsedDkUnBkP5L7Vr2VrZqk1syQqh15zEZzngJkCah9Zr0plf8d3piztdHscJ1IsxulEjw434rWGMU5VveRGDuzhHtWxOWEHzM6IhNZtky6DMObHFuC5MRLG_1-2S96Jq6AKqNgPmLIB3G2agSG6326AEOV-OKucoGAA7jdmIr3T4kCJynxB_-E_a0K83l0SaB_kuYTIH2Ake3h1YMbmsPRogiypHgbuRfxOhTsH_bd9AAe4jZs0HnYShgWHMuPmOLekwyHROhBF9Tbx3cbDjVGD4Eo03fM9lzA60tWO36BoUgulVf7h_w"
# # }

# # rest_url = "https://app-api-stage.fuseclassroom.com"
# # schoolId = "5ec38621540c47004217fefd"

# # def object_list(object_type):
# #       url = "/api/v2/enrolledCourses"
# #       results = requests.get(rest_url + url, headers=headers)
# #       object_list = []

#   GNU nano 2.5.3                            File: check.py

# p = {
#       "studentSubmittedAssignmentFile":"None",
#       "grade":"None",
#       "remarks":"None",
#       "assignmentGraded":"None",
#       "assignmentSubmitted":"None",
#       "assignment":{
#          "id":"60181de9c70cd4004ddc8c08",
#          "assignmentTitle":"test open assignment 1",
#          "files":[

#          ],
#          "deadLine":1612280701000,
#          "totalGrade":10,
#          "instructions":"<p>description test&nbsp;</p>\n",
#          "programId":"5edb3aab5188c800428ea2d4",
#          "batchId":"5edb40415188c800428ea326"
#       }
# }
print(p["assignment"]["assignmentTitle"])
print(p["assignment"]["totalGrade"])


# import requests",
header={
"Authorization": "bearer eyJraWQiOiJUVU1cL0I2N0xyWEtwekNFQVZrdlRsY085emlYb2JBK29sU2lKOEVZdUpjUT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzOTEwOTRmMC1mM2I5LTQ4ZTItYWFiMy0xOWFiNTg0OTY5MTYiLCJjb2duaXRvOmdyb3VwcyI6WyJBQ0FERU1ZX1NUVURFTlQiXSwiZXZlbnRfaWQiOiJkZDJlMTlkMi1lMGJkLTQ4NGUtYmU4MC1mZTg5Yzk5MTE1ZDQiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIiwiYXV0aF90aW1lIjoxNjI1NzM2MzcxLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtd2VzdC0yLmFtYXpvbmF3cy5jb21cL3VzLXdlc3QtMl9OZzlHTEFHOVkiLCJleHAiOjE2MjU3NDM2MTgsImlhdCI6MTYyNTc0MDAxOCwianRpIjoiYWFjMTVmNDItNzU2OC00ZDE2LTk2OTEtYzEzZTlmZDFhMjc1IiwiY2xpZW50X2lkIjoiNGpvY3Vxam9nbXNsNDZkczcyNGdhZXUzbjQiLCJ1c2VybmFtZSI6IjM5MTA5NGYwLWYzYjktNDhlMi1hYWIzLTE5YWI1ODQ5NjkxNiJ9.d0uiDtY14OgFRHri7wijjNPw7J5DoUJlxxrPotaTCEodzLp3VeGJzglTF3YdYOcPuLTZH4Y-_Q47ZbC2kMYr974sTwa1rxVHX2YlBC09Z7H-7V17QBu3a2ZRTWvZNSpM8zzrh-uhcIxWsxXrsU46-7LsXu4UPyiYr5KL-8CxiLdbS66ORoE3HDpVSylwkDX5A41zvxbvpChwKzs90MI1xDkr_y176-2l9D-mPh7-hFRIcnARUqIRe42datgDX9PVrVm4xGeztCEES-23qVx0Ct5pcJ51OZl9s-If5SA_snZ4MHkofrFKhE0tr_okc9itPAObClFm4EvPNm5SPqA66Q",
"Origin": "https://thames-dev.fuseclassroom.com",
"idToken": "eyJraWQiOiJDTlc5WDIxVTFaVG5HSjNHTnBnV2dtYXpUYTZcL0xVNDlldHpEY3Z3bm9rQT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzOTEwOTRmMC1mM2I5LTQ4ZTItYWFiMy0xOWFiNTg0OTY5MTYiLCJjdXN0b206c2Nob29sSWQiOiI1ZWMyNGFkMzEwMzkxYTAwNDJjM2Y1ZjIiLCJjb2duaXRvOmdyb3VwcyI6WyJBQ0FERU1ZX1NUVURFTlQiXSwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy13ZXN0LTIuYW1hem9uYXdzLmNvbVwvdXMtd2VzdC0yX05nOUdMQUc5WSIsImNvZ25pdG86dXNlcm5hbWUiOiIzOTEwOTRmMC1mM2I5LTQ4ZTItYWFiMy0xOWFiNTg0OTY5MTYiLCJhdWQiOiI0am9jdXFqb2dtc2w0NmRzNzI0Z2FldTNuNCIsImV2ZW50X2lkIjoiZGQyZTE5ZDItZTBiZC00ODRlLWJlODAtZmU4OWM5OTExNWQ0IiwidG9rZW5fdXNlIjoiaWQiLCJzY2hvb2xJZCI6IjVlYzI0YWQzMTAzOTFhMDA0MmMzZjVmMiIsImF1dGhfdGltZSI6MTYyNTczNjM3MSwiZXhwIjoxNjI1NzQzNjE4LCJpYXQiOjE2MjU3NDAwMTgsImVtYWlsIjoia2Ftb2RkaGFtbGEuc0B5b3BtYWlsLmNvbSJ9.QwTUufCZI6E--2y3MENjvdZBq0-BpR7tJpjAqrlUzTvFxF27zySzPUOzbVE_4bz_CLArLnRqNwtvHmVsQRnRECxXYBHHD5jzfDoF5hxYPmcd9urjKPYuRyEFpzOPos6SKLTUvYaN3sO1Iws8z7gbIOCN2VYsqN3uubJp8k8za_2gYdEjLXsmAuhXwIiFMlv0-mL6poZgn4RzoyGJRxZIZgHUs8JqYOycXPdpaiP6qwCi50QMwz3Wf85N7KL0n-HWxkekILeuSHj6tWBpDmuNtdyQ4YMCwwQlBZRft95WZXro_lTcbyZfUPBoR8CRP84OvZfGDJja21CLy7zW8yDklw"
}

# headers = {
#       "Authorization":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNWVjMjZjNzVkZGU0MjEwMDQyMjExMjU5In0.rrj83oxtsZSkioT7rUAgQaWBPT2alU4DXUCls50l4vs",
#       "Origin": "https://thames-dev.fuseclassroom.com"

# }
# rest_url = "https://app-api-stage.fuseclassroom.com"
# schoolId = "5ec24ad310391a0042c3f5f2"

# def object_list(object_type):
#       url = "/api/v2/enrolledCourses"
#       results = requests.get(rest_url + url, headers=headers)
#       print(results)
#       object_list = []
#       for p in results.json():
#           if object_type == "courseBy":
#               object_list.append(p[object_type][0])
#           else:
#               object_list.append(p[object_type])
#       return object_list

# courseId = set(object_list("courseId"))
# batchId = set(object_list("batchId"))
# params = {
#                 "filterBy": "notSubmitted",
#                 "page": 1,
#                 "size": 10,
#                 "courseId": ",".join(courseId),
#                 "batchId": ",".join(batchId),
#                 "filterByGradeType":""

#             }
# full_url = rest_url + "/api/v2/assignments/student/papers?"
full_url = "https://app-api-dev.fuseclassroom.com/api/v2/assignments/students/papers?filterBy=overdue&page=1&size=10&courseId=6061ca241fb45a0093582eb1&courseId=605499e0ea2cab0094ef08c8&courseId=5ec25fd310391a0042c3f62f&courseId=608fa50a676c0d009619ebf5&courseId=60dc33ae19b0eb780b76946f&courseId=5ec25fd410391a0042c3f633&courseId=5ec25fd410391a0042c3f643&courseId=60dc317019b0eb780b769440&courseId=5ec25fd410391a0042c3f64b&courseId=5ec25fd410391a0042c3f647&courseId=6087c175d12e46009959b70f&courseId=5ed60a592a60830042cff0d4&batchId=6087c02cd12e46009959b6f8&batchId=5fa39102b94995004284de10&batchId=60dc309719b0eb780b769416&batchId=5ed6078c2a60830042cff0c8&batchId=5ec25b0f10391a0042c3f61f&batchId=60dc309719b0eb780b769414&batchId=605492f9ea2cab0094eed3af&filterByGradeType=&keyword=&assignmentType=PAPER"
# response = requests.get(full_url, params=params, headers=header)
# full_url = "https://app-api-dev.fuseclassroom.com/api/v2/assignments/students/papers?filterBy=submitted&page=1&size=10&courseId=5ec25fd310391a0042c3f62f,5ec25fd410391a0042c3f633,5ec25fd410391a0042c3f643,5ec25fd410391a0042c3f647,5ec25fd410391a0042c3f64b,5ed60a592a60830042cff0d4,605499e0ea2cab0094ef08c8,6061ca241fb45a0093582eb1,6087c175d12e46009959b70f,608fa50a676c0d009619ebf5,60dc317019b0eb780b769440,60dc33ae19b0eb780b76946f&batchId=5ec25b0f10391a0042c3f61f,5ed6078c2a60830042cff0c8,605492f9ea2cab0094eed3af,6087c02cd12e46009959b6f8,5fa39102b94995004284de10,60dc309719b0eb780b769414,60dc309719b0eb780b769416&filterByGradeType="
response = requests.get(full_url, headers=header)
print(full_url)
print(response.json())
# # print(courseId)
# # print(batchId)