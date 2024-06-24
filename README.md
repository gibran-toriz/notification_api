# Notification API

This project is a Flask-based API for sending notifications to Microsoft Teams using Adaptive Cards. It includes functionality to read secrets from HashiCorp Vault, format messages, and send them to a Teams channel via a webhook URL.


## Getting Started

### Prerequisites

- Python 3.9 or higher
- Docker
- Docker Compose
- HashiCorp Vault

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-username/notification-api.git
    cd notification-api
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python3 -m venv env
    source env/bin/activate 
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the `.env` file**:
    Create a `.env` file in the root directory with the following content:
    ```sh
    FLASK_ENV=development
    VAULT_URL=https://your-vault-url
    VAULT_TOKEN=your-vault-token
    SECRET_PATH=iwrobot
    SECRET_KEY=webhook_teams
    ```

### Running the Application

1. **Run the Flask application**:
    ```sh
    python run.py
    ```

2. **Access the API**:
    The API will be running at `http://127.0.0.1:5000`.

### Using Docker

1. **Build the Docker image**:
    ```sh
    docker-compose build
    ```

2. **Run the Docker container**:
    ```sh
    docker-compose up
    ```

3. **Access the API**:
    The API will be running at `http://127.0.0.1:5000`.

## API Endpoints

### Send Notification

- **URL**: `/notifications/notify`
- **Method**: `POST`
- **Description**: Send a notification to Microsoft Teams.
- **Request Body**:
    ```json
    {
        "iwagent": "flow-name",
        "errors": {
            "monitor_name": [
                {
                    "step_name": [
                        ["error message", "base64_image"]
                    ]
                }
            ]
        }
    }
    ```

- **Response**:
    - `200 OK`: Notification sent successfully.
    - `400 Bad Request`: Invalid input data.
    - `500 Internal Server Error`: An error occurred while processing the request.

## Project Components

### Configuration (`app/config.py`)

Handles the loading of environment variables and fetching secrets from HashiCorp Vault.

### Models (`app/models/message.py`)

Defines the data models for parsing and validating notification messages.

### Routes (`app/routes/notifications.py`)

Defines the API endpoints and handles incoming requests.

### Services (`app/services/teams_service.py`)

Formats messages and sends them to Microsoft Teams.

### Utilities (`app/utils/validation.py`)

Provides utility functions for validating incoming requests.

## Testing

- **Run tests**:
    ```sh
    python -m unittest discover -s tests
    ```

## License

This project is licensed under the MIT License.
