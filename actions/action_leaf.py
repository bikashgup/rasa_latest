import ast
from typing import Any, Dict, List, Text

import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.api.query_graph import extract_schoolid_from_tracker
from actions.log_config import logger
db_help = pd.read_csv("./actions/data/menu.csv")


class ActionLeaf(Action):
    def name(self) -> Text:
        return "action_leaf"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        current_intent = tracker.latest_message["intent"].get("name")
        context = current_intent
        # school_id = extract_schoolid_from_tracker(tracker)
        help_context = db_help[db_help["context"] == current_intent]
        if help_context.empty:
            dispatcher.utter_message(text="I'm sorry I could not find help. 😕")
            return []
        if help_context.action.notnull().values:
            next_action = help_context.action.values[0]

            if help_context.object_type.notnull().values:
                object_type = help_context["object_type"]
                object_type = ast.literal_eval(object_type.iloc[0])[0]

            else:
                object_type = "null"

            if help_context.attribute.notnull().values:
                attribute = help_context["attribute"]
                attribute = ast.literal_eval(attribute.iloc[0])[0]

            else:
                attribute = "null"
        logger.info("action_leaf")
        return [
            SlotSet("context", context),
            SlotSet("object_type", object_type),
            SlotSet("attribute", attribute),
            FollowupAction(next_action),
        ]
