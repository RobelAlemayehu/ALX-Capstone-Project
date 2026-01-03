# Fitness Tracker API

A RESTful API built with Django REST Framework for managing fitness activities. Users can log, update, delete activities, and view their activity history.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Setup (First Time Only)

```bash
# Navigate to project directory
cd "Project Tesst"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create admin superuser (optional - default credentials provided)
python create_superuser.py
```

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

### Step 2: Run the Server

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the development server
python manage.py runserver
```

The server will start at: **http://localhost:8000/**

### Step 3: Access the API

Once the server is running, you can access:

- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
  - Login with: `admin` / `admin123`
- **Browsable API**: http://localhost:8000/api/ (Interactive API interface)

### Stop the Server

Press `Ctrl + C` in the terminal where the server is running.

---

## 📋 Features

- ✅ **CRUD Operations**: Full Create, Read, Update, Delete operations for both users and activities
- ✅ **JWT Authentication**: Secure token-based authentication using JWT
- ✅ **User Permissions**: Users can only manage their own activities
- ✅ **Activity History**: View activity history with advanced filtering and statistics
- ✅ **Date Range Filtering**: Filter activities by specific date ranges (start_date, end_date)
- ✅ **Sorting**: Sort activities by date, duration, or calories burned
- ✅ **Activity Trends**: Weekly and monthly activity trends over time
- ✅ **Activity Summary**: Get aggregated statistics for activities
- ✅ **Field Validation**: Comprehensive validation for all activity fields
- ✅ **Error Handling**: Proper HTTP status codes and error messages
- ✅ **Pagination**: Automatic pagination for large result sets
- ✅ **Django ORM**: All database interactions use Django ORM

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/register/` | Register a new user | No |
| POST | `/api/token/` | Get JWT access token | No |
| POST | `/api/token/refresh/` | Refresh JWT access token | No |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/users/` | List all users | Yes |
| POST | `/api/users/` | Create a new user (or use `/api/register/`) | No |
| GET | `/api/users/{id}/` | Get user details | Yes |
| PUT | `/api/users/{id}/` | Update user (full) - own profile only | Yes |
| PATCH | `/api/users/{id}/` | Update user (partial) - own profile only | Yes |
| DELETE | `/api/users/{id}/` | Delete user - own profile only | Yes |
| GET | `/api/users/{id}/activities/` | Get all activities for a user - own activities only | Yes |

### Activities

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/activities/` | List user's own activities | Yes |
| POST | `/api/activities/` | Create a new activity | Yes |
| GET | `/api/activities/{id}/` | Get activity details (own activities only) | Yes |
| PUT | `/api/activities/{id}/` | Update activity (own activities only) | Yes |
| PATCH | `/api/activities/{id}/` | Update activity (own activities only) | Yes |
| DELETE | `/api/activities/{id}/` | Delete activity (own activities only) | Yes |
| GET | `/api/activities/history/` | Get activity history with statistics | Yes |
| GET | `/api/activities/summary/` | Get summary statistics | Yes |
| GET | `/api/activities/trends/` | Get activity trends (weekly/monthly) | Yes |

### Query Parameters for Activities List

**GET** `/api/activities/`

Query Parameters:
- `activity_type` (optional): Filter by activity type
- `sort_by` (optional): Sort by field
  - Valid values: `date`, `-date`, `duration`, `-duration`, `calories_burned`, `-calories_burned`, `created_at`, `-created_at`
  - Default: `-date` (newest first)

**Example:**
```
GET /api/activities/?activity_type=running&sort_by=-duration
```

### Activity History Endpoint

**GET** `/api/activities/history/`

Query Parameters:
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `days` (optional, default: 30): Number of days to look back (ignored if start_date/end_date provided)
- `activity_type` (optional): Filter by activity type
- `sort_by` (optional): Sort by field (date, -date, duration, -duration, calories_burned, -calories_burned)

**Examples:**
```
GET /api/activities/history/?start_date=2024-01-01&end_date=2024-01-31
GET /api/activities/history/?days=7&activity_type=running&sort_by=-duration
GET /api/activities/history/?start_date=2024-01-01
```

### Activity Summary Endpoint

**GET** `/api/activities/summary/`

Query Parameters:
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format

**Example:**
```
GET /api/activities/summary/?start_date=2024-01-01&end_date=2024-01-31
```

### Activity Trends Endpoint

**GET** `/api/activities/trends/`

Query Parameters:
- `period` (optional, default: 'weekly'): 'weekly' or 'monthly'
- `weeks` (optional, default: 4): Number of weeks to look back (for weekly period)
- `months` (optional, default: 6): Number of months to look back (for monthly period)

**Examples:**
```
GET /api/activities/trends/?period=weekly&weeks=8
GET /api/activities/trends/?period=monthly&months=12
```

---

## 🏃 Activity Types

Available activity types:
- `running`
- `cycling`
- `swimming`
- `walking`
- `gym`
- `yoga`
- `hiking`
- `other`

---

## 💻 Example API Usage

### 1. Register a New User

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### 2. Get JWT Token (Login)

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Create an Activity (Authenticated)

```bash
curl -X POST http://localhost:8000/api/activities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "activity_type": "running",
    "duration": 30,
    "distance": 5.0,
    "calories_burned": 300,
    "date": "2024-01-15",
    "notes": "Morning run in the park"
  }'
```

### 4. Get Activity History with Date Range

```bash
curl -X GET "http://localhost:8000/api/activities/history/?start_date=2024-01-01&end_date=2024-01-31&sort_by=-duration" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Get Activity Trends (Weekly)

```bash
curl -X GET "http://localhost:8000/api/activities/trends/?period=weekly&weeks=8" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 6. Get Activity Summary

