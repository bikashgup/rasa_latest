from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from actions.log_config import logger

class ActionInitTutorial(Action):
    def name(self):
        return "action_init_tutorial"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        logger.info("action_init_tutorial")
        return [SlotSet("context", "help"), FollowupAction("action_help_menu")]
