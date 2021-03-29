# Functions to use in main program
# TODO: "Add Reminder," capabilities for student UI

import requests
import smtplib

global due_assignment


# If webhook is saved, this function executes
def webhook_present(ms_webhook, due_assignment):
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
def webhook_not_present(webhook_obj):
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
        if check: # Checks for assignments. If none then no reminder needed
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
def prof_ta_ui(p_obj, ms_webhook=None):
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