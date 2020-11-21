import os
import requests
# Import the async app instead of the regular one
from slack_bolt.async_app import AsyncApp
from utils import get_user_id
from blocks import build_uifw_team, build_uifw_ooo
from models import OutOfOffice, setup_db, db, Employee

database_url = "postgresql://localhost/diego"

app = AsyncApp(
    name="Diego",
    token=os.environ.get("DIEGO_SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("DIEGO_SLACK_SIGNING_SECRET")
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
    
    
@app.command("/add") #todo create employee from slack profile
async def add_team_member(ack, say, command, logger):
    try:
        team_member_id = get_user_id(command["text"])
        print(team_member_id)
        # Acknowledge command request
        response = requests.get("https://slack.com/api/users.profile.get?token=xoxb-1499543051015-1511265275141-9l6Lx0ml1numbgFZw8oX0xfo&user=U01FU3PTE8G&pretty=1")
        await ack()
        await say(f"{command['text']}")
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