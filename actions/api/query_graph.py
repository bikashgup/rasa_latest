import time
from datetime import datetime, timedelta
from time import mktime

import requests
from actions.log_config import logger

assignement_template = """
**{title}**
Due on: {deadline}
Grade: {grade}
"""
announcement_template = """
**{title}**
Message:{message}
Published On: {published_date}
"""
grade_template = """
**{course}**  :Percentage:   {gpa}
"""
quiz_template = """
**{title}**
Description:{description}
FullScore:{score}
ObtainedScore:{obtained_score}
"""

exam_template = """
**{title}**
Desciption:{description}
FullScore:{score}
ObtainedScore:{obtained_score}
"""


def extract_headers_from_tracker(tracker):
    events = tracker.current_state()["events"]
    for e in reversed(events):
        if e["event"] == "user":
            metadata = e["metadata"]
            try:
                headers = {
                    key: metadata[key]
                    for key in ["Authorization", "Origin", "idToken"]
                }
                logger.info("Header is sent from frontend successfully.")
                return headers
            except KeyError:
                logger.error("Header not sent from frontend")
                return None


def extract_url_from_tracker(tracker):
    events = tracker.current_state()["events"]
    for e in reversed(events):
        if e["event"] == "user":
            metadata = e["metadata"]
            try:
                logger.info(f"Rest Url{metadata['rest_url']} sent from frontend sucessfully.")
                return metadata["rest_url"]
            except KeyError as e:
                logger.error(f"Rest URL not sent from frontend ErrorMessage:{e}")
                return None


def extract_schoolid_from_tracker(tracker):
    events = tracker.current_state()["events"]
   

    for e in reversed(events):
        if e["event"] == "user":
            metadata = e["metadata"]
            try:
                logger.info(f"schoolid {metadata['schoolId']} sent from frontend sucessfully.")
                return metadata["schoolId"]
            except KeyError as e:
                logger.error(f"SchoolId not sent from frontend ErrorMessage:{e}")
                return None


def api_reader(url, params=None, httpmethod="get", data=None, tracker=None):
    headers = extract_headers_from_tracker(tracker)
    fullurl = extract_url_from_tracker(tracker) + "/" + url
    try:
        if httpmethod == "get":
            response = requests.get(fullurl, params=params, headers=headers)
        else:
            response = requests.post(fullurl, headers=headers, json=data)
        logger.success(
            f"api call on fullurl {response.request.url} done sucessfully"
        )
        return response.json()
    except Exception as e:
        logger.error(f"Api call on url {fullurl} Failed")


def school_info(url, attribute, tracker):
    if attribute is None:
        return None
    try:
        res = api_reader(url, tracker=tracker)
        logger.success(
            f"api call on url {url} done sucessfully for school info"
        )
        return res.get(attribute)
    except Exception as e:
        logger.exception(f"Api call on url {url} Failed")
        return None


def teacher_info(url, params, attribute, tracker):
    if attribute is None:
        return None
    try:
        res = api_reader(url, params=params, tracker=tracker)
        logger.success(f"api call on url {url} done sucessfully")
        for p in res:
            return p.get(attribute)
    except Exception as e:
        logger.exception(f"Api call on url {url} Failed")
        return None


def assignment_list(context, url, params, tracker):

    text = ""
    try:

        res = api_reader(url, params, tracker=tracker)
        
        
       
        if not res:
            return res
        logger.info(f"The assignments list are:\n{res}")
        for i, p in enumerate(res["content"]):
            title = p["assignment"]["assignmentTitle"]
            logger.info(f"data  is {p['assignment']}")
            epochtime = p["assignment"]["deadLine"]
            try:
                grade = p["assignment"]["totalGrade"]
            except:
                grade = "NOT Available"
            

            deadline = time.localtime(epochtime / 1000)
            deadline = datetime.fromtimestamp(mktime(deadline))
            deadline = deadline + timedelta(hours=5, minutes=45)
            deadline = deadline.strftime("%m/%d/%Y, %H:%M")
            text = text + assignement_template.format(
                title=title, deadline=deadline, grade=grade
            )
            if i == 4:
                break
        
        
        if context == "help_upcoming_assignments":
            if text:
                return "**The upcoming assignments are** \n\n" + text
            return "Currently, you have no any upcoming assignments.😀"
        elif context == "help_late_assignments":
            if text:
                return "**The late assignments are** \n\n" + text
            return "Congrats!!! you have completed all the assignments till now.😀"
    except Exception as e:
        logger.exception(f"Parsing of API resuts failed")
        return None


