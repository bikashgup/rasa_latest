from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction

from rasa_sdk.executor import CollectingDispatcher
from actions.log_config import logger
class ActionRouter(Action):
    def name(self):
        return "action_router"

    async def run(self, dispatcher, tracker, domain):
        newaction = tracker.get_slot("new_action")
        logger.info("action_router")
        return [FollowupAction(newaction)]