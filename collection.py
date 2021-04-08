class AssignmentCollector:
    from bs4 import BeautifulSoup
    import datetime
    import requests
    import pymsteams
    import smtplib
    import time
    from win10toast import ToastNotifier
    import credentials as cd

    def get_class_assignments(self) -> list:
        """
        Gets table from IST Website and creates a 2D list array of due material.
        :return: list - 2D array. [[dueDate[0], dueTime[1], gradeBook[2], points[3], tool[4], whatsDue[5]]]
        """

        response = self.requests.get("http://ist256.com/syllabus/#course-schedule")  # Pulls website IST 256
        soup = self.BeautifulSoup(response.content, 'html.parser')  # Parses website and extracts its contents

        assignments_table = soup.find(text='Date Due').find_parent(
            'table')  # Finds the due date table by matching its text with table tag
        assignments = []  # List that will hold lists of assignments

        for table_row in assignments_table.find_all("tr")[1:]:
            assignments.append(
                [text.get_text(strip=True) for text in table_row.find_all("td")])  # Create a list for each row

        return assignments  # Return 2D array of assignments and due dates

    def get_date(self) -> tuple:
        """
        Function that gets today's date
        :return: return a string with date in format m/d/y
        """
        # Create an instance of datetime
        today = self.datetime.datetime.today()
        date_current = f"{today.month}/{today.day}/{today.year}"  # Get the date in m/d/y form
        date_tomorrow = f"{today.month}/{int(today.day) + 1}/{today.year}"  # Check next day

        return date_current, date_tomorrow

    def get_assignment(self) -> tuple:
        """
        Get the assignment due today if there is any
        :return: list of today's assignments.
        """

        table_titles = ["Due Date:", "Due Time:", "Grade Book:", "Points:", "Tools:", "What is Due:"]  # Column titles
        table = self.get_class_assignments()
        date_today, date_tomorrow = self.get_date()

        today_assignment = []
        tomorrow_assignment = []

        for row in range(0, len(table)):
            if table[row][0] == date_today:  # If Due Date from table matches today's date
                for row_element in range(0, len(table[row])):  # Go through each element in that assignment's list
                    today_assignment.append(f"{table_titles[row_element]} {table[row][row_element]}")

        for row in range(0, len(table)):
            if table[row][0] == date_tomorrow:  # If Due Date from table matches today's date
                for row_element in range(0, len(table[row])):  # Go through each element in that assignment's list
                    tomorrow_assignment.append(f"{table_titles[row_element]} {table[row][row_element]}")

        if not today_assignment and not tomorrow_assignment:
            return [], []  # There are no assignments for "today"
        elif not today_assignment and tomorrow_assignment:
            return [], tomorrow_assignment
        elif today_assignment and not tomorrow_assignment:
            return today_assignment, []
        else:
            return today_assignment, tomorrow_assignment

    def print_assignments(self) -> bool:

        due_today, due_tomorrow = self.get_assignment()  # Assignments due "today"

        if due_today or due_tomorrow:
            if due_today:
                print(f"\n-----Due today-----")

                for item in range(0, len(due_today)):
                    print(due_today[item])
                print("")
            else:
                print("Nothing due Today!\n")

            if due_tomorrow:
                print(f"\n-----Due Tomorrow:-----")
                for item in range(0, len(due_tomorrow)):
                    print(due_tomorrow[item])
            else:
                print("Nothing Due tomorrow! ")
            return True
        else:
            print("\nNothing due today or tomorrow!\n")
            return False

    def create_reminder(self) -> None: # BETA IDEA - NOT PROPER

        assignment_reminder, dump = self.get_assignment()

        year = assignment_reminder[0].split(" ")[2].split("/")[2]
        month = assignment_reminder[0].split(" ")[2].split("/")[0]
        day = assignment_reminder[0].split(" ")[2].split("/")[1]
        hour = assignment_reminder[1].split(" ")[2].split(":")[0]

        message = ""

        for element in range(0, len(assignment_reminder)):
            message += f"\n{assignment_reminder[element]}\n"

        right_now = self.datetime.datetime.now()
        future = self.datetime.datetime(year=int(year),
                                        month=int(month),
                                        day=int(day),
                                        hour=int(hour))

        reminder_in = abs((right_now - future).total_seconds())

        notification = self.ToastNotifier()
        print("Created Reminder! See Yah later! ")
        self.time.sleep(reminder_in)
        notification.show_toast(title="IST 256 Assignment Reminder :D",
                                msg=message,
                                duration=5)

    def push_to_ms(self, webhook: str, card_title: str = None) -> None:
        """
        function to push today's assignments to an MS teams Team.
        :return: Void/No returns
        """
        connection = self.pymsteams.connectorcard(webhook)
        due_today, due_tomorrow = self.get_assignment()
        message = ""

        if due_today:
            if card_title:
                connection.title(card_title)
            else:
                connection.title("IMPORTANT - ASSIGNMENT REMINDER!")

            for element in range(0, len(due_today)):
                if "Due Date:" in due_today[element]:
                    message += "\n---------------------\n"
                else:
                    message += f"\n{due_today[element]}\n"
        else:
            message = "Nothing Due Today! "

        connection.text(message)
        connection.send()

        print("Your Reminder Has Been Posted :D")

    def push_email(self) -> None:

        server = self.smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        try:
            server.login(self.cd.email_credentials['email_from'], self.cd.email_credentials['password'])
            connection = True
            if connection:
                print("\nSuccessful Established Connection...")

                subject = "Assignment Reminder! Due Today!"
                sender = self.cd.email_credentials['email_from']
                recipients = self.cd.email_credentials['email_to']
                message = "Hello IST 256 Student!\nThis is due today:\n"

                today, tomorrow = self.get_assignment()

                for element in range(0, len(today)):
                    message += f"\n{today[element]}"

                message += "\n\nThank you!\n IST 256 - Reminder Bot"

                msg = f"Subject: {subject}\n\n{message.strip('[]')}"

                server.sendmail(msg=msg, from_addr=sender, to_addrs=recipients)
                print(f"Email Sent to students!")

            server.quit()
        except self.smtplib.SMTPAuthenticationError:
            print("\nCould not Establish Connection\nEmail or Password Incorrect")