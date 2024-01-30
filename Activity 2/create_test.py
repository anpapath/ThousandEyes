from webex_bot.webex_bot import WebexBot
from webex_bot.webex_bot import Command
from adaptivecardbuilder import *
from webex_bot.models.response import response_from_adaptive_card, Response
import requests
import json
import asyncio

BOTEMAIL = "" # Your bot's email <bot_name>@webex.bot
TEAMSTOKEN = "" # Your bot's token
BOTAPPNAME = "" # Your bot's name
TETOKEN = "" # The ThousandEyes OAuth token

bot = WebexBot(teams_bot_token=TEAMSTOKEN,
               bot_name=BOTAPPNAME,
               include_demo_commands=True)


# define ListAgents Command
class ListAgents(Command):
    base_url = "https://api.thousandeyes.com/v7/"

    query_string = "?agentTypes=ENTERPRISE"
    TE_headers = {
        "Authorization": "Bearer " + TETOKEN,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    def __init__(self):
        super().__init__(
            command_keyword="list",
            help_message="List all Enterprise ThousandEyesAgents")

    def execute(self, message, attachment_actions, activity):
        response = requests.get(url=self.base_url + "agents" + self.query_string, headers=self.TE_headers)
        agents = json.loads(response.text)
        print(agents)
        card = AdaptiveCard()
        card.body.append(
            TextBlock(size="Medium", weight="Bolder", text="Your ThousandEyes agents are listed below", wrap=True))
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
        card_data = json.loads(asyncio.run(card.to_json()))
        card_payload = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": card_data,
        }
        response = Response()
        print(card_payload)
        # Fallback text
        response.text = "Test Card"
        # Attachments being sent to user
        response.attachments = card_payload
        return response


# Add new commands for the bot to listen out for.

bot.add_command(ListAgents())

# define CreateTest Command

with open("./input_card.json") as card:
    INPUTCARD = json.load(card)


class CreateTest(Command):
    def __init__(self):
        super().__init__(
            command_keyword="createtest",
            help_message="Create a ThousandEyes Test with parameters",
            card=INPUTCARD)

    def pre_execute(self, message, attachment_actions, activity):
        pass

    def execute(self, message, attachment_actions, activity):
        success = False
        output_card = AdaptiveCard()
        interval = attachment_actions.inputs["interval"]
        source_agent = attachment_actions.inputs["said"]
        dest_agent = attachment_actions.inputs["taid"]
        test_name = attachment_actions.inputs["test_name"]
        proto = attachment_actions.inputs["proto"]
        url = "https://api.thousandeyes.com/v7/tests/agent-to-agent/new"

        TE_headers = {
            "Authorization": "Bearer " + TETOKEN,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = json.dumps({
            "interval": interval,
            "agents": [
                {
                    "agentId": source_agent
                }
            ],
            "testName": test_name,
            "protocol": proto,
            "targetAgentId": dest_agent
        })
        test_create = requests.post(url=url, data=payload, headers=TE_headers)
        status_code = test_create.status_code
        test_data = test_create.json()
        print(test_data)
        if status_code == 201:
            success = True
        if success:
            output_card.add(
                [
                    TextBlock(text=f"The test ' {test_name} ' was created successfully!", size="ExtraLarge",
                              weight="Bolder", wrap=True),
                    ColumnSet(),
                    Column(width="stretch"),
                        TextBlock(text=f"Interval: {interval}", wrap=True, weight="Bolder"),
                        TextBlock(text=f"Source Agent: {source_agent}", wrap=True, weight="Bolder"),
                        TextBlock(text=f"Target Agent: {dest_agent}", wrap=True, weight="Bolder"),
                        TextBlock(text=f"Protocol: {proto}", wrap=True, weight="Bolder"),
                ]
            )
        else:
            error_message = test_data["errorMessage"]
            output_card.add(
                [
                    TextBlock(text=f"There was an error while trying to create the test ' {test_name} '.", wrap=True,
                              size="ExtraLarge", weight="Bolder"),
                    ColumnSet(),
                    Column(width="stretch"),
                        TextBlock(text=f"API error code: {str(status_code)}", wrap=True),
                        TextBlock(text=f"Error message: {error_message}", wrap=True),
                ]
            )
        print(type(output_card))
        output_card_data = json.loads(asyncio.run(output_card.to_json()))

        output_card_payload = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": output_card_data,
        }
        response = Response()
        response.text = "Test card"

        response.attachments = output_card_payload
        return response


bot.add_command(CreateTest())

# Call `run` for the bot to wait for incoming messages.
bot.run()

