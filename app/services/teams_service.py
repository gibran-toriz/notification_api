import requests
from app.models.message import NotificationMessage
from app.utils.validation import validate_notification_message
from app.config import get_config

config = get_config()

def format_teams_message(notification_message: NotificationMessage):
    text_monitores = "Monitores con Errores" if len(notification_message.errors.monitors) > 1 else "Monitor con Error"
    body_items = [
        {
            "type": "TextBlock",
            "size": "Large",
            "weight": "Bolder",
            "text": f"Reporte de Errores {notification_message.flow}"
        },
        {
            "type": "TextBlock",
            "text": f"{len(notification_message.errors.monitors)} {text_monitores}",
            "wrap": True
        }
    ]
    

    for monitor_name, step_errors in notification_message.errors.monitors.items():
        monitor_section = {
            "type": "Container",
            "items": [
                {
                    "type": "TextBlock",
                    "weight": "Bolder",
                    "text": monitor_name,
                    "spacing": "Medium"
                }
            ]
        }
        
        for step_name, errors in step_errors.steps.items():
            step_section = {
                "type": "TextBlock",
                "text": f"- Step: {step_name}",
                "wrap": True,
                "spacing": "Medium"
            }
            monitor_section["items"].append(step_section)
            
            for error in errors:
                error_detail = {
                    "type": "TextBlock",
                    "text": f"- Error: {error.message}",
                    "wrap": True,
                    "spacing": "None"
                }
                monitor_section["items"].append(error_detail)
                
                if error.image_base64:
                    image_detail = {
                        "type": "Image",
                        "url": f"data:image/png;base64,{error.image_base64}",         
                        "size": "Stretch",
                        "spacing": "None"
                    }
                    monitor_section["items"].append(image_detail)                
        
        body_items.append(monitor_section)

    card_payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "body": body_items,
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.0"
                }
            }
        ]
    }

    return card_payload

def send_to_teams(notification_message: NotificationMessage):
    validate_notification_message(notification_message)
    teams_webhook_url = config.get_vault_secret(config.SECRET_PATH, config.SECRET_KEY)    
    formatted_message = format_teams_message(notification_message)
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(teams_webhook_url, json=formatted_message, headers=headers)
    response.raise_for_status()
    print("Notification sent to Microsoft Teams successfully.")
