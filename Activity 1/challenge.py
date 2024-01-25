
# Importing necessary libraries

from webex_bot.webex_bot import WebexBot
from webex_bot.webex_bot import Command
from adaptivecardbuilder import *
from webex_bot.models.response import response_from_adaptive_card, Response
import requests
import json
import asyncio

BOTEMAIL = ""# BOTEMAIL = "" # Your bot's email <bot_name>@webex.bot
TEAMSTOKEN = "" # Your bot's token
BOTAPPNAME = "" # Your bot's name
TETOKEN = "" # The ThousandEyes OAuth token

bot = WebexBot(teams_bot_token=TEAMSTOKEN,
               approved_rooms=['<your room ID (Ctrl + Shift + K)>'],
               bot_name=BOTAPPNAME,
               include_demo_commands=True)


class ListAgents(Command):
    base_url = "https://api.thousandeyes.com/v7/agents"

    query_string = "?agentTypes=ENTERPRISE"

    # Defining the Headers for the API request to ThousandEyes

    TE_headers = {
        "Authorization": "Bearer " + TETOKEN,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # The command_keyword is what will trigger the execute()
    # function when the command button will be pressed by a user
    # in the bot

    # The help_message is the command name

    def __init__(self):
        super().__init__(
            command_keyword="list",
            help_message="List all Enterprise ThousandEyesAgents")

    # The logic executed when the user gives this command to the bot

    def execute(self, message, attachment_actions, activity):
        # The API call to the ThousandEyes API

        response = requests.get(url=self.base_url + self.query_string, headers=self.TE_headers)

        # Convert API response to JSON

        agents = json.loads(response.text)

        # Printing Agents to the terminal for display and debugging purposes
        # This DOES NOT return the list of agents to the bot.
        print(agents)
        card = AdaptiveCard()

        # The Adaptive card header
        card.body.append(
            TextBlock(size="Medium", weight="Bolder", text="Your ThousandEyes agents are listed below", wrap=True))

        # For each agent in the API response, add in the adaptive card TextBlock() elements which contain
        # the Agent name and IP address. Then, add a separator line to separate the Agent information.

        for agent in agents["agents"]:
            print(agent)
            card = card.add([
                TextBlock(text=f"Agent Name: {agent['agentName']}", wrap=True, spacing="ExtraLarge"),
                TextBlock(text=f"Agent ID: {agent['agentId']}", wrap=True, spacing="ExtraLarge"),
                TextBlock(text=f"Agent IP: {agent['ipAddresses'][0]}", wrap=True, spacing="ExtraLarge"),
                TextBlock(text=f"Agent State: {agent['agentState']}", wrap=True, spacing="ExtraLarge"),
                TextBlock(text="-----------------------------", wrap=True, spacing="Large")
            ]
            )

        # Initialising a Webex Bot Response object
        bot_response = Response()

        # Convert JSON string data from card to Python dictionary

        card_data = json.loads(asyncio.run(card.to_json()))

        # Adding some additional data to the card payload necessary for the
        # card to be rendered successfully by the bot
        card_payload = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": card_data,
        }
        # The bot response text

        bot_response.text = "The bot's response:"

        # Adding card to bot response attachments

        bot_response.attachments = card_payload

        # Return the bot response to be rendered by the bot

        return bot_response


bot.add_command(ListAgents())
bot.run()
