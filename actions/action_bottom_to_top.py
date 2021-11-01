import json
from typing import Any, Dict, List, Text

import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.log_config import logger 

# from actions.api.query_graph import extract_schoolid_from_tracker

db_help = pd.read_csv("./actions/data/menu.csv")


class ActionBottomTopMenu(Action):
    def name(self) -> Text:
        return "action_bottom_top_menu"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        current_context = tracker.get_slot("context")
        rows = db_help[db_help["context"] == current_context]
        prev_context = rows.loc[rows.index[0], "prev_context_leaf"]
        prev_action = rows.loc[rows.index[0], "prev_action_leaf"]
        if (current_context.lower() == "school info") or (current_context.lower() == "school_info"):
            button_label = ["⬅ Back to top"]
            button_code = ["help"]
            new_action = ["action_help_menu"]
            text = "I have not been programmed by school admin yet. Please check again soon!"

        else:
            button_label = ["⬅ Back", "⬆ Top"]
            button_code = [prev_context, "help"]
            new_action = [prev_action, "action_help_menu"]
            text = "What else can I help you with?"
        buttons_list = []
        for label, code, action in zip(button_label, button_code, new_action):
            print("label:", label, "code:", code, "action:", action)
            payload = {"context": code, "new_action": action}
            payload = json.dumps(payload)
            buttons_list.append(
                {"title": f"{label}", "payload": f"/router{payload}"}
            )
        logger.info("action_bottom_top_menu")
        dispatcher.utter_message(text=text, buttons=buttons_list)

        return [
            FollowupAction("action_listen"),
        ]


class ActionTopMenuNlu(Action):
    def name(self) -> Text:
        return "action_top_menu_nlu"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        button_label = "⬆ Back to Top"
        button_code = "help"
        new_action = "action_help_menu"
        buttons_list = []
        payload = {"context": button_code, "new_action": new_action}
        payload = json.dumps(payload)
        buttons_list.append(
            {"title": f"{button_label}", "payload": f"/router{payload}"}
        )
        text = "Hope that was useful 😊😊"
        dispatcher.utter_message(text=text, buttons=buttons_list)
        logger.info("action_top_menu_nlu")
        return [
            FollowupAction("action_listen"),
        ]
