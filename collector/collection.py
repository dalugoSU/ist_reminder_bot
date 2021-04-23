class AssignmentCollector:
    from bs4 import BeautifulSoup
    import datetime
    import requests
    import pymsteams
    import smtplib
    from logic import credentials as cd


    def get_class_assignments(self) -> list:
        """
        Gets table from IST Website and creates a 2D list array of due material.
        :return: list - 2D array. [[dueDate[0], dueTime[1], gradeBook[2], points[3], tool[4], whatsDue[5]]]
        """

        response = self.requests.get("http://ist256.com/syllabus/#course-schedule")  # Pulls website IST 256
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
                print("\nNothing due Today!\n")
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
            connection = self.pymsteams.connectorcard(webhook)
            message = ""

            if cmd == 'today':
                due_today = self.get_today()
                if due_today:
                    if card_title:
                        connection.title(card_title)
                    else:
                        connection.title("IMPORTANT - ASSIGNMENT REMINDER!")

                    for element in range(0, len(due_today)):
                        if "Due Date:" in due_today[element]:
                            message += "\n---------------------\n"
                            message += f"\n{due_today[element]}\n"
                        else:
                            message += f"\n{due_today[element]}\n"
                else:
                    message = "Nothing Due Today! "
            elif cmd == 'tomorrow':
                due_tomorrow = self.get_tomorrow()
                if due_tomorrow:
                    if card_title:
                        connection.title(card_title)
                    else:
                        connection.title("IMPORTANT - ASSIGNMENT REMINDER!")

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
        except:
            print("Invalid Webhook")
            return False

    def push_email(self, cmd) -> None:
        """
        function to push assignments due today to emails
        uses information is credentials.py
        :return: none
        """

        server = self.smtplib.SMTP("smtp.gmail.com", 587)
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
            return

        try:
            server.login(self.cd.email_credentials['email_from'], self.cd.email_credentials['password'])
            connection = True
            if connection:
                print("\nSuccessful Established Connection...")

                subject = f"Assignment Reminder! Due {command.capitalize()}!"
                sender = self.cd.email_credentials['email_from']
                recipients = self.cd.email_credentials['email_to']
                message = "Hello IST 256 Student!\nThis is due today:\n"


                for element in range(0, len(date)):
                    message += f"\n{date[element]}"

                message += "\n\nThank you!\n IST 256 - Reminder Bot"

                msg = f"Subject: {subject}\n\n{message.strip('[]')}"

                server.sendmail(msg=msg, from_addr=sender, to_addrs=recipients)
                print(f"Email Sent to students!")

            server.quit()
        except self.smtplib.SMTPAuthenticationError:
            print("\nCould not Establish Connection\nEmail or Password Incorrect")