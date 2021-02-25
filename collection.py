class AssignmentCollector:
    from bs4 import BeautifulSoup
    import datetime
    import requests
    import pymsteams

    def get_class_assignments(self):
        """
        Gets table from IST Website and creates a 2D list array of due material.
        :return: list - 2D array. [[dueDate[0], dueTime[1], gradeBook[2], points[3], tool[4], whatsDue[5]]]
        """

        response = self.requests.get("http://ist256.com/syllabus/#course-schedule")  # Pulls website
        soup = self.BeautifulSoup(response.content, 'html.parser')  # Parses website and extracts its contents

        assignments_table = soup.find(text='Date Due').find_parent('table')  # Finds the due date table by matching its text with table tag
        assignments = []  # List that will hold lists of assignments

        for table_row in assignments_table.find_all("tr")[1:]:
            assignments.append([text.get_text(strip=True) for text in table_row.find_all("td")])  # Create a list for each row

        return assignments  # Return 2D array of assignments and due dates

    def get_date(self):
        """
        Function that gets today's date
        :return: return a string with date in format m/d/y
        """
        # Create an instance of datetime
        today = self.datetime.datetime.today()
        date = f"{today.month}/{today.day}/{today.year}"  # Get the date in m/d/y form

        return date

    def get_assignment(self):
        """
        Get the assignment due today if there is any
        :return: list of today's assignments.
        """

        table_titles = ["Due Date:", "Due Time:", "Grade Book:", "Points:", "Tools:", "What is Due:"]  # Column titles
        table = self.get_class_assignments()
        date = self.get_date()
        today_assignment = []

        for row in range(0, len(table)):
            if table[row][0] == date:  # If Due Date from table matches today's date
                for row_element in range(0, len(table[row])):  # Go through each element in that assignment's list
                    today_assignment.append(f"{table_titles[row_element]} {table[row][row_element]}")

        if not today_assignment:
            return ['No Assignments']  # There are no assignments for "today"
        else:
            return today_assignment

    def push_to_ms(self, webhook):
        """
        function to push today's assignments to an MS teams Team.
        :return: Void/No returns
        """
        connection = self.pymsteams.connectorcard(webhook)
        today_to_do = self.get_assignment()
        message = ""

        connection.title("IMPORTANT - ASSIGNMENT REMINDER!")

        for element in range(0, len(today_to_do)):
            if "Due Date:" in today_to_do[element]:
                message += "\n---------------------\n"
            else:
                message += f"\n{today_to_do[element]}\n"

        connection.text(message)
        connection.send()

        print("Your Reminder Has Been Posted")


def begin_collection(ms_webhook=None): # ms_webhook = None in case you do not have one saved in main.py
    due_assignment = AssignmentCollector() # Create instance of Assignment Collector Class
    user_choice = input("Check Today's Assignments [yes, no or quit to exit]: ")

    while user_choice != 'quit':
        if user_choice.lower() == "yes":
            due_today = due_assignment.get_assignment() # Assignments due "today"
            print("")
            for item in range(0, len(due_today)):
                print(due_today[item])
            push = input("\nWould you like to push assignments to teams [yes or no]: ")
            if push.lower() == 'yes':
                valid = False
                if ms_webhook:
                    while not valid or ms_webhook.lower() == 'quit':
                        try:
                            due_assignment.push_to_ms(webhook=ms_webhook)
                            valid = True
                        except:
                            print("Invalid Webhook!")
                            break
                else:
                    while not valid or ms_webhook.lower() == 'quit':
                        ms_webhook = input("Enter MS Teams webhook: ")
                        try:
                            due_assignment.push_to_ms(webhook=ms_webhook)
                            valid = True
                        except:
                            print("Invalid Webhook!")
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
                while not valid:
                    ms_webhook = input("Enter MS Teams webhook: ")
                    if ms_webhook.lower() == "quit":
                        break
                    try:
                        due_assignment.push_to_ms(webhook=ms_webhook)
                        valid = True
                    except:
                        print("Invalid Webhook!")
                break
            else:
                print("See you later!")
                break
