import unittest
from app.models.message import NotificationMessage, ErrorDetail, StepErrors, MonitorErrors
from app.utils.validation import validate_notification_message

class TestNotificationMessage(unittest.TestCase):
    
    def test_valid_input(self):
        json_input = {
            "errors": {
                "Monitor1": [
                    {
                        "step1": [
                            ["error message", "image base64"],
                            ["another error message"]
                        ]
                    },
                    {
                        "step2": [
                            ["error message", "image base64"]
                        ]
                    }
                ],
                "Monitor2": [
                    {
                        "step1": [
                            ["error message"]
                        ]
                    }          
                ]
            }
        }
        notification_message = NotificationMessage.from_dict(json_input)
        
        self.assertIn("Monitor1", notification_message.errors.monitors)
        self.assertIn("Monitor2", notification_message.errors.monitors)
        self.assertIn("step1", notification_message.errors.monitors["Monitor1"].steps)
        self.assertIn("step2", notification_message.errors.monitors["Monitor1"].steps)
        self.assertEqual(notification_message.errors.monitors["Monitor1"].steps["step1"][0].message, "error message")
        self.assertEqual(notification_message.errors.monitors["Monitor1"].steps["step1"][0].image_base64, "image base64")

    def test_missing_optional_field(self):
        json_input = {
            "errors": {
                "Monitor1": [
                    {
                        "step1": [
                            ["error message"]
                        ]
                    }
                ]
            }
        }
        notification_message = NotificationMessage.from_dict(json_input)
        
        self.assertIn("Monitor1", notification_message.errors.monitors)
        self.assertIn("step1", notification_message.errors.monitors["Monitor1"].steps)
        self.assertEqual(notification_message.errors.monitors["Monitor1"].steps["step1"][0].message, "error message")
        self.assertIsNone(notification_message.errors.monitors["Monitor1"].steps["step1"][0].image_base64)

    def test_empty_error_list(self):
        json_input = {
            "errors": {
                "Monitor1": [
                    {
                        "step1": [
                            ["error message", "image base64"]
                        ]
                    }
                ],
                "Monitor2": [
                    {
                        "step1": [
                            []
                        ]
                    }
                ]
            }
        }
        with self.assertRaises(ValueError) as context:
            notification_message = NotificationMessage.from_dict(json_input)
        self.assertTrue("The step 'step1' in monitor 'Monitor2' contains an empty error list." in str(context.exception))

    def test_invalid_input_no_errors(self):
        json_input = {
            "errors": {}
        }
        with self.assertRaises(ValueError) as context:
            notification_message = NotificationMessage.from_dict(json_input)
        self.assertTrue("The notification message must contain at least one monitor with errors." in str(context.exception))

if __name__ == '__main__':
    unittest.main()
