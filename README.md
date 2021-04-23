### Check if you have any Assignments due for IST 256. If you are a TA or Professor you can also push these reminders to your MS Teams and push to emails as well!

Latest update: 4/23/21
updates: Application is now an actual CLI application not linear.

Features:
- Paginator for alldue, duetoday and duetomorrow
- continuous doesn't close after running a command
- removal of unecessary typing; autofill
- command validator
- Push your assignments to MS teams (webhook saved in webhook.py inside logic folder or entered manually in CLI)
- Push your assignments to emails (email credentials (from and to) saved in credentials.py inside logic folder)

Commands:

- help : usage of each command
- duetoday : show assignments due today. q to exit, h for help
- duetomorrow : show assignments due tomorrow. q to exit, h for help
- alldue : show all assignments. q to exit, h for help
- pushms : push [today] or push [tomorrow] push assignments to ms teams
- pushe : pushe [today] or pushe [tomorrow] push assignments to email
- clear : clear screen

ctrl + d to exit

clone this project: git clone https://github.com/dalugoSU/ist_reminder_bot.git

Dependencies needed:
- pypager
- bs4
- datetime
- requests
- pymsteams
- pyfiglet

If you are missing any of these you can install by typing:
pip install -module name-

Command Look:
![Alt text](examples/cli_example.JPG?raw=true "Example Command")

Steps to run program:
- Download zip file and extract folder
- Open folder in command prompt
- Type: python main.py

### For Students:
#### The program will ask you if you want to see today's assignments:
You can check 'today' or 'tomorrow' assignments
- type duetoday -> you will see things due 'today'
- type duetomorrow -> you will see things due 'tomorrow'

### For TAs and Professors:
#### Do you have one webhook you would like to use always?

If you want to use the same webhook everytime in case you would like to push open the webhook.py file and inside logic folder paste in your webhook inside quotes and save. Now everytime you select to pushms to microsoft teams it will use that webhook. Otherwise you will be prompted to input manually.

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