def quiz_list(url, params, tracker, context):

    text = ""
    try:
        res = api_reader(url, params, tracker=tracker)
        logger.success(f"api call on url {url} done sucessfully")

        if not res["content"]:
            return res["content"]
        for i, p in enumerate(res["content"]):
            title = str(p["quizTitle"])
            description = str(p["quizDescription"])
            score = str(p["fullScore"])
            if p["obtainedScore"] and str(p["obtainedScore"]) != "null":
                obtained_score = str(format(p["obtainedScore"], ".2f"))
            else:
                obtained_score = "Not Available"

            text = text + quiz_template.format(
                obtained_score=obtained_score,
                title=title,
                description=description,
                score=score,
            )
            if i == 4:
                break
        if context == "help_not_attempted_quiz":
            text = "**Not attempted quizzes are: ** \n\n " + text
        elif context == "help_passed_quiz":
            text = "**Passed quizzes are: ** \n\n " + text
        else:
            text = "**Failed quizzes are: ** \n\n " + text
        return text

    except Exception as e:
        logger.exception(f"Parsing of API resuts failed")
        

        return None


def exam_list(url, params, tracker, context):

    text = ""
    try:
        res = api_reader(url, params, tracker=tracker)
        

        if not res["content"]:
            return res["content"]
        for i, p in enumerate(res["content"]):
            title = str(p["quizTitle"])
            description = str(p["quizDescription"])
            score = str(p["fullScore"])
            if p["obtainedScore"] and str(p["obtainedScore"]) != "null":
                obtained_score = str(format(p["obtainedScore"], ".2f"))
            else:
                obtained_score = "Not available"

            text = text + exam_template.format(
                title=title,
                description=description,
                score=score,
                obtained_score=obtained_score,
            )
            if i == 4:
                break
        if context == "help_not_attempted":
            text = "**Not attempted exams are: ** \n\n " + text
        elif context == "help_passed":
            text = "**Passed exams are: ** \n\n " + text
        else:
            text = "**Failed exams are: ** \n\n " + text
        return text

    except Exception as e:
        logger.exception(f"Parsing of API resuts failed")
        return None


def grade_list(url, tracker):
    text = ""
    try:
        res = api_reader(url, tracker=tracker)
        logger.success(f"api call on url {url} done sucessfully")

        if not res:
            return res
        for p in res[0]["academicCourses"]:
            course = str(p["courseName"])
            gpa = str(p["courseGpa"])

            text = text + grade_template.format(course=course, gpa=gpa)

        return "**These are your grades:** \n\n" + text
    except Exception as e:
        logger.exception(f"Parsing of API resuts failed")
        

        return None


def announcement_list(url, data, tracker):
    try:

        text = ""

        res = api_reader(url, httpmethod="post", data=data, tracker=tracker)
        logger.success(f"api call on url {url} done sucessfully")

        if not res["content"]:
            return res["content"]
        for i, p in enumerate(res["content"]):
            title = str(p["title"])
            message = str(p["message"])
            epochtime = p["publishedDate"]
            published_date = time.localtime(epochtime / 1000)
            published_date = datetime.fromtimestamp(mktime(published_date))
            published_date = published_date + timedelta(hours=5, minutes=45)
            published_date = published_date.strftime("%m/%d/%Y, %H:%M")

            text = text + announcement_template.format(
                title=title, message=message, published_date=published_date
            )
            if i == 4:
                break

        return "**Your recent announcements are:** \n\n" + text

    except Exception as e:
        logger.exception(f"Parsing of API resuts failed")
        return None


def object_list(object_type, tracker):
    try:

        url = "api/v2/enrolledCourses"
        results = api_reader(url, tracker=tracker)
        logger.info(f"object list results is {results}")

        object_list = []
        for p in results:
            if object_type == "courseBy":
                object_list.append(p[object_type][0])
            else:
                object_list.append(p[object_type])
        return object_list

    except Exception as e:
        logger.exception(f"Parsing of API resuts failed")
        return None
