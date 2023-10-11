
# Temparature Alert using Fetch.ai's uAgents for TechFest HackAI 2023-24

***NOTE: For some reason, github html viewer is not showing my uploaded images. Please open the `flowchart.jpg` for the Flowchart and refer to `img/` directory for screenshots of the working app in your local machine***

*Showcasing a simple yet powerful implementation of the `uAgents` library.*

# Project Highlights
- Uses **Open Weather** to get Temperature
- Uses **Python Flask** for better GUIs
- fully functional [GPS MAP](https://www.openstreetmap.org/copyright) to drag and drop to a locaton to get temperature of that point **instead of manually typing your coordinates**
- Sends automated **Emails** to the users instead or printing to the console for alerting people using `SMTP library`(***fully functional for real world execution***)
- The Temparature checking logic and core functionality is handled by two agents named `alice` and `bob` from the **uAgents** library.
- The agents check every 60 seconds if temperature fluctuates




## Demo Instructions:
- live demo is hosted at https://hack230469.pythonanywhere.com/
- after entering your information there, drag and drop the pin to the location you would like to monitor.
- check your mail to see if you have entered your mail correctly
- if not recieved any mail:
    - check your spams folder and mark our mail `as not spam`
    - your mail will be shown in the results page, check if spellings are correct
    - if incorrect email, click on `Stop Service` and register again
    - if you still did not get email then run locally, the free resource might be used up and agents might be blocked by the free hosting provider `pythonanywhere`. Moreover the uAgent's documentation was not even sufficient to handle complicated errors. This should surely work locally on your machine.

- the `agents` will check **every 60 seconds** the Temparature of your location using open weather. The API key in the demo server is mine, and hosting is free, so after testing, please consider clicking on the red button `Stop Service` as if the program exceeds the daily free quota, the demo would not work, and *judges would think its a program fault, resulting in my disqualification*




**Code/Logic walkthrough**
-
Basically there are two scripts in the base directory. 
- First you have to run `main.py` that inherits from `app.py`, which handles the front end + client sided logic, then you have to register there first, you will get a mail that you are registered, then you are ready to move to the next point.
- After running `main.py`, you need to run `agent_run.py`, which is our main **agents executor script**(*actual module in agents>module_x.py*) which has the ***uAgents*** and the agents handle the logic, from getting weather data to checking condition and sending mails.

***`app.py`*** docs
-
This is a flask  implementation. The first `/` page has basic form to get user data. To make it more convinient, I implemented a **maps** implementaion where user can drag and drop their location.
***resason?***
- **this project is not just for a competition**, ***it should also meet the complexity of the real world***, in real world, there are many places with identical names, the weather module will get confused and show wrong results*, therefore location pin method was the most stable way of solving this problem, nobody likes to type their coordinates manually!

I have added comments inside `app.py` if you would like to know more about the code. Also i have used `Tailwind CSS` and [Tailblocks](https://tailblocks.cc/) for quick designing of the front end


***`agents.module_x.py`*** docs
-

This file has the core agents, i named them `alice` and `bob` (similar to the docs). 

The uAgents libray holds the core functionality of the program including:
- getting weather data
- checking of temperature fluctuates
- sending email noitification if fluctuation occurs
- repeating the steps every 60 seconds to give realtime data

Let's go through the agents:
- ***bob***: `Bob` is the first agent that runs. *This agent is responsible for getting Temperature data* from dropped pin location, and sends the temperature to the next agent `Alice` using `ctx.send(alice.address, Message(message=temp_string))` for further review and processing. After sending, it waits for 60 seconds, and repeat the process again for real time data. Used `@bob.on_interval(period=AGENT_INTERVAL)` to hold the loop. 

- ***alice***: `alice` gets the temperature data from `bob`, retieves all user data including `emails`, `min/max temperatures` - checks if temperature rises or fall below the given range. If so, then sends email alert to user using `SMTP Library`, with `TLS protocol`, else it saves resources and does nothing.

*refer to code for elaborate explainatoin, extensive code explaination can be found inside the files in comments.*

***`miscellaneous`*** docs:
-
- `agents.mailings.mails.py`: has the `Mail` class that authenticates with google mail and send mail passed into `your_mail_object.send(targetmail, message)` (*line 24 in module*)

- `agents.weather.weather.py`: has the function to get weather data(set to get temperature only)




# Running locally on your machine
If in case the server stops (as it is a free server) and you can't access the hosted demo, follow the instructions to run it:

*Compulsory Requirements for running locally:*
-
- Open weather API key (https://openweathermap.org/api), just sign up and generate an API key, 1000 calls per day is free
- A *gmail* account for sending mail alerts with new app password. **If you will give your normal password, it won't work anymore** as Google changed their privacy policies now. Refer to [this stackoverflow question](https://stackoverflow.com/questions/73136764/python-cannot-send-email-from-gmail-account-with-smtp) to solve the issue, or follow the below steps:
    - go to Google Account settings
    - enable 2 step verification
    - scroll down to create App password(you will get a 16 digit app password, write it down somewhere)




- Then clone this repo
- Place your keys/passwords in `config.py` file of base directory like this:
```python
MASTER_EMAIL = "your google mail"
PASSWORD = "16 digit gmail app passowrd"

AGENT_INTERVAL = 60.0 #60 SECONDS

WEATHER_API_KEY = "your open-weather api key"
DB_PATH = 'agents/db/users.db'


```

- Open *terminal* or *cmd* based on your os on the base directory where the scripts `agent_run.py`, `config.py` lies.
- Run: 
```
pip install -r requirements.txt
``` 
for linux or mac os:
```
pip3 install -r requirements.txt
```

- First run the flask script:
```
python main.py
```
*after runing the script, make sure you register there, give your locations and all, and get the confirmation email as you proceed.*

- after that, start the agents script:
```
python agent_run.py
```
*this will start the agents, and they will start checking for temprature or send mails until this script is stopped. To stop the script to not drain your free API calls, strike `Ctrl+C` while on this console*

*After running `agent_run.py` script, you will get an email if the temperature does not meet our condition,* **every 60 seconds**.

***If you are not getting mail alerts, it's not the program's fault. The temperature falls inside your given range, so it thinks everything is normal and does not send mail***

**Solution?** *To trick the program*, try giving weird temperature range such as 0 to 10 degree and place the pin on mumbai, it will trigger the alert every 60 secods after that unless you close thes script

 
*Code attributions:*
- FetchAi uAgent documentaion
- StackOverflow
- Google Mail/Developer
  
