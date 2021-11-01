import json
from typing import Any, Dict, List, Text

from rasa_sdk.events import FollowupAction
from rasa_sdk.executor import Action, CollectingDispatcher, Tracker

from actions.api.query_graph import object_list
from actions.log_config import logger

# class ActionTeacher(Action):
#     def name(self) -> Text:
#         return "list_teacher"

#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         buttons_list = []
#         logger.info("On List teacher action")

#         teacher_list = object_list("courseBy", tracker)
#         course_id_list = object_list("courseId", tracker)
#         if not teacher_list or not course_id_list:
#             dispatcher.utter_message(
#                 "Sorry, 🤔 It seems I don't have that information about your Teacher."
#             )
#             return []

#         res = zip(teacher_list, course_id_list)
#         s = {}
#         final_results = []
#         for teacher, courseid in res:  # in order to remove duplicate teacher
#             if not s.get(teacher):
#                 s[teacher] = True
#                 final_results.append((teacher, courseid))

#         for teachername, courseid in final_results:
#             payload = {
#                 "teacher_name": teachername,
#                 "course_id": courseid,
#                 "new_action": "query_teacher",
#             }
#             payload = json.dumps(payload)
#             buttons_list.append(
#                 {"title": teachername, "payload": f"/router{payload}"}
#             )

#         text = "Select the teacher: "

#         dispatcher.utter_message(text=text, buttons=buttons_list)

#         return [FollowupAction("action_listen")]


class ActionCourse(Action):
    def name(self) -> Text:
        return "list_course"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        buttons_list = []
        course_list = object_list("courseName", tracker)
        course_id = object_list("courseId", tracker)
        results = zip(course_list, course_id)
        # for running in rasax
        # results = zip(["computer programming"], ["5fe09439dfc567003f7afb8b"])
        logger.info("list_course")
        for course, id in results:
            payload = {"course_id": id, "new_action": "open_get_data"}
            payload = json.dumps(payload)
            buttons_list.append(
                {"title": course, "payload": f"/router{payload}"}
            )

        text = "Select the course:"

        dispatcher.utter_message(text=text, buttons=buttons_list)
        return []
