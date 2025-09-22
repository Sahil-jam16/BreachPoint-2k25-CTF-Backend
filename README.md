# BreachPoint CTF Backend

This is the backend API for the BreachPoint CTF (Capture The Flag) platform, built with FastAPI and Python. It provides services for managing teams, challenges, and administrative functions, using Firebase for data storage and file management.

## Features

-   **Challenge Management**: API endpoints for creating, reading, updating, and deleting CTF challenges.
-   **Team Management**: Endpoints for team registration, scoring, and progress tracking.
-   **Admin Panel**: Secure endpoints for administrative tasks.
-   **Firebase Integration**: Uses Firestore for the database and Firebase Storage for challenge-related file uploads.
-   **Automatic API Documentation**: Interactive API documentation powered by Swagger UI and ReDoc.

## Technologies Used

-   [Python 3.8+](https://www.python.org/)
-   [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance) web framework for building APIs.
-   [Uvicorn](https://www.uvicorn.org/): An ASGI server for running FastAPI applications.
-   [Firebase Admin SDK for Python](https://firebase.google.com/docs/admin/python): For integration with Firestore and Firebase Storage.
-   [python-dotenv](https://pypi.org/project/python-dotenv/): For managing environment variables.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Python 3.8 or newer
-   pip package manager
-   A Firebase project. If you don't have one, create one at the [Firebase Console](https://console.firebase.google.com/).

### Installation

1.  **Clone the repository:**
    ```sh
    git clone <your-repository-url>
    cd Backend_BreachPoint
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    If a `requirements.txt` file is not present, create one with the following content:
    ```txt
    fastapi
    uvicorn[standard]
    firebase-admin
    python-dotenv
    ```
    Then run:
    ```sh
    pip install -r requirements.txt
    ```

### Configuration

The application requires a connection to a Firebase project.

1.  **Firebase Service Account:**
    -   In your Firebase project console, go to **Project settings** > **Service accounts**.
    -   Click on **Generate new private key** to download your service account JSON file.
    -   **Important**: Treat this file as a secret. Do not commit it to your version control system. Add its filename to your `.gitignore` file.
    -   Place the downloaded JSON file in the root of the `Backend_BreachPoint` directory (or another secure location).

2.  **Environment Variables:**
    -   Create a file named `.env` in the `Backend_BreachPoint` root directory.
    -   Add the following environment variables to the `.env` file, replacing the placeholder values with your actual Firebase project details.

    ```env
    # Path to your Firebase service account key file
    SERVICE_ACCOUNT_KEY_PATH="path/to/your/serviceAccountKey.json"

    # Your Firebase Storage bucket URL (e.g., your-project-id.appspot.com)
    FIREBASE_STORAGE_BUCKET="your-project-id.appspot.com"
    ```
    *Example `SERVICE_ACCOUNT_KEY_PATH`*: If you placed the key in the project root, the path would just be the filename, e.g., `"serviceAccountKey.json"`.

## Running the Application

Once you have completed the setup and configuration, you can run the development server.

From the `Backend_BreachPoint` directory, run:

```sh
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. The `--reload` flag will automatically restart the server when you make changes to the code.

## API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can access it at:

-   **Swagger UI**: http://127.0.0.1:8000/docs
-   **ReDoc**: http://127.0.0.1:8000/redoc

These interfaces allow you to explore and test all the API endpoints directly from your browser.