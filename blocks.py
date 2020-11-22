import json

# ---------------------------------------------------------------------------- #
# UIFW Team List
# ---------------------------------------------------------------------------- #

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
        
        
# ---------------------------------------------------------------------------- #
# Out of Office
# ---------------------------------------------------------------------------- #

def get_ooo_emoji(reason):
    if reason == "PTO":
        return("🌴")
    if reason == "sick":
        return("🤒")
    return("🚫")

def get_ooo_date(date):
    return date.strftime("%m/%d")
    

def build_uifw_ooo(employee_ooo_data, employees):
    uifw_oooo_response = [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Here is the scheduled out of office events for UIFW:",
			}
		},
    ]
     
    for employee in employees:
        if employee_ooo_data.get(employee.id):
            uifw_oooo_response.append({
                "type": "divider"
            })
            uifw_oooo_response.append({
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "image_url": employee.avatar,
                        "alt_text": f"{employee.name} avatar"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*{employee.name}*"
                    }
                ]
            })
            ooo_event_text = []
            for ooo_event in employee_ooo_data[employee.id]:
                emoji = get_ooo_emoji(ooo_event.reason)
                start = get_ooo_date(ooo_event.start)
                end = get_ooo_date(ooo_event.end)
                duration = ooo_event.duration
                
                if duration > 1:
                    ooo_event_text.append(f"{emoji} {start} - {end} [{duration} days]")
                else:
                    ooo_event_text.append(f"{emoji} {start}\n")
                
  
            ooo_events_section = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "\n".join(ooo_event_text)
                }
            }
            uifw_oooo_response.append(ooo_events_section);
    return uifw_oooo_response