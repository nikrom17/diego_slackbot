import os
import requests
from requests_oauthlib import OAuth2Session
# Import the async app instead of the regular one
from slack_bolt.async_app import AsyncApp
from oAuth import slack_token, slack_signing_secret
from api import slack_api, microsoft_api
from utils import get_user_id
from blocks import build_uifw_team, build_uifw_ooo
from models import OutOfOffice, setup_db, db, Employee

database_url = "postgresql://localhost/diego"

app = AsyncApp(
    name="Diego",
    token=slack_token,
    signing_secret=slack_signing_secret
)
# ***************** examples ************************
@app.event("app_mention")
async def event_test(body, say, logger):
    logger.info(body)
    await say("What's up?")
    
# Listens to incoming messages that contain "hello"
@app.message("hello")
async def message_hello(message, say, logger):
    try:
        # say() sends a message to the channel where the event was triggered
        await say(
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Click Me"},
                        "action_id": "button_click"
                    }
                }
            ],
            text=f"Hey there <@{message['user']}>!"
        )
    except Exception as e:
        logger.error(f"Error opening modal: {e}")

@app.shortcut("uidod")
async def action_button_click(ack, shortcut, client):
# Acknowledge the shortcut request
    await ack()
    # Call the views_open method using one of the built-in WebClients
    await client.views_open(
        trigger_id=shortcut["trigger_id"],
        # A simple view payload for a modal
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": "My App"},
            "close": {"type": "plain_text", "text": "Close"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "About the simplest modal you could conceive of :smile:\n\nMaybe <https://api.slack.com/reference/block-kit/interactive-components|*make the modal interactive*> or <https://api.slack.com/surfaces/modals/using#modifying|*learn more advanced modal use cases*>."
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "Psssst this modal was designed using <https://api.slack.com/tools/block-kit-builder|*Block Kit Builder*>"
                        }
                    ]
                }
            ]
        }
    )

# ********************* real shit ****************************

@app.message("employees") #todo should this be a shortcut?
async def message_employees(body, say, logger):
        all_employees = Employee.query.all()
        response = build_uifw_team(all_employees)
        logger.info(body)
        await say(blocks=response) 
    
    
@app.command("/add-uifw")
async def add_team_member(ack, say, command, logger):
    try:
        team_member_id = get_user_id(command["text"])
        duplicate = Employee.query.filter(Employee.slack_id == team_member_id).all()
        if not duplicate:
            url = f"{slack_api}/users.profile.get?token={slack_token}&user={team_member_id}"
            response = requests.get(url)
            team_member_profile = response.json()
            new_uifw_team_member = Employee(
                team_member_id,
                team_member_profile["profile"]["real_name"],
                team_member_profile["profile"]["image_original"],
                team_member_profile["profile"]["title"],
            )
            new_uifw_team_member.insert()
            slackbot_response = f"{team_member_profile['profile']['real_name']} has been added to UIFW"
        else:
            if len(duplicate) >  1:
                name = duplicate[0].name
            else:
                name = duplicate.name
            slackbot_response = f"{name} is already a member of UIFW"
        # Acknowledge command request
        await ack()
        await say(slackbot_response)
    except Exception as e:
        logger.error(f"Error adding team member: {e}")
    
@app.command("/remove-uifw")
async def remove_team_member(ack, say, command, logger):
    try:
        user_id = get_user_id(command["text"])
        team_member = Employee.query.filter(Employee.slack_id == user_id).all()
        if team_member:
            for member in team_member:
                member.delete()
            slackbot_response = f"That Backstopper was removed from UIFW" #todo fetch name or @user
        else:
            slackbot_response = f"That Backstopper isn't a member of UIFW" #todo fetch name or @user
        # Acknowledge command request
        await ack()
        await say(slackbot_response)
    except Exception as e:
        logger.error(f"Error adding team member: {e}")
@app.command("/rickybobby")
async def repeat_text(ack, say, command):
    # Acknowledge command request
    await ack()
    await say(f"{command['text']}")
    

@app.command("/ooo")
async def out_of_office(ack, say, command, logger):
    try:
        employee_ooo_data = {}
        employees = Employee.query.all()
        for employee in employees:
            employee_ooo_events = OutOfOffice.query.filter(OutOfOffice.employee_id == employee.id).all()
            if len(employee_ooo_events):
                employee_ooo_data[employee.id] = employee_ooo_events
        response = build_uifw_ooo(employee_ooo_data, employees)
        # Acknowledge command request
        await ack()
        await say(blocks=response)
    except Exception as e:
        logger.error(f"Error getting out of office events: {e}")
    
# Initialize Flask app
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

flask_app = Flask(__name__)
setup_db(flask_app)


# SlackRequestHandler translates WSGI requests to Bolt's interface
# and builds WSGI response from Bolt's response.
from slack_bolt.adapter.flask import SlackRequestHandler
handler = SlackRequestHandler(app)

# Register routes to Flask app
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    # handler runs App's dispatch method
    return handler.handle(request)

if __name__ == "__main__":
    app.start(3000)