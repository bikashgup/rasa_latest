import random
from typing import Any, Dict, Text

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from actions.log_config import logger

class ValidateOpenGetData(FormValidationAction):
    """Gets data from user"""

    def name(self) -> Text:
        return "validate_open_get_data"

    def validate_data(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if len(slot_value) > 50:
            dispatcher.utter_message(
                text=random.choice(
                    [
                        "Oh wow, that question was too long. Haha\
                    I couldn't understand that. Please rephrase it ok. Go ahead ask me!",
                        "Haha. That question was too long for me to understand \
                    Can you make it shorter please? Go ahead, ask me :) ",
                    ]
                )
            )

            return {"data": None}
        else:
            return {"data": slot_value}

  