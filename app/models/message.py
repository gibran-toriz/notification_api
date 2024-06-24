from typing import List, Optional, Dict, Union
from dataclasses import dataclass, field

@dataclass
class ErrorDetail:
    message: str
    image_base64: Optional[str] = None

@dataclass
class StepErrors:
    steps: Dict[str, List[ErrorDetail]] = field(default_factory=dict)

@dataclass
class MonitorErrors:
    monitors: Dict[str, StepErrors] = field(default_factory=dict)

@dataclass
class NotificationMessage:
    errors: MonitorErrors
    channel: Optional[str] = None

    @staticmethod
    def from_dict(data: Dict[str, Union[str, Dict]]) -> 'NotificationMessage':
        channel = data.get('channel')
        monitors = {}
        for monitor_name, steps in data.get('errors', {}).items():
            step_errors = {}
            for step in steps:
                for step_name, errors in step.items():
                    error_details = []
                    for error in errors:
                        if not error:
                            raise ValueError(f"The step '{step_name}' in monitor '{monitor_name}' contains an empty error list.")
                        message = error[0] if len(error) > 0 else None
                        image_base64 = error[1] if len(error) > 1 else None
                        error_details.append(ErrorDetail(message=message, image_base64=image_base64))
                    if not error_details:
                        raise ValueError(f"The step '{step_name}' in monitor '{monitor_name}' must contain at least one error detail.")
                    step_errors[step_name] = error_details
            if not step_errors:
                raise ValueError(f"The monitor '{monitor_name}' must contain at least one step with errors.")
            monitors[monitor_name] = StepErrors(steps=step_errors)
        if not monitors:
            raise ValueError("The notification message must contain at least one monitor with errors.")
        return NotificationMessage(channel=channel, errors=MonitorErrors(monitors=monitors))
