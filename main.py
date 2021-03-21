from logic import student_ui, prof_ta_ui
from pyfiglet import Figlet
from collection import AssignmentCollector
import webhook as wh

global due_assignment

if __name__ == "__main__":
    def begin_collection(ms_webhook: str = None) -> None:  # ms_webhook = None in case you do not have one saved in webhook.py
        global due_assignment

        due_assignment = AssignmentCollector()  # Create instance of Assignment Collector Class

        banner = Figlet(font='slant')
        print(banner.renderText("IST 256 Reminders"))
        print("Application will gather IST 256 Assignments. For Professors/TAs, you can Push these to MS Teams")
        ui_selection = input("Are you a student or Professor/TA [s: student; p: professor/TA]:  ")

        while True:
            if ui_selection.lower() == "s":
                try:
                    user_choice: str = input("Check Today's Assignments [yes or quit to exit]: ")
                    student_ui(user_choice=user_choice, due_assignment=due_assignment)
                    break
                except TypeError:
                    print("Enter yes or quit to exit")
            elif ui_selection.lower() == "p":
                try:
                    print("\nIf you have an MS Webhook to use every time, save it in webhook.py")
                    user_choice: str = input("Check Today's Assignments [yes or quit to exit]: ")
                    prof_ta_ui(user_choice=user_choice, due_assignment=due_assignment, ms_webhook=ms_webhook)
                    break
                except TypeError:
                    print("Enter yes or quit to exit")
            else:
                print("Invalid command! [s or p]: ")
                ui_selection = input("Are you a student or Professor/TA [s: student; p: professor/TA]:  ")

    begin_collection(ms_webhook=wh.WEBHOOK) # Go to webhook.py to save your webhook