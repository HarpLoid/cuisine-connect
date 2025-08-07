# CuisineConnect: The Recipe Sharing App

## Introduction

Cuisine Connect is a simulation of an online recipe-sharing platform designed for nutritionists to display their creations in an innovative way, adding more flavor to food choices.

## Features

- JWT-based user registration and login.
- Create, update, and delete your recipes.
- View other people's recipes.
- React to recipes with a like or bookmark them to your dashboard.

## Technologies Used

### Backend

- Python (Flask)
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-JWT-Extended

### Frontend

- React.js
- Redux
- TailwindCSS

## Quick Start

To get a local copy up and running, follow these simple steps.

### Prerequisites

- Python 3.x
- Node.js and npm/yarn

### Backend Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/your_username/CuisineConnect.git
    cd CuisineConnect/backend
    ```

2. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:

      ```sh
      venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```sh
      source venv/bin/activate
      ```

4. Install the required packages:

    ```sh
    pip install -r requirement.txt
    ```

5. Run the application:

    ```sh
    flask run
    ```

### Frontend Setup

1. Navigate to the frontend directory:

    ```sh
    cd ../frontend
    ```

2. Install the necessary packages:

    ```sh
    yarn install
    ```

    or

    ```sh
    npm install
    ```

3. Run the application:

    ```sh
    yarn start
    ```

    or

    ```sh
    npm start
    ```

## License

Distributed under the MIT License. See `LICENSE` for more information.
