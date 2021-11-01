from typing import Any, Dict, List, Text

from config_parser import env
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.api.message_resolver import resolve_message
from actions.api.query_graph import (
    announcement_list,
    assignment_list,
    exam_list,
    grade_list,
    object_list,
    quiz_list,
    school_info,
    teacher_info,
)
from actions.log_config import logger


class QuerySchool(Action):
    def name(self):
        return "query_school"

    async def run(
        self, dispatcher, tracker, domain,
    ):
        logger.info("query_school")
        attribute = tracker.get_slot("attribute")

        url = "api/v2/schoolProfiles"
        logger.info("On Query School action")

        results = school_info(url, attribute, tracker,)

        if results is None:

            dispatcher.utter_message(
                "Sorry, 🤔 It seems I don't have that information about your school."
            )
            return [FollowupAction("action_bottom_top_menu")]

        text = resolve_message(
            intent="school_info", attribute=attribute, results=results,
        )
        dispatcher.utter_message(text)
        return [FollowupAction("action_bottom_top_menu")]


# class QueryTeacher(Action):
#     def name(self):
#         return "query_teacher"

#     async def run(
#         self, dispatcher, tracker, domain,
#     ):
#         logger.info("On Query Teacher Actions")

#         attribute = tracker.get_slot("attribute")

#         # url = "api/v2/schoolProfiles"
#         url = "api/v2/academicStaff?"

#         courseId = tracker.get_slot("course_id")

#         params = {
#             "courseId": courseId,
#         }
#         results = teacher_info(
#             url, params=params, attribute=attribute, tracker=tracker,
#         )
#         teachername = tracker.get_slot("teacher_name")

#         if results is None:
#             dispatcher.utter_message(
#                 "Sorry, 🤔 I think I don't have that information about your teacher."
#             )
#             return [
#                 SlotSet("counter", "0",),
#                 FollowupAction("action_bottom_top_menu"),
#             ]
#         text = resolve_message(
#             intent="teacher_info",
#             name=teachername,
#             attribute=attribute,
#             results=results,
#         )
#         dispatcher.utter_message(text)
#         return [FollowupAction("action_bottom_top_menu")]


class ActionAssignements(Action):
    def name(self):
        return "query_assignments"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        logger.info("query_assignments")
        context = tracker.get_slot("context")
        courseId = []
        batchId = []

        courseId = set(object_list("courseId", tracker,))
        batchId = set(object_list("batchId", tracker,))
        logger.info(f"course id is {courseId}")
        logger.info(f"bATCH id is {batchId}")

        url = "api/v2/assignments/students/papers?"

        if tracker.get_slot("context") == "help_late_assignments":

            params = {
                "filterBy": "overdue",
                "page": 1,
                "size": 10,
                "courseId": list(courseId),
                "batchId": list(batchId),
                "filterByGradeType":"",
                "keyword":"",
                "assignmentType":"PAPER"

            }

        else:

            params = {
                "filterBy": "notSubmitted",
                "page": 1,
                "size": 10,
                "courseId": list(courseId),
                "batchId": list(batchId),
                "filterByGradeType":"",
                "keyword":"",
                "assignmentType":"PAPER"

            }
        text = assignment_list(context, url, params, tracker)
        if not text:
            if tracker.get_slot("context") == "help_late_assignments":
                dispatcher.utter_message(
                    "I couldn't find any late assignments at the moment. 😁"
                )
            else:
                dispatcher.utter_message(
                    "I couldn't find any upcoming assignments at the moment. Check again later!😊 "
                )

            return [FollowupAction("action_bottom_top_menu")]

        if text is None:  # for exception
            dispatcher.utter_message(
                "I couldn't find your assignments. Something must be wrong.🤔Check again later, sorry."
            )
            return [FollowupAction("action_bottom_top_menu")]

        dispatcher.utter_message(text)
        return [FollowupAction("action_bottom_top_menu")]


