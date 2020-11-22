import os

slack_token = os.environ.get("DIEGO_SLACK_BOT_TOKEN")
slack_signing_secret = os.environ.get("DIEGO_SLACK_SIGNING_SECRET")

microsoft_client_secret = os.environ.get("DIEGO_MICROSOFT360_CLIENT_SECRET") 
microsoft_client_id = os.environ.get("DIEGO_MICROSOFT360_CLIENT_ID") 
microsoft_calendar_id = os.environ.get("DIEGO_UIFW_CALENDAR_ID")