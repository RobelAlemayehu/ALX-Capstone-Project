# API Usage Examples

This document provides practical examples of how to use the Fitness Tracker API.

## Base URL
- Local: `http://localhost:8000/api/`
- Production: `https://your-app-name.herokuapp.com/api/` or `https://yourusername.pythonanywhere.com/api/`

## 1. User Management

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

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "date_joined": "2024-01-15T10:30:00Z",
  "activities_count": 0
}
```

### Get All Users
```bash
curl http://localhost:8000/api/users/
```

### Get User by ID
```bash
curl http://localhost:8000/api/users/1/
```

### Update User
```bash
curl -X PATCH http://localhost:8000/api/users/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com"
  }'
```

### Delete User
```bash
curl -X DELETE http://localhost:8000/api/users/1/
```

## 2. Activity Management

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

**Response:**
```json
{
  "id": 1,
  "user": "john_doe",
  "activity_type": "running",
  "duration": 30,
  "distance": 5.0,
  "calories_burned": 300,
  "notes": "Morning run in the park",
  "date": "2024-01-15",
  "created_at": "2024-01-15T10:35:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

### Get All Activities
```bash
curl http://localhost:8000/api/activities/
```

### Get Activities for a Specific User
```bash
curl http://localhost:8000/api/activities/?user_id=1
```

### Get Activity by ID
```bash
curl http://localhost:8000/api/activities/1/
```

### Update Activity
```bash
curl -X PATCH http://localhost:8000/api/activities/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "duration": 35,
    "distance": 5.5
  }'
```

### Delete Activity
```bash
curl -X DELETE http://localhost:8000/api/activities/1/
```

## 3. Activity History

### Get Activity History (Last 30 days)
```bash
curl http://localhost:8000/api/activities/history/
```

### Get Activity History for Specific User
```bash
curl http://localhost:8000/api/activities/history/?user_id=1
```

### Get Activity History for Last 7 Days
```bash
curl http://localhost:8000/api/activities/history/?days=7
```

### Get Activity History Filtered by Type
```bash
curl http://localhost:8000/api/activities/history/?activity_type=running
```

### Get Activity History with Multiple Filters
```bash
curl "http://localhost:8000/api/activities/history/?user_id=1&days=7&activity_type=running"
```

**Response:**
```json
{
  "statistics": {
    "total_activities": 5,
    "total_duration": 150,
    "total_distance": 25.0,
    "total_calories": 1500,
    "average_duration": 30.0,
    "activities_by_type": [
      {
        "activity_type": "running",
        "count": 5
      }
    ]
  },
  "activities": [
    {
      "id": 1,
      "user": "john_doe",
      "activity_type": "running",
      "duration": 30,
      "distance": 5.0,
      "calories_burned": 300,
      "notes": "Morning run",
      "date": "2024-01-15",
      "created_at": "2024-01-15T10:35:00Z",
      "updated_at": "2024-01-15T10:35:00Z"
    }
  ],
  "period": "Last 7 days"
}
```

## 4. Activity Summary

### Get Summary for All Activities
```bash
curl http://localhost:8000/api/activities/summary/
```

### Get Summary for Specific User
```bash
curl http://localhost:8000/api/activities/summary/?user_id=1
```

**Response:**
```json
{
  "total_activities": 10,
  "total_duration_minutes": 300,
  "total_distance_km": 50.0,
  "total_calories_burned": 3000,
  "activities_by_type": [
    {
      "activity_type": "running",
      "count": 5,
      "total_duration": 150,
      "total_distance": 25.0
    },
    {
      "activity_type": "cycling",
      "count": 3,
      "total_duration": 90,
      "total_distance": 20.0
    },
    {
      "activity_type": "gym",
      "count": 2,
      "total_duration": 60,
      "total_distance": null
    }
  ]
}
```

## 5. User Activities Endpoint

### Get All Activities for a User
```bash
curl http://localhost:8000/api/users/1/activities/
```

## Using Python requests

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Create a user
user_data = {
    "username": "jane_doe",
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Doe"
}
response = requests.post(f"{BASE_URL}/users/", json=user_data)
user = response.json()
user_id = user["id"]

# Create an activity
activity_data = {
    "user_id": user_id,
    "activity_type": "cycling",
    "duration": 45,
    "distance": 15.0,
    "calories_burned": 450,
    "date": "2024-01-15",
    "notes": "Evening bike ride"
}
response = requests.post(f"{BASE_URL}/activities/", json=activity_data)
activity = response.json()

# Get activity history
response = requests.get(f"{BASE_URL}/activities/history/", params={"user_id": user_id, "days": 30})
history = response.json()

# Get summary
response = requests.get(f"{BASE_URL}/activities/summary/", params={"user_id": user_id})
summary = response.json()
```

## Using JavaScript (fetch)

```javascript
const BASE_URL = "http://localhost:8000/api";

// Create a user
async function createUser() {
  const response = await fetch(`${BASE_URL}/users/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username: "jane_doe",
      email: "jane@example.com",
      first_name: "Jane",
      last_name: "Doe"
    })
  });
  return await response.json();
}

// Create an activity
async function createActivity(userId) {
  const response = await fetch(`${BASE_URL}/activities/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      activity_type: "running",
      duration: 30,
      distance: 5.0,
      calories_burned: 300,
      date: "2024-01-15",
      notes: "Morning run"
    })
  });
  return await response.json();
}

// Get activity history
async function getHistory(userId, days = 30) {
  const response = await fetch(`${BASE_URL}/activities/history/?user_id=${userId}&days=${days}`);
  return await response.json();
}
```


