### This is an example of Webex bot interacting with Thousand Eye API
#### Requirements
Require environment variables
- `TH_WEBEX_BOT_EMAIL` - Webex bot email
- `TH_ACCESS_TOKEN` - Thousand Eye API access token
- `WEBEX_TEAMS_ACCESS_TOKEN` - Webex Teams API access token


__Setting environment variables__

To Set environment variables, you can use the following command
```bash
export TH_WEBEX_BOT_EMAIL="YOUR_BOT_EMAIL"
export TH_ACCESS_TOKEN="YOUR_THOUSAND_EYE_API_ACCESS_TOKEN"
export WEBEX_TEAMS_ACCESS_TOKEN="YOUR_WEBEX_BOT_ACCESS_TOKEN"
```

#### OR

You can create a `.env` file in the root directory of the project and add the following content
```bash
TH_WEBEX_BOT_EMAIL="YOUR_BOT_EMAIL"
TH_ACCESS_TOKEN="YOUR_THOUSAND_EYE_API_ACCESS_TOKEN"
WEBEX_TEAMS_ACCESS_TOKEN="YOUR_WEBEX_BOT_ACCESS_TOKEN"
```

After setting the environment variables, you can run the bot using the following command
```bash
cd webinar
python bot.py
```