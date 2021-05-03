### Check if you have any Assignments due for IST 256. If you are a TA or Professor you can also push these reminders to your MS Teams and push to emails as well!

### Set Up:
- Clone/download project: git clone https://github.com/dalugoSU/ist_reminder_bot.git
- Type: python installation.py (This will install all required packages to set up CLI)
- Type: python main.py (To run program)
- Enjoy :D

Optional:
- If you have a webhook for MS Teams: go in webhook.py (inside the logic folder) and paste your webhook in a string to the variable webhook currently set to None
- If you have credentiasl for email bot: go in credentials.py (inside the logic folder) and paste your email credentials and recipients in the defined dict
- If you have credentials for google calendar API: go in creds.json and delete current code and paste your credentials, then go in collection.py (inside collector folder) and go to line 225 and paste your creds.json file path.

Latest update: 5/1/21

updates: 

5/1 - installation.py to set up CLI (installs required packages), bug fixes, code refactoring
4/21 - New commands (openjupyter, open, and grades); bug fixes

Commands:

- help : usage of each command
- duetoday : show assignments due today. q to exit, h for help
- duetomorrow : show assignments due tomorrow. q to exit, h for help
- alldue : show all assignments. q to exit, h for help
- pushms : push [today] or push [tomorrow] push assignments to ms teams
- pushe : pushe [today] or pushe [tomorrow] push assignments to email
- setreminder : add tomorrow's homework reminder to google calendar (Needs API key)
- openjupyter : open jupyterHub in web browser
- open : open [blackboard] [polly] [zybook] websites
- grades : display grading scale
- clear : clear screen
- ctrl + d to exit

Features:
- Paginator for alldue, duetoday, grades and duetomorrow
- continuous doesn't close after running a command
- removal of unecessary typing; autofill
- command validator
- Push your assignments to MS teams (webhook saved in webhook.py inside logic folder or entered manually in CLI)
- Push your assignments to emails (email credentials (from and to) saved in credentials.py inside logic folder)
- Set reminders on your google calendar
- open jupyter, blackboard, polly and zybook directly from CLI


Command Look:

![Alt text](examples/cli_example.JPG?raw=true "Example Command")

Steps to run program:
- Download zip file and extract folder
- Open folder in command prompt
- Type: python main.py

### Setting up Google's Calendar API
- Create a project in Google Developer Console
- Add your email as an user
- Get your API Key and Credentials
- Download credentials json file, rename to something easier such as 'creds.json'
- place that file in project folder and add path inside create_event() function inside the AssignmentCollector class

### For Students:
#### The program will ask you if you want to see today's assignments:
You can check 'today' or 'tomorrow' assignments
- type duetoday -> you will see things due 'today'
- type duetomorrow -> you will see things due 'tomorrow'

#### Create A Google Calendar Reminder
You can create a reminder by typing: setreminder
This functionality uses google's calendar API. You need credentials.
Refer Above on how to set up

Example Google Reminder:

![Alt text](examples/calendar_example.JPG?raw=true "Example Calendar")

### For TAs and Professors:
#### Do you have one webhook you would like to use always?

If you want to use the same webhook everytime in case you would like to push open the webhook.py file and inside logic folder paste in your webhook inside quotes and save. Now everytime you select to pushms to microsoft teams it will use that webhook. Otherwise you will be prompted to input manually.

### how to push assignments:
- type: pushms today -> this will push 'today' assignments to ms teams
- type: pushms tomorrow -> this will push 'tomorrow' assignments to ms teams

Example of reminder card pushed to Microsoft Teams after pushing reminder:
![Alt text](examples/card_example.jpg?raw=true "Example Card")

### How to get a webhook:
1) Go to the teams you would like to push these assignments to
2) At the top right you will see three dots ***
3) Click the three dots and click connectors
4) In the new Screen add/configure "incoming connectors"
5) Once confifured, you will see a link at the bottom of the box, copy this link and save it. That is your webhook for that MS Teams

#### Send Reminder as an Email!

You may also send your reminder by email to all of your students at once!

Example of email sent by bot:

![Alt text](examples/email_example.JPG?raw=true "Example email")

### how to push assignments:
- type: pushe today -> this will push 'today' assignments to email recipients saved in file
- type: pushe tomorrow -> this will push 'tomorrow' assignments to email recipients saved in file

### How to set emailing up:
1) Go to your Google Account.
2) Select Security.
3) Under "Signing in to Google," select App Passwords. You may need to sign in. If you don’t have this option, it might be because:
- 2-Step Verification is not set up for your account.
- 2-Step Verification is only set up for security keys.
- Your account is through work, school, or other organization.
- You turned on Advanced Protection.
4) At the bottom, choose Select app and choose the app you using and then Select device and choose the device you’re using and then Generate.
5) Follow the instructions to enter the App Password. The App Password is the 16-character code in the yellow bar on your device.
6) Tap Done.

If you are all Professors/TAs for IST 256 you can all share one single bot email to use, or you may use your personal emails.

In credentials.py:
- Save bot's email
- Save bot email password
- Save student's emails (You may write a script to automatically clean this up for you)

#### Feel free to play around with the code and change it!
