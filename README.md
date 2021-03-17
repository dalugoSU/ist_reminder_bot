### Check if you have any Assignments due for IST 256. If you are a TA or Professor you can also push these reminders to your MS Teams!

Dependencies needed:
- bs4
- datetime
- requests
- pymsteams
- pyfiglet

If you are missing any of these you can install by typing:
pip install -module name-


Steps to run program:
- Download zip file and extract folder
- Open folder in command prompt
- Type: python main.py

### For Students:
#### The program will ask you if you want to see today's assignments:
When you select:
-yes
  * Assignments due "today" will be displayed. If there are no assignments -1 will be returned
  * You will be prompted if you want to push to Microsoft Teams:
    - You should type in 'no'


### For TAs and Professors:
#### Do you have one webhook you would like to use always?

If you want to use the same webhook everytime in case you would like to push open the main.py file and inside begin_collection() paste in your webhook inside quotes and save. Now everytime you select to push to microsoft teams it will use that webhook.

Example of reminder card pushed to Microsoft Teams after pushing reminder:
![Alt text](card_example.jpg?raw=true "Example Card")

### How to get a webhook:
1) Go to the teams you would like to push these assignments to
2) At the top right you will see three dots ***
3) Click the three dots and click connectors
4) In the new Screen add/configure "incoming connectors"
5) Once confifured, you will see a link at the bottom of the box, copy this link and save it. That is your webhook for that MS Teams



#### Feel free to play around with the code and change it!
