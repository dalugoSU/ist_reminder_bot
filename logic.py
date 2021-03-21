import requests

global due_assignment


# Quick homework print function
def print_hw(due_assignment):
    due_today = due_assignment.get_assignment()  # Assignments due "today"
    print("")

    for item in range(0, len(due_today)):
        print(due_today[item])


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
def webhook_not_present(due_assignment):
    valid = False
    while not valid:
        ms_webhook = input("Enter MS Teams webhook: ")
        if ms_webhook.lower() == "quit":
            print("See you later!")
            break
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


# If student is using app, capabilities to push to MS etc.. are not used.
def student_ui(user_choice, due_assignment):
    if user_choice.lower() == "yes":
        print_hw(due_assignment)
        print("\nSee you later! ")
    else:
        print("See you later! ")


# If professor/TA using app, all capabilities unlocked
def prof_ta_ui(user_choice, due_assignment, ms_webhook=None):
    while True:
        if user_choice == 'quit':
            break
        if user_choice.lower() == "yes":
            print_hw(due_assignment)  # Function prints HW due "today"

            push = input("\nWould you like to push assignments to teams [yes or no]: ")
            if push.lower() == 'yes':
                if ms_webhook:
                    webhook_present(due_assignment=due_assignment, ms_webhook=ms_webhook)
                else:
                    webhook_not_present(due_assignment=due_assignment)
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
                if ms_webhook:
                    webhook_present(ms_webhook=ms_webhook)
                else:
                    webhook_not_present(due_assignment=due_assignment)
            else:
                print("See you later!")
                break