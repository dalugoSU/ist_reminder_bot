class AssignmentCollector:
    from bs4 import BeautifulSoup
    import datetime
    import requests
    import pymsteams

    def get_class_assignments(self) -> list:
        """
        Gets table from IST Website and creates a 2D list array of due material.
        :return: list - 2D array. [[dueDate[0], dueTime[1], gradeBook[2], points[3], tool[4], whatsDue[5]]]
        """

        response = self.requests.get("http://ist256.com/syllabus/#course-schedule")  # Pulls website
        soup = self.BeautifulSoup(response.content, 'html.parser')  # Parses website and extracts its contents

        assignments_table = soup.find(text='Date Due').find_parent(
            'table')  # Finds the due date table by matching its text with table tag
        assignments = []  # List that will hold lists of assignments

        for table_row in assignments_table.find_all("tr")[1:]:
            assignments.append(
                [text.get_text(strip=True) for text in table_row.find_all("td")])  # Create a list for each row

        return assignments  # Return 2D array of assignments and due dates

    def get_date(self) -> str:
        """
        Function that gets today's date
        :return: return a string with date in format m/d/y
        """
        # Create an instance of datetime
        today = self.datetime.datetime.today()
        date = f"{today.month}/{today.day}/{today.year}"  # Get the date in m/d/y form

        return date

    def get_assignment(self) -> list:
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

    def push_to_ms(self, webhook: str, card_title: str = None):
        """
        function to push today's assignments to an MS teams Team.
        :return: Void/No returns
        """
        connection = self.pymsteams.connectorcard(webhook)
        today_to_do = self.get_assignment()
        message = ""

        if card_title:
            connection.title(card_title)
        else:
            connection.title("IMPORTANT - ASSIGNMENT REMINDER!")

        for element in range(0, len(today_to_do)):
            if "Due Date:" in today_to_do[element]:
                message += "\n---------------------\n"
            else:
                message += f"\n{today_to_do[element]}\n"

        connection.text(message)
        connection.send()

        print("Your Reminder Has Been Posted")

    def push_email(self):
        # TODO: implement this and update main function
        pass

    def push_text(self):
        # TODO: implement this and update main function
        pass