```bash
curl -X GET "http://localhost:8000/api/activities/summary/?start_date=2024-01-01&end_date=2024-01-31" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 7. List Activities with Sorting

```bash
curl -X GET "http://localhost:8000/api/activities/?activity_type=running&sort_by=-calories_burned" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 8. Refresh JWT Token

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "YOUR_REFRESH_TOKEN"
  }'
```

For more examples, see [API_EXAMPLES.md](API_EXAMPLES.md)

---

## 🔐 Authentication & Permissions

### JWT Authentication

The API uses JWT (JSON Web Tokens) for authentication. You need to:

1. **Register** a new user at `/api/register/` (no auth required)
2. **Login** at `/api/token/` to get access and refresh tokens
3. **Include the token** in all authenticated requests:
   ```
   Authorization: Bearer YOUR_ACCESS_TOKEN
   ```

### Permissions

- **Public Endpoints** (No authentication required):
  - `POST /api/register/` - User registration
  - `POST /api/token/` - Get JWT token (login)
  - `POST /api/token/refresh/` - Refresh JWT token

- **Authenticated Endpoints** (Authentication required):
  - All activity endpoints
  - User profile endpoints

- **Ownership Rules**:
  - Users can only view, create, update, and delete their own activities
  - Users can only view and modify their own profile
  - Users cannot access other users' activities or profiles

### Token Expiration

- **Access Token**: Valid for 1 hour
- **Refresh Token**: Valid for 7 days
- Use the refresh token to get a new access token when it expires

---

## 🛠️ Installation (Detailed)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "Project Tesst"
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
# Generate a secret key (optional - defaults provided)
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Create `.env` file:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=
```

### 5. Database Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 6. Create Admin User

**Option 1: Use the provided script (recommended)**
```bash
python create_superuser.py
```
This creates a superuser with:
- Username: `admin`
- Password: `admin123`

**Option 2: Interactive creation**
```bash
python manage.py createsuperuser
```

### 7. Run the Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

---

## 🌐 Deployment

### Deploying to Heroku

1. **Install Heroku CLI and login:**
   ```bash
   heroku login
   ```

2. **Create a Heroku app:**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables:**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

4. **Deploy:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

5. **Run migrations:**
   ```bash
   heroku run python manage.py migrate
   ```

6. **Create superuser (optional):**
   ```bash
   heroku run python create_superuser.py
   ```

7. **Your API will be available at:** `https://your-app-name.herokuapp.com/api/`

**Note:** Heroku automatically uses PostgreSQL via the `DATABASE_URL` environment variable.

### Deploying to PythonAnywhere

1. Sign up at https://www.pythonanywhere.com

2. **Open Bash console and clone repository:**
   ```bash
   git clone <repository-url>
   cd "Project Tesst"
   ```

3. **Create virtual environment:**
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create `.env` file:**
   ```bash
   nano .env
   ```

6. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Configure Web App:**
   - Go to Web tab in PythonAnywhere dashboard
   - Create new web app
   - Choose "Manual configuration" and Python 3.10
   - Set source code directory to your project path
   - Set working directory to your project path
   - Set virtualenv path to your venv path

9. **Edit WSGI configuration file:**
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

10. **Add domain to ALLOWED_HOSTS** in settings.py or via environment variables

11. **Reload your web app**

12. **Your API will be available at:** `https://yourusername.pythonanywhere.com/api/`

---

## 🗄️ Database

- **Development**: SQLite (default)
- **Production (Heroku)**: PostgreSQL (automatic)
- **Production (PythonAnywhere)**: SQLite or MySQL/PostgreSQL (configurable)

---

## 🧪 Testing

You can test the API using:
- **cURL commands** (see examples above)
- **Postman** - Import the API endpoints
- **Django REST Framework's browsable API** - Visit `http://localhost:8000/api/`
- **Any HTTP client** - Python requests, JavaScript fetch, etc.

---

## 📁 Project Structure

```
Project Tesst/
├── fitness_tracker/          # Main project directory
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
├── activities/               # Activities app
│   ├── models.py             # Activity model
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # ViewSets for API endpoints
│   ├── urls.py               # App URL configuration
│   ├── admin.py              # Admin configuration
│   └── migrations/           # Database migrations
├── manage.py                 # Django management script
├── create_superuser.py       # Script to create admin user
├── requirements.txt          # Python dependencies
├── Procfile                  # Heroku deployment file
├── runtime.txt               # Python version for Heroku
├── setup.sh                  # Automated setup script
├── README.md                 # This file
└── API_EXAMPLES.md           # Detailed API usage examples
```

---

## 🔐 Admin Panel Access

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

**To change password:**
```bash
python manage.py changepassword admin
```

**To create new superuser:**
```bash
python manage.py createsuperuser
```

---

## ❓ Troubleshooting

### Server won't start
- Make sure virtual environment is activated
- Check if port 8000 is already in use
- Run `python manage.py check` to verify configuration

### Database errors
- Run `python manage.py makemigrations`
- Then run `python manage.py migrate`

### Module not found errors
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

### Admin login issues
- Run `python create_superuser.py` to create/reset admin user
- Check that migrations have been applied

---

## 📝 License

This project is open source and available for use.

---

## 📞 Support

For issues or questions:
1. Check the [API_EXAMPLES.md](API_EXAMPLES.md) for usage examples
2. Review the Django REST Framework documentation
3. Check the troubleshooting section above
