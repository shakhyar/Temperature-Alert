""""
CORE MODULE FOR CONNECTING DATABASE, WEATHER FORCAST AND EMAIL SENDING MODULE
USING FETCH.AI'S UAGENTS LIBRARY. REFER TO COMMENTS AND DOCCUMENTATIONS FOR DOUBTS.
[use a good IDE theme to read clearly]
"""
"""--------------------------------------------------------IMPORTS-----------------------------------------------------------------------"""
from uagents import Agent, Bureau, Context, Model

# the config file of the base directory that has all important global variables including api keys
from config import MASTER_EMAIL, PASSWORD, AGENT_INTERVAL

# custom libraries that includes the databse, weather and mailing module 
from agents.db.users import Users
from agents.weather.weather import fetch_weather
from agents.mailing.mails import Mail
"""--------------------------------------------------------------------------------------------------------------------------------------"""




"""--------------------------------------------------------CLASS AND OBJECTS--------------------------------------------------------------"""
# Note: some basic codes were taken from official doc as no elaborate explaination was provided, so some code might look identical
# initialising Message class of uagents
class Message(Model):
    message: str

# setting up agents alice and bob
alice = Agent(name="alice", seed="alice recovery phrase")
bob = Agent(name="bob", seed="bob recovery phrase")

# our mailing object that send mails and database object that has registered user data
mail = Mail(MASTER_EMAIL, PASSWORD)
db_ = Users()
"""--------------------------------------------------------------------------------------------------------------------------------------"""





"""---------------------------------------------- AGENT BOB --------------------------------------------------------------------------"""
@bob.on_interval(period=AGENT_INTERVAL) # default interval is 60 seconds
async def data_cleaner_and_sender(ctx: Context):

    # empty list to erase previously cached data    
    emails_and_names = []
    ranges = []
    coordinates = db_.get_coordinates()

    temp_raw = []
    
    for sublist in coordinates:
        weather_data = fetch_weather(sublist[0], sublist[1])
        print(f"coord{sublist}, temp{weather_data}")
        # trying to make a csv/string type of gathered temperature data of multiple 
        # users instead of list, so to make it easy to pass to other agents later
        # also the databse is ordered, so temperatures and users won't mix up
        temp_raw.append(str(weather_data))

    #print(temp_raw)

    temp_string = ",".join(temp_raw)

        
    print(f"""[BOB INFO] sending temperature string as "{temp_string}" to ALICE""")

    # sending parsed temperature to alice agent
    await ctx.send(alice.address, Message(message=temp_string))
"""--------------------------------------------------------------------------------------------------------------------------------------"""




"""------------------------------------------------------AGENT ALICE---------------------------------------------------------------------"""
@alice.on_message(model=Message)
async def alice_message_handler(ctx: Context, sender: str, msg: Message):
    
    print(f"""[ALICE INFO] recieved temperature string as "{msg.message}" """)
    
    temp_ = str(msg.message).split(',') #converting back to list
    

    # get user entered temparature ranges and their emails and names as to make the noitification look a bit nicer
    ranges_ = db_.get_ranges()
    email_and_names_ = db_.get_emails()
    print(f"[ALICE INFO] All Temperature ranges: {ranges_}")


    # iterate through the lists having the following shape
    #           [[x@email.com, name_x], 
    #                 ......
    #                 ......
    #           [y@email.com, name_y]]
    for range__, email_and_name, temperature in zip(ranges_, email_and_names_, temp_):
        temperature = float(temperature)

        # below in range__ list, 0th index is the max temperature and 1th index is the min temp.
        # check if temperature lies in range
        if temperature<= range__[0] and temperature > range__[1]:
            # won't send any email if temperature is normal
            print(f"optimal temperature for {email_and_name[1]}")
            

        else:
            # else send email to alert the user
            print(f"sending mail to {email_and_name[0]} as current temperature {temperature} does not lie between the range {range__[1]} to {range__[0]}")
            # send mail from agent ALICE using smtp
            mail.send(email_and_name[0], f"Temperature alert! Dear {email_and_name[1]}, the current Temperature of your given location is {temperature}, and doesn't lie between your favourable range!")
            print(f"email sent for {email_and_name[1]}")
"""--------------------------------------------------------------------------------------------------------------------------------------"""

bureau = Bureau()
bureau.add(alice)
bureau.add(bob)
 
if __name__ == "__main__":
    bureau.run()