# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Tuple
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
#
#
from actions.constants import EMAIL, REQUESTED_SLOT,OTP
from actions.database_utils import is_valid_user, is_valid_otp
from rasa_sdk.events import ReminderScheduled, ReminderCancelled
import sqlite3
import datetime

class ActionSetReminder(Action):
    """Schedules a reminder, supplied with the last message's entities."""

    def name(self) -> Text:
        return "action_set_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

      #  dispatcher.utter_message("I will remind you in 60 seconds.")

        date = datetime.datetime.now() + datetime.timedelta(seconds=1800)
       # entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled(
            "request_feedback",
            trigger_date_time=date,
            name="my_reminder",
            kill_on_user_message=False,
        )

        return [reminder]
        
class ActionHelloWorld(Action):
#
    def name(self) -> Text:
        return "action_utter_slot_values"
#
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("email")
        fdback = tracker.get_slot("fdback")
        conn = sqlite3.connect("user_data.db")
        c = conn.cursor()

        # Insert the user input text into the database
        c.execute("INSERT INTO DB (user_id, email) VALUES (?, ?)", (email, fdback,))
        conn.commit()

        # Close the database connection
        conn.close()
        if email is not None:
            dispatcher.utter_message(text="Feedback recorded successfully")

class ActionAuthenticate(Action):

    def name(self) -> Text:
        return "action_authenticate"

    def run(self, dispatcher, tracker, domain):
        authenticated = tracker.get_slot("authenticated")
        if not authenticated:
            dispatcher.utter_template("utter_not_authenticated", tracker)
            return []
        return []
        
class ActionCheckIsAuth(Action):
    def name(self) -> Text:
        return "action_check_is_auth"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if(tracker.get_slot('authenticated')!=True):
            dispatcher.utter_message(response="utter_loginfail")
        return []

class GreetAction(Action):
    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
            dispatcher.utter_message(text="Welcome to the UPES HelpDesk. Please login to continue...")
            return []

class AuthenticatedAction(Action):
    def name(self) -> Text:
        return "action_authenticated"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
            email = tracker.get_slot("email")
            otp = tracker.get_slot("otp")
            if email is not None and otp is not None:
                dispatcher.utter_message(template="utter_authenticated_successfully")
                return [SlotSet("authenticated", True)]
            else:
                dispatcher.utter_message(text="utter_authentication_failure")
            return []

class ActionDefaultFallback(Action):

   def name(self):
      return "action_default_fallback"

   def run(self, dispatcher, tracker, domain):
      dispatcher.utter_message("Sorry, I couldn't understand.")


class ValidateAuthFormAction(FormValidationAction):
    def name(self) -> Text:
        return "validate_auth_form"

    def validate_email(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[EventType]:
        returned_slots = {}
        if value is not None and is_valid_user(value):
            returned_slots = {EMAIL:value}
        else:
            returned_slots = {REQUESTED_SLOT: EMAIL}
            if value is None:
                dispatcher.utter_message(template="utter_email_not_valid")
            elif not is_valid_user(value):
                dispatcher.utter_message(template="utter_email_not_registered")
        return returned_slots

    def validate_otp(
        self,
        value: float,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[EventType]:
        email = tracker.get_slot(EMAIL)
        returned_slots = {}
        if value is not None and is_valid_otp(value,email):
            returned_slots = {OTP:value}
        else:
            returned_slots ={REQUESTED_SLOT:OTP}
            dispatcher.utter_message(template="utter_otp_not_valid")
        return returned_slots
        
    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Setting the authenticated slot to True if user credentials are valid
        return [SlotSet("authenticated", True)]

