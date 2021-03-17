from pyfiglet import Figlet
from collection import AssignmentCollector
import requests


def begin_collection(ms_webhook: str = None) -> None:  # ms_webhook = None in case you do not have one saved in main.py

    due_assignment = AssignmentCollector()  # Create instance of Assignment Collector Class
    ms_webhook = ""

    banner = Figlet(font='slant')
    print(banner.renderText("IST 256 Reminders"))
    user_choice = input("Check Today's Assignments [yes or quit to exit]: ")

    while True:
        if user_choice == 'quit':
            break
        if user_choice.lower() == "yes":
            due_today = due_assignment.get_assignment()  # Assignments due "today"
            print("")
            for item in range(0, len(due_today)):
                print(due_today[item])
            push = input("\nWould you like to push assignments to teams [yes or no]: ")
            if push.lower() == 'yes':
                valid = False
                if ms_webhook:
                    while not valid:
                        try:
                            due_assignment.push_to_ms(webhook=ms_webhook)
                            valid = True
                        except requests.exceptions.MissingSchema as e:
                            print("Invalid Webhook!")
                            print(f"{e}\n")
                            break
                else:
                    while not valid:
                        ms_webhook = input("Enter MS Teams webhook: ")
                        if ms_webhook.lower() == "quit":
                            print("See you later!")
                            break
                        try:
                            due_assignment.push_to_ms(webhook=ms_webhook)
                            valid = True
                        except requests.exceptions.MissingSchema as e:
                            print("Invalid Webhook!")
                            print(f"{e}\n")
                break
            else:
                print("See you later!")
                break
        elif user_choice == 'no':
            print("See ya later!")
            break
        else:
            push = input("Would you like to push assignments to teams [yes or no]: ")
            if push.lower() == 'yes':
                valid = False
                if ms_webhook:
                    while not valid:
                        try:
                            due_assignment.push_to_ms(webhook=ms_webhook)
                            valid = True
                        except requests.exceptions.MissingSchema as e:
                            print("Invalid Webhook!")
                            print(f"{e}\n")
                            break
                else:
                    while not valid:
                        ms_webhook = input("Enter MS Teams webhook: ")
                        if ms_webhook.lower() == "quit":
                            print("See you later!")
                            break
                        try:
                            due_assignment.push_to_ms(webhook=ms_webhook)
                            valid = True
                        except requests.exceptions.MissingSchema as e:
                            print("Invalid Webhook!")
                            print(f"{e}\n")
            else:
                print("See you later!")
                break