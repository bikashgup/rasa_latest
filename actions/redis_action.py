import ast
import json
import random
from typing import Any, Dict, List, Text

import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet

from actions.api.query_graph import extract_schoolid_from_tracker
from actions.elasticbert import search_query_fallback
from actions.log_config import logger
from actions.queryredis import get_parent_button, read_obj

help_db = pd.read_csv("actions/data/menu.csv")


class ActionElasticRedis(Action):
    def name(self):
        return "action_elastic_redis"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        logger.info("action_elastic_redis")
        last_message = tracker.latest_message.get("text")
        school_id = extract_schoolid_from_tracker(tracker)
        
        if not school_id:
            dispatcher.utter_message(
                "Sorry 🤔 something is wrong.Please try again later."
            )
            return []
        buttonid = search_query_fallback(last_message, school_id)
        if isinstance(buttonid, str):
            return [
                SlotSet("buttonid", buttonid),
                FollowupAction("action_queryredisid"),
            ]
        elif isinstance(buttonid, zip):
            buttons = []
            for objectid, label in buttonid:
                payload = {
                    "buttonid": objectid,
                    "new_action": "action_queryredisid",
                }
                payload = json.dumps(payload)

                buttons.append(
                    {"title": label, "payload": f"/router{payload}",}
                )
            payload = {
                "context": "School Info",
                "new_action": "action_help_menu",
            }
            payload = json.dumps(payload)
            buttons.append(
                {"title": "School Info", "payload": f"/router{payload}"}
            )
            message_title = "Do you mean any of these"
            dispatcher.utter_message(text=message_title, buttons=buttons)
            return []
        else:
            dispatcher.utter_message(
                "Sorry something is wrong.Please try again later."
            )
            
            return [
                SlotSet("new_action", "action_help_menu"),
                SlotSet("context", "help"),
                FollowupAction("action_router"),
            ]


class ActionDatabase(Action):
    def name(self) -> Text:
        return "action_queryredis_csv"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        school_id = extract_schoolid_from_tracker(tracker)
        logger.info("action_queryredis_csv") 
        if not school_id:
            dispatcher.utter_message(
                "Sorry 🤔 something is wrong.Please try again later."
            )
            return []
        context = tracker.get_slot("context")
        try:
            parent_button_list = get_parent_button(school_id)
        except ConnectionError as e:
            logger.error("Connection error to redis server Error Message{e}")
            dispatcher.utter_message(
                "Sorry 🤔 something is wrong.Please try again later."
            )
            return []
        

        parentbuttonlabel = list(parent_button_list.keys())
        parentbuttonpayload = list(parent_button_list.values())
        buttons = []
        if not parentbuttonlabel and not parentbuttonpayload:

            return [FollowupAction("action_bottom_top_menu")]

        # this loop generate button for parent i.e. button right after csv
        for button_label, button_id in zip(
            parentbuttonlabel, parentbuttonpayload
        ):
            payload = {
                "buttonid": button_id,
                "new_action": "action_queryredisid",
            }
            payload = json.dumps(payload)
            buttons.append(
                {"title": f"{button_label}", "payload": f"/router{payload}"}
            )

        # find previous context before current context "schoolinfo" from csv and take contol to action_help_menu for back button
        help_context = help_db[help_db["context"] == context]

        context = help_context.prev_context_leaf.values[0]

        backbuttonpayload = {
            "buttonid": None,
            "context": context,
            "new_action": "action_help_menu",
        }
        backbuttonpayload = json.dumps(backbuttonpayload)
        buttons.append(
            {"title": "Back", "payload": f"/router{backbuttonpayload}"}
        )
        dispatcher.utter_message(text="This is what I have", buttons=buttons)

        return [FollowupAction("action_listen")]


class ActionDatabaseId(Action):
    def name(self) -> Text:
        return "action_queryredisid"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
    
        logger.info("action_queryredisid")
        parentid = tracker.get_slot("buttonid")
        try:
            button_obj = read_obj(parentid)
        except ConnectionError:
            logger.error("Connection error to redis server Error Message{e}")
            dispatcher.utter_message("Sorry 🤔 something is wrong.Please try again later.")
        # button_obj = read_obj(parentid)  # Only None when we are in parent node
        
        if not button_obj:
            return [
                FollowupAction("action_router"),
                SlotSet("new_action", "action_queryredis_csv"),
                SlotSet("context", "School Info"),
            ]
        message_list = []

        if button_obj.get("answerTypes"):

            answer_type = ast.literal_eval(button_obj.get("answerTypes"))
            for p in answer_type:
                

                if p["type"] == "text":
                    message = p.get("text")
                    message = random.choice(message)
                    message_info = {"type": "text", "msg": message}

                    message_list.append(message_info)
                else:
                    message = p.get("uri")
                    message = random.choice(message)
                    message_info = {"type": "uri", "msg": message}
                    message_list.append(message_info)
                    
       

        backbutton_payload = {
            "buttonid": button_obj.get("parent"),
            "new_action": "action_queryredisid",
        }
        backbutton_payload = json.dumps(backbutton_payload)

        child_button_id = ast.literal_eval(button_obj.get("children"))
        if not child_button_id:
            for message in message_list:
                if message["type"] == "text":
                    text = message["msg"]
                    

                    dispatcher.utter_message(text=text)

                else:
                    attachment = message["msg"].rsplit("/", 1)[-1]
                    buttons_list = []
                    logger.info(f"attachment is {attachment} ")

                    payload = f"{message['msg']}"
                    payload = json.dumps(payload)
                    buttons_list.append(
                        {"title": attachment, "payload": f"{payload}/link",}
                    )
                    dispatcher.utter_message(
                        text="Please click the following link",
                        buttons=buttons_list,
                    )
            return [FollowupAction("action_top_menu_nlu")]
           

        buttons = []
        for childid in child_button_id:
            button_obj = read_obj(childid)
            button_label = button_obj.get("label")
            payload = {
                "buttonid": childid,
                "new_action": "action_queryredisid",
            }
            payload = json.dumps(payload)
            buttons.append(
                {"title": f"{button_label}", "payload": f"/router{payload}"}
            )
        buttons.append(
            {"title": "Back", "payload": f"/router{backbutton_payload}"}
        )
       

        for message in message_list:
            if message["type"] == "text":
                text = message["msg"]
                dispatcher.utter_message(text)
            else:
                attachment = message["msg"].rsplit("/", 1)[-1]

                logger.info(f"attachment is {attachment} ")
                buttons_list = []
                payload = f"{message['msg']}"
                payload = json.dumps(payload)

                buttons_list.append(
                    {"title": f"{attachment}", "payload": f"{payload}/link"}
                )
                dispatcher.utter_message(
                    text="Please click the following link",
                    buttons=buttons_list,
                )

        dispatcher.utter_message(text="Select from below", buttons=buttons)
        return []
