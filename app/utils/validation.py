from app.models.message import NotificationMessage

def validate_notification_message(notification_message: NotificationMessage):
    if not notification_message.errors.monitors:
        raise ValueError("The notification message must contain at least one monitor with errors.")
    
    for monitor, step_errors in notification_message.errors.monitors.items():
        if not step_errors.steps:
            raise ValueError(f"The monitor '{monitor}' must contain at least one step with errors.")
        
        for step, errors in step_errors.steps.items():
            if not errors:
                raise ValueError(f"The step '{step}' in monitor '{monitor}' must contain at least one error detail.")
            
            for error in errors:
                if error.message is None:
                    raise ValueError(f"The error detail in step '{step}' of monitor '{monitor}' must contain a message.")
