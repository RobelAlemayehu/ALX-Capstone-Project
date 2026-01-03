# Fitness Tracker API

A RESTful API built with Django REST Framework for managing fitness activities. Users can log, update, delete activities, and view their activity history.

## Features

- **CRUD Operations**: Full Create, Read, Update, Delete operations for both users and activities
- **Activity History**: View activity history with filtering and statistics
- **Activity Summary**: Get aggregated statistics for activities
- **User Management**: Manage users and view their activities
- **Django ORM**: All database interactions use Django ORM

## API Endpoints

### Users

- `GET /api/users/` - List all users
- `POST /api/users/` - Create a new user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `PATCH /api/users/{id}/` - Partially update user
- `DELETE /api/users/{id}/` - Delete user
- `GET /api/users/{id}/activities/` - Get all activities for a user

### Activities

- `GET /api/activities/` - List all activities (optional: `?user_id={id}`)
- `POST /api/activities/` - Create a new activity
- `GET /api/activities/{id}/` - Get activity details
- `PUT /api/activities/{id}/` - Update activity
- `PATCH /api/activities/{id}/` - Partially update activity
- `DELETE /api/activities/{id}/` - Delete activity
- `GET /api/activities/history/` - Get activity history with statistics
  - Query parameters:
    - `user_id` (optional): Filter by user ID
    - `days` (optional, default: 30): Number of days to look back
    - `activity_type` (optional): Filter by activity type
- `GET /api/activities/summary/` - Get summary statistics
  - Query parameters:
    - `user_id` (optional): Filter by user ID

## Activity Types

- running
- cycling
- swimming
- walking
- gym
- yoga
- hiking
- other

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Project Tesst"
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Update the `.env` file with your settings:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## Example API Usage

### Create a User
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Create an Activity
```bash
curl -X POST http://localhost:8000/api/activities/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "activity_type": "running",
    "duration": 30,
    "distance": 5.0,
    "calories_burned": 300,
    "date": "2024-01-15",
    "notes": "Morning run in the park"
  }'
```

### Get Activity History
```bash
curl http://localhost:8000/api/activities/history/?user_id=1&days=7
```

### Get Activity Summary
```bash
curl http://localhost:8000/api/activities/summary/?user_id=1
```

## Deployment

### Deploying to Heroku

1. Install Heroku CLI and login:
```bash
heroku login
```

2. Create a Heroku app:
```bash
heroku create your-app-name
```

3. Set environment variables:
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

4. Deploy:
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

5. Run migrations:
```bash
heroku run python manage.py migrate
```

6. Create superuser (optional):
```bash
heroku run python manage.py createsuperuser
```

7. Your API will be available at `https://your-app-name.herokuapp.com/api/`

**Note**: Heroku automatically uses PostgreSQL via the `DATABASE_URL` environment variable. The `dj-database-url` package handles this configuration.

### Deploying to PythonAnywhere

1. Sign up for a PythonAnywhere account at https://www.pythonanywhere.com

2. Open a Bash console and clone your repository:
```bash
git clone <repository-url>
cd "Project Tesst"
```

3. Create a virtual environment:
```bash
python3.10 -m venv venv
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file with your settings:
```bash
nano .env
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Collect static files:
```bash
python manage.py collectstatic --noinput
```

8. In the PythonAnywhere Web tab:
   - Create a new web app
   - Choose "Manual configuration" and Python 3.10
   - Set the source code directory to your project path
   - Set the working directory to your project path
   - Set the virtualenv path to your venv path

9. Edit the WSGI configuration file:
```python
import os
import sys

path = '/home/yourusername/Project Tesst'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'fitness_tracker.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

10. Add your domain to `ALLOWED_HOSTS` in settings.py or via environment variables

11. Reload your web app

12. Your API will be available at `https://yourusername.pythonanywhere.com/api/`

## Database

The project uses SQLite for development and PostgreSQL for production (Heroku). For PythonAnywhere, you can use SQLite or configure MySQL/PostgreSQL.

## Testing

You can test the API using:
- cURL commands
- Postman
- Django REST Framework's browsable API at `http://localhost:8000/api/`
- Any HTTP client

## Project Structure

```
fitness_tracker/
├── fitness_tracker/          # Main project directory
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py               # WSGI configuration
├── activities/               # Activities app
│   ├── models.py             # Activity and User models
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # ViewSets for API endpoints
│   ├── urls.py               # App URL configuration
│   └── admin.py              # Admin configuration
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── Procfile                  # Heroku deployment file
└── README.md                 # This file
```

## License

This project is open source and available for use.


