import pickle
import os.path
import webbrowser
import requests
import pymsteams
import smtplib

from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from bs4 import BeautifulSoup
from logic import credentials as cd
from exceptions.exceptions import InvalidWebhookError


class AssignmentCollector:

    @staticmethod
    def get_class_assignments() -> list:
        """
        Gets table from IST Website and creates a 2D list array of due material.
        :return: list - 2D array. [[dueDate[0], dueTime[1], gradeBook[2], points[3], tool[4], whatsDue[5]]]
        """
        response = requests.get("http://ist256.com/syllabus/#course-schedule")  # Pulls website IST 256
        soup = BeautifulSoup(response.content, 'html.parser')  # Parses website and extracts its contents

        assignments_table = soup.find(text='Date Due').find_parent('table')  # Finds the due date table by matching its text with table tag
        assignments = []  # List that will hold lists of assignments

        for table_row in assignments_table.find_all("tr")[1:]:
            assignments.append([text.get_text(strip=True) for text in table_row.find_all("td")])  # Create a list for each row

        return assignments  # Return 2D array of assignments and due dates

    @staticmethod
    def get_date():
        """
        Function that gets today's date
        :return: return a string with date in format m/d/y
        """
        # Create an instance of datetime
        today = datetime.today()
        date_current = f"{today.month}/{today.day}/{today.year}"  # Get the date in m/d/y form
        date_tomorrow = f"{today.month}/{int(today.day) + 1}/{today.year}"  # Check next day

        return date_current, date_tomorrow

    def get_today(self):
        """
        Get the assignment due today if there is any
        :return: list of today's assignments.
        """

        table_titles = ["Due Date:", "Due Time:", "Grade Book:", "Points:", "Tools:", "What is Due:"]  # Column titles
        table = self.get_class_assignments()
        date_today, dump = self.get_date()

        today_assignment = []

        for row in range(0, len(table)):
            if table[row][0] == date_today:  # If Due Date from table matches today's date
                for row_element in range(0, len(table[row])):  # Go through each element in that assignment's list
                    today_assignment.append(f"{table_titles[row_element]} {table[row][row_element]}")


        return today_assignment

    def get_tomorrow(self):
        """
        Get the assignment due tomorrow if there is any
        :return: list of tomorrow's assignments.
        """

        table_titles = ["Due Date:", "Due Time:", "Grade Book:", "Points:", "Tools:", "What is Due:"]  # Column titles
        table = self.get_class_assignments()
        dump, tomorrow = self.get_date()

        tomorrow_assignment = []

        for row in range(0, len(table)):
            if table[row][0] == tomorrow:  # If Due Date from table matches today's date
                for row_element in range(0, len(table[row])):  # Go through each element in that assignment's list
                    tomorrow_assignment.append(f"{table_titles[row_element]} {table[row][row_element]}")


        return tomorrow_assignment


    def print_assignments(self, cmd):
        """
        function to 'pretty print' assignments due either today or tomorrow
        :return: true if anything is due today or tomorrow, false if nothing due
        """
        if cmd == 'today':
            due_today = self.get_today()  # Assignments due "today"
            if due_today:
                return due_today
            else:
                print("Nothing due Today!")
        elif cmd == 'tomorrow':
            due_tomorrow = self.get_tomorrow()
            if due_tomorrow:
                return due_tomorrow
            else:
                print("Nothing Due tomorrow! ")
        elif cmd == 'all':
            all_due = self.get_class_assignments()
            table_titles = ["Due Date:", "Due Time:", "Grade Book:", "Points:", "Tools:",
                            "What is Due:"]  # Column titles
            all_assignments = []

            for row in range(0, len(all_due)):
                for row_element in range(0, len(all_due[row])):  # Go through each element in that assignment's list
                    all_assignments.append(f"{table_titles[row_element]} {all_due[row][row_element]}")

            return all_assignments
        else:
            print("\nNothing due today or tomorrow!\n")


    def push_to_ms(self, webhook: str, cmd: str, card_title: str = None):
        """
        function to push today's assignments to an MS teams Team.
        :return: Void/No returns
        """
        try:
            connection = pymsteams.connectorcard(webhook)
            if card_title:
                connection.title(card_title)
            else:
                connection.title("IMPORTANT - ASSIGNMENT REMINDER!")
            message = ""

            if cmd == 'today':
                due_today = self.get_today()
                if due_today:
                    for element in range(0, len(due_today)):
                        if "Due Date:" in due_today[element]:
                            message += "\n---------------------\n"
                            message += f"\n{due_today[element]}\n"
                        else:
                            message += f"\n{due_today[element]}\n"
                else:
                    message = "Nothing Due Today!"
            elif cmd == 'tomorrow':
                due_tomorrow = self.get_tomorrow()
                if due_tomorrow:
                    for element in range(0, len(due_tomorrow)):
                        if "Due Date:" in due_tomorrow[element]:
                            message += "\n---------------------\n"
                            message += f"\n{due_tomorrow[element]}\n"
                        else:
                            message += f"\n{due_tomorrow[element]}\n"
                else:
                    message = "Nothing Due Tomorrow! "

            connection.text(message)
            connection.send()

            print("Your Reminder Has Been Posted :D")
        except requests.exceptions.MissingSchema:
            print("Invalid Webhook")
            return False

    def push_email(self, cmd: str):
        """
        function to push assignments due today to emails
        uses information is credentials.py
        :return: none
        """
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        if cmd == 'today':
            command = 'today'
            date = self.get_today()
        elif cmd == 'tomorrow':
            command = 'tomorrow'
            date = self.get_tomorrow()
        else:
            print("Command Not Valid")
            return False

        try:
            server.login(cd.email_credentials['email_from'], cd.email_credentials['password'])
            connection = True
            if connection:
                print("Successful Established Connection...")

                subject = f"Assignment Reminder! Due {command.capitalize()}!"
                sender = cd.email_credentials['email_from']
                recipients = cd.email_credentials['email_to']
                message = "Hello IST 256 Student\n\n"

                if date:
                    message += "This is due today:\n"
                    for element in range(0, len(date)):
                        message += f"\n{date[element]}"
                        if "What is Due:" in date[element]:
                            message += f"\n-------------------"
                else:
                    message += f"Nothing due {command.capitalize()}"

                message += "\n\nThank you!\n IST 256 - Reminder Bot"

                msg = f"Subject: {subject}\n\n{message.strip('[]')}"

                server.sendmail(msg=msg, from_addr=sender, to_addrs=recipients)
                print(f"Email Sent to students!")

            server.quit()
        except smtplib.SMTPAuthenticationError:
            print("\nCould not Establish Connection\nEmail or Password Incorrect")


    def create_event(self):
        """
        create a google calendar event reminder using google calendar API
        :return: none
        """
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/calendar']

        CREDENTIALS_FILE = 'GOOGLE API CREDENTIALS JSON FILE PATH'
        assignments_tomorrow = self.get_tomorrow()
        if not assignments_tomorrow:
            return "Nothing Due Tomorrow, Nothing needed to remind"
        message = ""

        for element in range(0, len(assignments_tomorrow)):
            if "Due Date:" in assignments_tomorrow[element]:
                message += "---------------------\n"
                message += f"{assignments_tomorrow[element]}\n"
            else:
                message += f"{assignments_tomorrow[element]}\n"

        credentials = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        CREDENTIALS_FILE, SCOPES)
                    credentials = flow.run_local_server(port=0)
                except FileNotFoundError:
                    return "Credentials File Path Wrong: Error Line 254: collection.py"

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)

        service = build('calendar', 'v3', credentials=credentials)


        d = datetime.now().date()
        tomorrow = datetime(d.year, d.month, d.day, 12) + timedelta(days=1)
        start = tomorrow.isoformat()
        end = (tomorrow + timedelta(hours=1)).isoformat()

        event_result = service.events().insert(calendarId='primary',
                                               body={
                                                   "summary": f'Assignments Due {datetime(d.year, d.month, d.day) + timedelta(days=1)}',
                                                   "description": f'{message}',
                                                   "start": {"dateTime": start, "timeZone": 'US/Eastern'},
                                                   "end": {"dateTime": end, "timeZone": 'US/Eastern'},
                                               }
                                               ).execute()

        print("created event")
        print("summary: ", event_result['summary'])
        print("Description:", event_result['description'])
        print("starts at: ", event_result['start']['dateTime'])
        print("ends at: ", event_result['end']['dateTime'])

    @staticmethod
    def open_jupyter():
        """
        Open jupyter notebook
        :return: None
        """
        try:
            webbrowser.open("https://jupyterhub.ischool.syr.edu/")
        except:
            return "Something Went wrong... Line 287 open_jupyter()"

    @staticmethod
    def open(command: str):
        """
        Open IST 256 used websites
        :param command: target website
        :return: None
        """
        try:
            if command.lower() == 'blackboard':
                webbrowser.open("https://blackboard.syr.edu")
            elif command.lower() == 'polly':
                webbrowser.open("https://poll.ist256.com")
            elif command.lower() == 'zybook':
                webbrowser.open("https://learn.zybooks.com")
            else:
                return "Command Not Available"
        except:
            return "Error in line 300. open()"

    @staticmethod
    def get_grades():
        """
        Pull grade distribution from IST syllabus website
        :return: None
        """
        response = requests.get("http://ist256.com/syllabus/#grading-scale-for-final-grade")  # Pulls website IST 256
        soup_grades = BeautifulSoup(response.content, 'html.parser')

        grades_table = soup_grades.find(text='Student Achievement').find_parent('table')  # Finds the due date table by matching its text with table tag
        table_titles = ['Student Achievement', 'Total Points Earned', 'Registrar Grade', 'Grade Points']
        grades = []  # List that will hold lists of assignments
        nice_grades = []

        for table_row in grades_table.find_all("tr")[1:]:
            grades.append([text.get_text(strip=True) for text in table_row.find_all("td")])  # Create a list for each row

        for row in range(0, len(grades)):
            for row_element in range(0, len(grades[row])):  # Go through each element in that assignment's list
                nice_grades.append(f"{table_titles[row_element]} {grades[row][row_element]}")

        return nice_grades