class ActionQuiz(Action):
    def name(self):
        return "query_quiz"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        logger.info("On Query Quiz action")

        url = "api/v2/students/quiz?"
        if tracker.get_slot("context") == "help_not_attempted_quiz":
            params = {
                "courseIds": "",
                "batchIds": "",
                "quizAttemptType": "NOT_ATTEMPTED",
                "quizType": "QUIZ",
                # "page": 1,
                # "size": 10,
            }

        elif tracker.get_slot("context") == "help_passed_quiz":

            params = {
                "courseIds": "",
                "batchIds": "",
                "quizAttemptType": "PASSED",
                "quizType": "QUIZ",
            }
        else:
            params = {
                "courseIds": "",
                "batchIds": "",
                "quizAttemptType": "FAILED",
                "quizType": "QUIZ",
            }
        text = quiz_list(url, params, tracker, tracker.get_slot("context"))

        if not text:  # for empty lists
            dispatcher.utter_message(
                "I couldn't find any quizzes at the moment.Check again later! 🤓 "
            )
            return [FollowupAction("action_bottom_top_menu")]

        if text is None:  # for exception
            dispatcher.utter_message(
                "I couldn't find any quizes. Something must be wrong.🤔 Check again later, sorry."
            )
            return [FollowupAction("action_bottom_top_menu")]

        dispatcher.utter_message(text)
        return [FollowupAction("action_bottom_top_menu")]


class ActionGrade(Action):
    def name(self):
        return "query_grade"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        logger.info("On Query Grade action")

        url = "api/v2/grades/homePage/student/semester"
        text = grade_list(url, tracker)
        if not text:
            dispatcher.utter_message(
                "I couldn't find your grades. Something must be wrong.🤔 Check again later, sorry. "
            )
            return [FollowupAction("action_bottom_top_menu")]
        if text is None:
            dispatcher.utter_message(
                "🤔 I couldn't find your grades.Something must be wrong.Check again later, sorry."
            )
            return [FollowupAction("action_bottom_top_menu")]

        dispatcher.utter_message(text)
        return [FollowupAction("action_bottom_top_menu")]


class ActionAnnouncement(Action):
    def name(self):
        return "query_announcement"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        logger.info("On Query announcement action")

        url = "announcements/messages/students"
        if tracker.get_slot("context") == "help_class_announcements":

            data = {
                "sortBy": "",
                "sortOrder": "",
                "batchId": [],
                "courseId": [],
                "filterBy": "Class_Announcement",
                "page": 1,
                "size": 10,
            }

        else:

            data = {
                "sortBy": "",
                "sortOrder": "",
                "batchId": [],
                "courseId": [],
                "filterBy": "General_Announcement",
                "page": 1,
                "size": 10,
            }

        text = announcement_list(url, data, tracker,)
        if not text:
            dispatcher.utter_message(
                "I couldn't find any announcements at the moment.Check again later. "
            )
            return [FollowupAction("action_bottom_top_menu")]

        if text is None:
            dispatcher.utter_message(
                "I couldn't find any announcements. Something must be wrong.🤔 Check again later, sorry. "
            )
            return [FollowupAction("action_bottom_top_menu")]

        dispatcher.utter_message(text)
        return [FollowupAction("action_bottom_top_menu")]


class ActionExam(Action):
    def name(self):
        return "query_exam"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        logger.info("On Query exam action")

        url = "api/v2/students/quiz?"
        if tracker.get_slot("context") == "help_not_attempted":
            params = {
                "courseIds": "",
                "batchIds": "",
                "quizAttemptType": "NOT_ATTEMPTED",
                "quizType": "EXAM",
            }

        elif tracker.get_slot("context") == "help_passed":

            params = {
                "courseIds": "",
                "batchIds": "",
                "quizAttemptType": "PASSED",
                "quizType": "EXAM",
            }
        else:
            params = {
                "courseIds": "",
                "batchIds": "",
                "quizAttemptType": "FAILED",
                "quizType": "EXAM",
            }

        text = exam_list(url, params, tracker, tracker.get_slot("context"))
        if not text:
            dispatcher.utter_message(
                "I couldn't find any exam at the moment.Check again later. "
            )
            return [FollowupAction("action_bottom_top_menu")]

        if text is None:
            dispatcher.utter_message(
                "I couldn't find any exam. Something must be wrong.🤔 Check again later, sorry. "
            )
            return [FollowupAction("action_bottom_top_menu")]

        dispatcher.utter_message(text)
        return [FollowupAction("action_bottom_top_menu")]
