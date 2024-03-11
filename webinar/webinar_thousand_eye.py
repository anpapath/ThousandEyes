import json
import logging
import os
from typing import List
import requests
from webexteamssdk.models.cards import AdaptiveCard, TextBlock, ColumnSet, Column, FontWeight, FontSize, Text
from webexteamssdk.models.cards.actions import Submit, ShowCard
from webex_bot.models.command import Command
from webex_bot.models.response import response_from_adaptive_card
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

# Setting up logging to log lines
log = logging.getLogger(__name__)


class ThousandEyeCommand(Command):
    """
    This command would help our bot to handle A Thousand Eye Activities
    Currently only supporting List Agents
    """
    def __init__(self):
        super().__init__(
            command_keyword="thousand_eye", # The command keyword helps the bot to identify the command
            help_message="Thousand Eye Activity", # The help message is what the bot will display when the see the button
            chained_commands=[ThousandEyeListAgent()] # This is chained command which will be executed when the button is clicked
        )

    def execute(self, message, attachment_actions, activity):
        """
        If you want to respond to a submit operation on the card, you
        would write code here!

        You can return text string here or even another card (Response).

        This sample command function simply echos back the sent message.

        :param message: message with command already stripped
        :param attachment_actions: attachment_actions object
        :param activity: activity object

        :return: a string or Response object (or a list of either). Use Response if you want to return another card.
        """

        # Creating textblock for the message
        text1 = TextBlock("I am here to help with Thousand Eye Activities", weight=FontWeight.BOLDER, size=FontSize.MEDIUM)

        # Creating textblock for the message
        text2 = TextBlock("My purpose is to help with Thousand Eye Activities.",
                          wrap=True, isSubtle=True)

        # Creating a submit button to list agents
        submit = Submit(title="List Agents",
                        data={
                            "callback_keyword": "thousand_eye_list"} # This is the callback keyword which will be used to identify the command when Submit button is pressed
                        )

        # Creating an adaptive card with the above elements
        card = AdaptiveCard(
            body=[ColumnSet(columns=[Column(items=[text1, text2], width=2)]),
                  ], actions=[submit])

        log.debug(f"Webinar Adaptive Card {json.dumps(card.to_json(), indent=4)}")
        return response_from_adaptive_card(card)


class ThousandEyeListAgent(Command):
    """
    This command will list the agents from Thousand Eye
    """
    def __init__(self):
        super().__init__(
            command_keyword="thousand_eye_list", # The command keyword helps the bot to identify the command and since this is a chained command, no help message is required
            delete_previous_message=True # This will delete the previous message when the command is executed
        )

    def get_list_agents(self) -> dict:
        """
        This function will get the list of agents from ThousandEyes
        :return: List of agents
        """
        base_url = "https://api.thousandeyes.com/v7/agents"
        query_string = "?agentTypes=ENTERPRISE"
        TETOKEN = os.getenv("TH_ACCESS_TOKEN")
        # Defining the Headers for the API request to ThousandEyes

        TE_headers = {
            "Authorization": "Bearer " + TETOKEN,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.get(url=base_url + query_string, headers=TE_headers)
        agents = response.json()
        return agents

    def execute(self, message, attachment_actions, activity):
        agents = self.get_list_agents()

        # The Adaptive card header
        textbanner = TextBlock(size="Medium", weight="Bolder", text="Your ThousandEyes agents are listed below",
                               wrap=True)

        agent_list_content = []
        if not agents.get("agents"):
            # If there are no agents, then add a message to the card to indicate that no agents were found.
            agent_list_content.extend(
                [TextBlock(text="No agents found", wrap=True, spacing="ExtraLarge"),
                 TextBlock(text="-----------------------------", wrap=True, spacing="Large")]
            )
        else:
            for agent in agents["agents"]:
                # For each agent in the API response, add in the adaptive card TextBlock() elements which contain
                # the Agent name and IP address. Then, add a separator line to separate the Agent information.
                agent_list_content.extend(
                    [TextBlock(text=f"Agent Name: {agent['agentName']}", wrap=True, spacing="ExtraLarge"),
                     TextBlock(text=f"Agent IP: {agent['ipAddresses'][0]}", wrap=True, spacing="ExtraLarge"),

                     TextBlock(text="-----------------------------", wrap=True, spacing="Large")]
                )

        # Creating an adaptive card with the above elements
        card = AdaptiveCard(
            body=[ColumnSet(columns=[Column(items=[textbanner, *agent_list_content], width=2)]),
                  ])
        return response_from_adaptive_card(card)
