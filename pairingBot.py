import os
import time
import re
import datetime
from Channel import Channel
from slackclient import SlackClient


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

channels = []

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel_id):
    """
        Executes bot command if the command is known
    """
    current_channel = None
    for channel in channels:
        if channel.get_channel_id == channel_id:
            current_channel = channel
            break

    # Default response is help text for the user
    default_response = "Please use `help` to find ways to interact with me"

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith("Hi"):
        response = "Hi, sup?"
    
    elif command.startswith("who created you?"):
        response = "I was created by Neha and Bari from Pathashala-63, cool people right?"
    
    elif command.startswith("help"):
        response = "Here are the commands you can use to interact with me:\n" + "`info` - about me\n" + "`pair info` - information about usage of pairBot for pairing\n"

    elif command.startswith("info"):
        response = "Hello, My name is PairingBot"

    elif command.startswith("pair info"):
        response = "`pair name1, name2, name3, name4….` - sends pair combinations everyday at 9:00 AM\n" + "`pair skip` - skips next day\n" + "`pair display`- displays pairs for current day\n"

    elif command.startswith("start"):
        add_channel(channel_id)
        handle_given_names(command[6:], current_channel)
        response = "Successfully generated all the combinations, please use `pairs` command for more information"

    elif command.startswith("pair skip"):
        current_channel.skip()
        response = "Skipped next notification"

    elif command.startswith("pair display"):
        #display current pair by getting from the database
        response = "This is not yet implimented"
        
    if current_channel == None:
        channel_to_send = channel_id
    else:
        channel_to_send = current_channel.get_channel_id()

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_to_send,
        text=response or default_response
    )

def add_channel(channel_id):
    channels.append(Channel(channel_id))

def send_pairs():
    current_time = str(datetime.datetime.now())[11:19]
    day = datetime.datetime.now().strftime("%A")
    if (current_time == "09:00:00") & (day != "Saturday") & (day != "Sunday"):
        for channel in channels:
            if not(channel.should_skip()):
                #call get combination from database and send for current channel and index
                # handle_command(list_of_all_combinations[INDEX], pathashalaChannel)
                channel.increment_index()
            else:
                channel.reset_skip()

def handle_given_names(names_as_string, channel):
    names_list = names_as_string.split(',')
    #should call algorithm, with the channel. The algorithm should generate pairs and save in a database.
    #It should return false for any error, true for success.

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            send_pairs()
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")