
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from connect_db import check_customer_by_name, add_customer, select_dishes,add_order,select_dishes_by_if_special,select_dishes_by_style
import random
import string
import datetime

# Check if the customer is new member
class CheckNewCustomer(Action):
    def name(self) -> Text:
        return 'action_check_new'

    def run(self, 
            dispatcher: "CollectingDispatcher", 
            tracker: Tracker, domain: "DomainDict"
    ) -> List[Dict[Text, Any]]:
        if check_customer_by_name(tracker.get_slot('name')) == False:
            buttons = [{"payload": "/register", "title": "Register"}]
            dispatcher.utter_message(text = "I think you are a new customer. Let's register an account now.", buttons=buttons)
        elif check_customer_by_name(tracker.get_slot('name')) == True:
            dispatcher.utter_message(text="What can I help you now?", buttons= [
                {"payload": "/order_table", "title": "Order a table"},
                {"payload": "/show_type_inform", "title": "Show Information"},
            ])
        return []

# Add one new customer into database
class AddNewCustomer(Action):
    def name(self) -> Text:
        return 'action_add_new_customer'
    
    def run(self, 
            dispatcher: "CollectingDispatcher", 
            tracker: Tracker, 
            domain: "DomainDict"
        ) -> List[Dict[Text, Any]]:
        add_customer(tracker.get_slot("name"), tracker.get_slot("email"))
        dispatcher.utter_message(text="What can I help you now?", buttons= [
            {"payload": "/order_table", "title": "Order a table"},
            {"payload": "/show_type_inform", "title": "Show Information"},
        ])
        return []

# Add one new order into database
class AddNewOrder(Action):
    def name(self) -> Text:
        return 'action_add_new_order'

    def run(
        self, 
        dispatcher: "CollectingDispatcher", 
        tracker: Tracker, 
        domain: "DomainDict"
    ) -> List[Dict[Text, Any]]:
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        add_order(tracker.get_slot("name"), tracker.get_slot("order_number"), create_time, tracker.get_slot("type_of_table"), tracker.get_slot("arrival_time"))
        dispatcher.utter_message(response="utter_show_order", name=tracker.get_slot("name"), create_time=create_time, order_number=tracker.get_slot("order_number"), arrival_time=tracker.get_slot("arrival_time"))
        return [SlotSet(key = "create_time", value = create_time)]

# Create one new random 6-digit order number
class GetOrderNumber(Action):
    def name(self) -> Text:
        return 'action_order_number'
    
    def run(
        self, 
        dispatcher: "CollectingDispatcher", 
        tracker: Tracker, 
        domain: "DomainDict"
    ) -> List[Dict[Text, Any]]:
        order_number = ''.join(random.sample(string.digits,6))
        return [SlotSet(key = "order_number", value = order_number)]

# Select dishes by if special customer chose
class ShowDishesByIfSpecial(Action):
    def name(self) -> Text:
        return 'action_show_dishes_by_if_special'

    def run(
        self, 
        dispatcher: "CollectingDispatcher", 
        tracker: Tracker, domain: "DomainDict"
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_menu_details_if_special", is_special=tracker.get_slot("if_special"))
        dishes = select_dishes_by_if_special(tracker.get_slot("if_special"))
        for dish in dishes:
            dispatcher.utter_message(response="utter_show_dish", dish_name=dish[0], price=dish[1], order_times=dish[2])
            dispatcher.utter_message(image="http://127.0.0.1/menu/"+dish[3]+"/"+dish[0]+".jpg")
        dispatcher.utter_message(text="Which style of dish do you want to view?")
        return []

# Select dishes by style and if special customer chose
class ShowDishesByStyle(Action):
    def name(self) -> Text:
        return 'action_show_dishes_by_style'

    def run(
        self, 
        dispatcher: "CollectingDispatcher", 
        tracker: Tracker, domain: "DomainDict"
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_menu_details_style", is_special=tracker.get_slot("if_special"), style=tracker.get_slot("style"))
        dishes = select_dishes_by_style(tracker.get_slot("style"), tracker.get_slot("if_special"))
        for dish in dishes:
            dispatcher.utter_message(response="utter_show_dish", dish_name=dish[0], price=dish[1], order_times=dish[2])
            dispatcher.utter_message(image="http://127.0.0.1/menu/"+tracker.get_slot("style")+"/"+dish[0]+".jpg")
        dispatcher.utter_message(text="Which flavor of dish do you want to view?")
        return []

# Select dishes by flavor, style and if special customer chose
class ShowDishes(Action):
    def name(self) -> Text:
        return 'action_show_dishes'

    def run(
        self, 
        dispatcher: "CollectingDispatcher", 
        tracker: Tracker, domain: "DomainDict"
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_menu_details", is_special=tracker.get_slot("if_special"), style=tracker.get_slot("style"),
        flavor=tracker.get_slot("flavor"))
        dishes = select_dishes(tracker.get_slot("style"), tracker.get_slot("flavor"), tracker.get_slot("if_special"))
        for dish in dishes:
            dispatcher.utter_message(response="utter_show_dish", dish_name=dish[0], price=dish[1], order_times=dish[2])
            dispatcher.utter_message(image="http://127.0.0.1/menu/"+tracker.get_slot("style")+"/"+dish[0]+".jpg")
        dispatcher.utter_message(text="What can I help you now?")
        return []