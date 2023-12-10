HUE LIGHT

DESCRIPTION
The Hue Light is controlled via SMS. Our python program receives the SMS message from Twilio, Checks a redis database to verify whether or not the specified color is in the database. If it is, it then interacts with the light and then uses requests to send an SMS message back to the user. When a color is used to change the light it is recorded and then displayed on a webpage that shows color statistics.

SET UP
1. clone the repo - https://github.com/cs298-398f23/HueLightFinalProject-actual-.git
   
TWILIO
2. Go to https://www.twilio.com/login and create a free developer account.
3. Once made you will get a free phone number, this is used to set up the API.
4. You will need 3 things to connect the twilio api to your program, Your Twilio phone number, account sid, and auth token.
5. In the .gitIgnore file there will be a line that says .env you need to create this .env file and put your twilio cridentials in it.

NGROK
1. Go to https://ngrok.com/download and download for Mac OS X
2. In a new terminal cd into your Downloads.
3. Run the command: spctl --add ngrok
4. Run the ./ngrok http 8000
5. A little window should pop up and you should say a line that says "fowarding" followed by a https link.
6. Copy this link and go to yur twilio developer dashboard.
7. Click “# Phone Numbers” on the left, then “Manage”, then “Active numbers”, and finally your Twilio phone number.
8. Scroll down the page until you get to the Messaging section
9. On the line for A MESSAGE COMES IN, make sureWebhook is selected and then paste the URL you copied from ngrok into the text box
10. In the drop box to the right, select HTTP GET instead of HTTP POST.
11. Click the blue Save button at the bottom of the page.
    
PYTHON PROGRAM
1. In your cloned folder create a virtual enviorment
2. Run the commans:
3. Python3 -m venv .venv
4. Source .venv/bin/activate
5. pip3 install -r requirements.txt

REDIS
The redis database needs to be ran one time so that the colors are put in the database.
1. Download redis - https://redis.io
2. Open a terminal and cd into your Downloads folder
3. run the command <redis-server>, this will allow you to open a connection to the server where you can run your database.
4. In a new terminal cd into the cloned folder, and run the create_redis.py file.
5. The database should now be created

RUN THE PROGRAM
1. Now that everything is set up we can run the prgram
2. Run the send.py script: Python3 send.py
3. Send a message from your phone to your twilio phone number and if the color is in the database it will change!




