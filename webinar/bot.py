"""
This file is used to create and initialize bot object and add commands to it.
"""
from webex_bot.webex_bot import WebexBot
import os
from dotenv import load_dotenv
from webinar_thousand_eye import ThousandEyeCommand

# Load the environment variables from the .env file
load_dotenv()

# Create a Bot Object
bot = WebexBot(teams_bot_token=os.getenv("WEBEX_TEAMS_ACCESS_TOKEN"),
               bot_name="Webinar Experimentation",
               include_demo_commands=False)

# Add new commands for the bot to listen out for.
bot.add_command(ThousandEyeCommand())

# Call `run` for the bot to wait for incoming messages.
bot.run()
