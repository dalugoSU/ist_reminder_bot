# Functions to use in main program
# TODO: "Add Reminder," capabilities for student UI

import requests
import smtplib
from pyfiglet import Figlet
from collector.collection import AssignmentCollector


# If webhook is saved, this function executes
def webhook_present(ms_webhook: str, due_assignment: object) -> None:
    valid = False
    while not valid:
        try:
            card_title = input("Card Title [enter no for default]: ")
            if card_title.lower() == "no":
                due_assignment.push_to_ms(webhook=ms_webhook)
            else:
                due_assignment.push_to_ms(webhook=ms_webhook, card_title=card_title)
            valid = True
        except requests.exceptions.MissingSchema as e:
            print("Invalid Webhook!")
            print(f"{e}\n")
            break


# Function to handle pushing to MS if webhook is not saved
def webhook_not_present(webhook_obj: object) -> None:
    valid = False
    while not valid:
        ms_webhook = input("Enter MS Teams webhook: ")
        if ms_webhook.lower() == "quit":
            print("See you later!")
            break
        try:
            card_title = input("Card Title [enter no for default]: ")
            if card_title.lower() == "no":
                webhook_obj.push_to_ms(webhook=ms_webhook)
            else:
                webhook_obj.push_to_ms(webhook=ms_webhook, card_title=card_title)
            valid = True
        except requests.exceptions.MissingSchema as e:
            print("Invalid Webhook!")
            print(f"{e}\n")


# If student is using app, capabilities to push to MS etc.. are not used.
def student_ui(student_obj: object) -> bool:
    user_choice: str = input("Check Today's Assignments [yes or quit to exit]: ")
    if user_choice.lower() == "quit":
        print("See you later! ")

    if user_choice.lower() == "yes":
        check = student_obj.print_assignments()
        if check:  # Checks for assignments. If none then no reminder needed
            remind = input("\nWould you like to set a reminder? [yes or no]: ")
            if remind.lower() == 'yes':
                print("\nCreating Timer...")
                student_obj.create_reminder()
                # print("Reminder Has been created :D\nSee you later!")
                return False
            else:
                print("See you later! ")
                return False
    else:
        print("See you later! ")
        return False


# If professor/TA using app, all capabilities unlocked
def prof_ta_ui(p_obj: object, ms_webhook: str =None) -> None:
    user_choice: str = input("Check Today's Assignments [yes or quit to exit]: ")
    while True:
        if user_choice == 'quit':
            break
        if user_choice.lower() == "yes":
            p_obj.print_assignments()  # Function prints HW due "today"

            push = input("\nWould you like to push assignments to teams [yes or no]: ")
            if push.lower() == 'yes':
                if ms_webhook:
                    webhook_present(due_assignment=p_obj, ms_webhook=ms_webhook)
                else:
                    webhook_not_present(webhook_obj=p_obj)
                break
            else:
                break
        elif user_choice == 'no':
            push = input("\nWould you like to push assignments to teams [yes or no]: ")
            if push.lower() == 'yes':
                if ms_webhook:
                    webhook_present(due_assignment=p_obj, ms_webhook=ms_webhook)
                else:
                    webhook_not_present(webhook_obj=p_obj)
                break
            else:
                break
        else:
            push = input("Would you like to push assignments to teams [yes or no]: ")
            if push.lower() == 'yes':
                if ms_webhook:
                    webhook_present(ms_webhook=ms_webhook)
                else:
                    webhook_not_present(webhook_obj=p_obj)
            else:
                break

    email_push = input("Would you like to push reminders to email? [yes or no]: ")

    if email_push.lower() == 'yes':
        try:
            p_obj.push_email()
            print("See you later! ")
        except smtplib.SMTPAuthenticationError:
            print("Email not sent successfully :( \nCheck email credentials!")
    else:
        print("\nSee you later! ")


def begin_collection(ms_webhook: str = None) -> None:  # ms_webhook = None in case you do not have one saved in webhook.py

    due_assignment = AssignmentCollector()  # Create instance of Assignment Collector Class

    banner = Figlet(font='slant')
    print(banner.renderText("IST 256 Reminders"))
    print("Application will gather IST 256 Assignments. For Professors/TAs, you can Push these to MS Teams")
    ui_selection = input("Are you a student or Professor/TA [s: student; p: professor/TA]:  ")

    while True:
        if ui_selection.lower() == "s":
            try:
                student_ui(student_obj=due_assignment)
                break
            except TypeError as e:
                print(e)
                print("Enter yes or quit to exit")
        elif ui_selection.lower() == "p":
            try:
                print("\nIf you have an MS Webhook to use every time, save it in webhook.py")
                prof_ta_ui(p_obj=due_assignment, ms_webhook=ms_webhook)
                break
            except TypeError as e:
                print(e)
                print("Enter yes or quit to exit")
        else:
            print("Invalid command! [s or p]: ")
            ui_selection = input("Are you a student or Professor/TA [s: student; p: professor/TA]:  ")