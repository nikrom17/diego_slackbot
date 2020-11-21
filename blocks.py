import json


def build_uifw_team(employees):
    uifw_team_members = [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Here are the UIFW team members:",
			}
		},
		{
			"type": "divider"
		},
    ]
     
    for employee in employees:
        uifw_team_member = {
                    "type": "context",
                    "elements": [
                        {
                            "type": "image",
                            "image_url": employee.avatar,
                            "alt_text": f"{employee.name} avatar"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*{employee.name}*: {employee.title}"
                        }
                    ]
                }
        uifw_team_members.append(uifw_team_member);
    return uifw_team_members
        
