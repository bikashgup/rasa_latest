import json
from typing import Any, Dict, List, Optional, Text, Union

import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.events import (
    ConversationPaused,
    EventType,
    FollowupAction,
    SlotSet,
    UserUtteranceReverted,
)
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from actions.api.query_graph import extract_schoolid_from_tracker
from actions.elasticbert import search_query_fallback
from actions.log_config import logger

INTENT_DESCRIPTION_MAPPING_PATH = (
    "./actions/data/intent_description_mapping.csv"
)


class ActionDefaultAskAffirmation(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self) -> Text:
        return "action_default_ask_affirmation"

    def __init__(self) -> None:
        import pandas as pd

        self.intent_mappings = pd.read_csv(INTENT_DESCRIPTION_MAPPING_PATH)
        self.intent_mappings.fillna("", inplace=True)
        self.intent_mappings.entities = self.intent_mappings.entities.map(
            lambda entities: {e.strip() for e in entities.split(",")}
        )

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        last_message = tracker.latest_message.get("text")
        school_id = extract_schoolid_from_tracker(tracker)
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
            message_title = "Do you mean any of these"
            dispatcher.utter_message(text=message_title, buttons=buttons)
            return []
        else:
            dispatcher.utter_message(
                "Sorry something is wrong.Please try again later."
            )
            logger.exception(
                "ES server is not returning any results.please once look into corresponding index"
            )
            return [
                SlotSet("new_action", "action_help_menu"),
                SlotSet("context", "help"),
                FollowupAction("action_router"),
            ]

        # if buttonid:
        # return [
        #     SlotSet("buttonid", buttonid),
        #     FollowupAction("action_queryredisid"),
        # ]

    #     intent_ranking = tracker.latest_message.get("intent_ranking", [])
    #     if len(intent_ranking) > 1:
    #         diff_intent_confidence = intent_ranking[0].get(
    #             "confidence"
    #         ) - intent_ranking[1].get("confidence")
    #         if diff_intent_confidence < 0.2:
    #             intent_ranking = intent_ranking[:2]
    #         else:
    #             intent_ranking = intent_ranking[:1]

    #     # for the intent name used to retrieve the button title, we either use
    #     # the name of the name of the "main" intent, or if it's an intent that triggers
    #     # the response selector, we use the full retrieval intent name so that we
    #     # can distinguish between the different sub intents
    #     first_intent_names = [
    #         intent.get("name", "")
    #         if intent.get("name", "")
    #         not in ["out_of_scope", "fuseclassroom", "chitchat", "smalltalk"]
    #         else tracker.latest_message.get("response_selector")
    #         .get(intent.get("name", ""))
    #         .get("full_retrieval_intent")
    #         for intent in intent_ranking
    #     ]

    #     message_title = (
    #         "Sorry, I'm not sure I've understood "
    #         "you correctly 🤔 Do you mean..."
    #     )

    #     entities = tracker.latest_message.get("entities", [])
    #     entities = {e["entity"]: e["value"] for e in entities}

    #     entities_json = json.dumps(entities)

    #     buttons = []
    #     for intent in first_intent_names:
    #         button_title = self.get_button_title(intent, entities)
    #         if "/" in intent:
    #             # here we use the button title as the payload as well, because you
    #             # can't force a response selector sub intent, so we need NLU to parse
    #             # that correctly
    #             buttons.append(
    #                 {"title": button_title, "payload": button_title}
    #             )
    #         else:
    #             buttons.append(
    #                 {
    #                     "title": button_title,
    #                     "payload": f"/{intent}{entities_json}",
    #                 }
    #             )

    #     buttons.append(
    #         {"title": "Something else", "payload": "/trigger_rephrase"}
    #     )

    # dispatcher.utter_message(text=message_title, buttons=buttons)

    #     return []

    # def get_button_title(
    #     self, intent: Text, entities: Dict[Text, Text]
    # ) -> Text:
    #     default_utterance_query = self.intent_mappings.intent == intent
    #     utterance_query = (
    #         self.intent_mappings.entities == entities.keys()
    #     ) & (default_utterance_query)

    #     utterances = self.intent_mappings[utterance_query].button.tolist()

    #     if len(utterances) > 0:
    #         button_title = utterances[0]
    #     else:
    #         utterances = self.intent_mappings[
    #             default_utterance_query
    #         ].button.tolist()
    #         button_title = utterances[0] if len(utterances) > 0 else intent

    #     return button_title.format(**entities)


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        # Fallback caused by TwoStageFallbackPolicy
        if (
            len(tracker.events) >= 4
            and tracker.events[-4].get("name")
            == "action_default_ask_affirmation"
        ):
            dispatcher.utter_message(template="utter_suggestion")

            return []

        # Fallback caused by Core
        else:
            dispatcher.utter_message(template="utter_default")
            return [UserUtteranceReverted()]
