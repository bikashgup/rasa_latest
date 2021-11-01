from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.log_config import logger

class ActionIntentSlotMap(Action):
    def name(self) -> Text:
        return "action_intent_slot_map"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("In action_intent_slot_map:")
        current_intent = tracker.latest_message["intent"].get("name")
        # context_to_set = intent_slot_dict[current_intent]
        logger.info("action_intent_slot_map")
        return [
            SlotSet("context", current_intent),
            FollowupAction("action_help_menu"),
        ]
