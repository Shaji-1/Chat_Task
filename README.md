# Real-time Private Chat Application

A WhatsApp-inspired real-time private 1-on-1 chat application built with Django and WebSockets.

## Features

- **User Authentication**: Register, login, and logout
- **Private 1-on-1 Messaging**: Chat with any registered user privately
- **Real-time Communication**: Messages delivered instantly using WebSockets (Django Channels)
- **Persistent Chat History**: All messages stored in SQLite database
- **Cross-tab/Incognito Support**: Works across normal and incognito windows

## Tech Stack

- **Backend**: Django 6.0
- **Real-time**: Django Channels
- **ASGI Server**: Daphne
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Shaji-1/Chat_Task.git
   cd Chat_Task
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```powershell
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install django channels daphne
   ```

5. Run migrations:
   ```bash
   cd chat_project
   python manage.py migrate
   ```

6. Start the server:
   ```bash
   python manage.py runserver
   ```

7. Open your browser and go to **http://localhost:8000**

## Usage

1. Register a new user account
2. Login with your credentials
3. Select another user from the list to start chatting
4. Send messages and they'll appear in real-time!

## Project Structure

```
Chat_Task/
├── chat_project/          # Django project configuration
│   ├── chat_app/          # Main chat application
│   │   ├── consumers.py   # WebSocket consumer for real-time messaging
│   │   ├── models.py      # Message database model
│   │   ├── views.py       # Views for authentication and chat
│   │   └── templates/     # HTML templates
│   ├── settings.py        # Project settings
│   └── asgi.py            # ASGI configuration
└── db.sqlite3             # SQLite database
```

## License

MIT License
