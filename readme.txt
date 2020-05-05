Here, I'm going to explain briefly how to enable authentifications so that the program can properly
access and edit the google sheets document. The following steps only need need to be done when
running the program for the first time. It is also recommended to read the comments in the python
file itself, but you won't need to.

To run this program, you will need:
- A Python IDE (I use and would recommend Pycyharm Community Edition)
- Access to the spreadsheet you want to edit and privileges to share with others

(The following steps may not line up exactly with what you see in terms of flow for step to step,
 but you should be able to generally follow along)
-First, go to console.developers.google.com and create a new project. Name it whatever you want.
-After creating the project you should be redirected back to the dashboard. Click on ENABLE APIS
 AND SERVICES. Search for Google Drive and enable it. Do the same for Google Sheets.
-Head back to the dashboard. Click on credentials on the left side and create credentials. This
 should be for a service account. When prompted for the API you are using, select Google Sheets.
 When prompted where you will be calling the API from, select Web Server (e.g. node.js). When
 prompted what data will you be accessing, select application data. When asked whether you are
 planning to use the API with App Engine or Compute Engine, select no. Continue to the next part.
-When prompted for a service account name, enter whatever you want. When selecting a role, choose
 Project > Editor. Select JSON for key type. Then create credentials. A JSON file should then be
 downloaded to your computer. Rename this file to creds.json and place it in the VoterLookUp folder.
-Open up that json file (you can use something like a python IDE but I believe notepad should be fine)
 and copy the client email. It should end in something like gserviceaccount.com. Share the spreadsheet
 with that email. Make sure they have enough permission to edit.
-Open up VotingProj2.py using your IDE. You may need to change the line that begins with
 sheet = client.open(' etc etc. It will need to match the title of your spreadsheet exactly. We are
 also assuming only one sheet on the spreadsheet is being used.
-You should now be able to run the program just fine (locate VotingProj2.py on the left, right click
 and choose run). If you are having errors with not not having permissions or something, try
 refreshing your program (in Pycharm right click on the python file or even the entire folder
 on the left side and select reload from disk).



TODO:
-ask about how some counties are written on the sheet
-ask whether to actually update cells, mark them red, both, etc
-what does no political party look like
-check how url changes when website is hanging