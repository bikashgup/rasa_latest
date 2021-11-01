import ast
import json
from typing import Any, Dict, List, Text

import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.log_config import logger


help_db = pd.read_csv("./actions/data/menu.csv")
context_mapping = pd.read_csv("./actions/data/intent_description_mapping.csv")


class ActionHelpMenu(Action):
    def name(self) -> Text:
        return "action_help_menu"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        context = tracker.get_slot("context")
        

        help_context = help_db[(help_db["context"] == context)]
        logger.info("action_help_menu")
        if help_context.empty:
            context_mapper_db = context_mapping[
                (context_mapping["intent"] == context)
            ]
            context2word = context_mapper_db.entities.values
            if context2word:
                dispatcher.utter_message(
                    text=f"Sorry, I'm not sure I've understood you correctly🤔 Do you mean '{context2word[0]}'. I don't think I have that information."
                )
                return []
            else:
                dispatcher.utter_message(
                    text=f"Sorry, I'm not sure I've understood you correctly🤔 .I don't think I have that information."
                )
            return []


        if help_context.action.isnull().values:

            button_choices = help_context.buttons
            button_context = help_context["button_context"]
            button_choices = ast.literal_eval(button_choices.iloc[0])
            button_context = ast.literal_eval(button_context.iloc[0])
            if help_context.object_type.notnull().values:

                object_type = help_context["object_type"]
               
                object_type = ast.literal_eval(object_type.iloc[0])

            else:
                object_type = ["null"] * len(button_context)
            if help_context.attribute.notnull().values:
                attribute = help_context["attribute"]
                
                attribute = ast.literal_eval(attribute.iloc[0])

            else:
                attribute = ["null"] * len(button_context)

            buttons = []
            
            for choice, context, obj, attrib in zip(
                button_choices, button_context, object_type, attribute
            ):
                payload = {
                    "context": context,
                    "object_type": obj,
                    "attribute": attrib,
                }
                payload = json.dumps(payload)

                buttons.append(
                    {"title": f"{choice}", "payload": f"/choose{payload}"}
                )

            help_message = help_context.message.values[0]
            dispatcher.utter_message(text=help_message, buttons=buttons)

            return [FollowupAction("action_listen")]

        
        elif (
            help_context.action.notnull().values
            and help_context.message.isnull().values
        ):
            next_action = help_context.action.values[0]
            return [
                FollowupAction(next_action),
            ]

        else:
            help_message = help_context.message.values[0]
            dispatcher.utter_message(help_message)
            next_action = help_context.action.values[0]
            return [
                FollowupAction(next_action),
            ]
