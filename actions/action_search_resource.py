import json
from typing import Any, Dict, List, Text

import requests
from config_parser import env
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.api.query_graph import object_list
from actions.log_config import logger


class ActionSearchResource(Action):
    def name(self) -> Text:
        return "action_search_resource"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        logger.success("on search resources action")

        data = tracker.get_slot("data")
        query = data

        dispatcher.utter_message(text="Searching resources, please wait...😊!")
        courses = [tracker.get_slot("course_id")]

        res = await self._get_recommendation(query, courses)
        if not res:
            dispatcher.utter_message(
                "I couldn't find any resources that maybe helpful to you."
            )
            return [
                SlotSet("data", None),
                FollowupAction("action_bottom_top_menu"),
            ]

        if res is None:
            dispatcher.utter_message(
                "I couldn't find any resources.Something must be wrong.🤔 Check again later, sorry."
            )

            return [
                SlotSet("data", None),
                FollowupAction("action_bottom_top_menu"),
            ]
        dispatcher.utter_message(
            "You might find the following link helpful: \n"
        )
        for i, (title, url) in enumerate(res):
            buttons_list = []
            if url and title:
                payload = f"{url}"
                payload = json.dumps(payload)
                buttons_list.append(
                    {"title": title, "payload": f"{payload}/link"}
                )
            if i == 3:
                break
            dispatcher.utter_message(text="", buttons=buttons_list)
        return [
            SlotSet("data", None),
            FollowupAction("action_bottom_top_menu"),
        ]

    async def _get_recommendation(self, query, courses):

        data = {"query": query, "courses": courses}

        # auth = ("fuseclassroom-dev", "M!jDwkTEa3KZ")
        auth = (
            "{}".format(env["actions"]["action_search_resource"]["user_name"]),
            "{}".format(env["actions"]["action_search_resource"]["password"]),
        )
        headers = {"Content-Type": "application/json"}

        url = (
            "{}".format(env["actions"]["action_search_resource"]["url"])
            + "api/search/query"
        )
        try:
            recommendations = requests.post(
                url, auth=auth, headers=headers, json=data
            )
            recommendation = recommendations.json()
            if not recommendation:
                return []
            res = []
            for _, p in enumerate(recommendation):
                a, b = p.get("title"), p.get("url")
                res.append((a, b))
            logger.success(f"api call on url {url} done sucessfully")

            return res
        except Exception as e:
            logger.exception(
                f"Api call on url {url} Failed   ErrorMessage: {e}"
            )
            return None


class ActionSearchResourceFromNlu(Action):
    def name(self) -> Text:
        return "action_search_resource_nlu"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        logger.success("on search resources through nlu action")

        if (
            len(tracker.events) >= 4
            and tracker.events[-4].get("name") == "action_ask_affirmation"
        ):
            query = tracker.events[-5].get("text")
        else:
            query = tracker.latest_message["text"].split(" ", 1)[1]

        dispatcher.utter_message(text="Searching resources, please wait...😊!")
        courses = object_list("courseId", tracker)

        res = await self._get_recommendation(query, courses)
        if not res:
            dispatcher.utter_message(
                "I couldn't find any resources that maybe helpful to you."
            )
            return [
                SlotSet("data", None),
                FollowupAction("action_bottom_top_menu"),
            ]

        if res is None:
            dispatcher.utter_message(
                "I couldn't find any resources.Something must be wrong.🤔 Check again later, sorry."
            )

            return [
                SlotSet("data", None),
                FollowupAction("action_bottom_top_menu"),
            ]
        dispatcher.utter_message(
            "You might find the following link helpful: \n"
        )
        for i, (title, url) in enumerate(res):
            buttons_list = []
            if url and title:
                payload = f"{url}"
                payload = json.dumps(payload)
                buttons_list.append(
                    {"title": title, "payload": f"{payload}/link"}
                )
            if i == 3:
                break
            dispatcher.utter_message(text="", buttons=buttons_list)
        return [
            SlotSet("data", None),
            FollowupAction("action_bottom_top_menu"),
        ]

        return [
            SlotSet("data", None),
            FollowupAction("action_bottom_top_menu"),
        ]

    async def _get_recommendation(self, query, courses):

        data = {"query": query, "courses": courses}

        # auth = ("fuseclassroom-dev", "M!jDwkTEa3KZ")
        auth = (
            "{}".format(env["actions"]["action_search_resource"]["user_name"]),
            "{}".format(env["actions"]["action_search_resource"]["password"]),
        )
        headers = {"Content-Type": "application/json"}

        url = (
            "{}".format(env["actions"]["action_search_resource"]["url"])
            + "api/search/query"
        )
        try:
            recommendations = requests.post(
                url, auth=auth, headers=headers, json=data
            )
            recommendation = recommendations.json()
            if not recommendation:
                return []
            res = []
            for _, p in enumerate(recommendation):
                a, b = p.get("title"), p.get("url")
                res.append((a, b))
            logger.success(f"api call on url {url} done sucessfully")

            return res
        except Exception as e:
            logger.exception(
                f"Api call on url {url} Failed   ErrorMessage: {e}"
            )
            return None
