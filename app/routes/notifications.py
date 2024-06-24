from flask import Blueprint, request, jsonify
from app.models.message import NotificationMessage
from app.services.teams_service import send_to_teams

notifications_bp = Blueprint('notifications', __name__)

def send_to_telegram(notification_message):
    ## To be implemented
    pass

def send_to_slack(notification_message):
    ## To be implemented    
    pass

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/', methods=['POST'])
def receive_notifications():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400
        
        notification_message = NotificationMessage.from_dict(data)
        
        channel = notification_message.channel if notification_message.channel else 'teams'

        if channel == 'teams':
            send_to_teams(notification_message)
        elif channel == 'telegram':
            send_to_telegram(notification_message)
        elif channel == 'slack':
            send_to_slack(notification_message)
        else:
            return jsonify({"error": "Unsupported channel"}), 400

        return jsonify({"message": "Notification sent successfully"}), 200
    
    except (TypeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400