# Event Management API

RESTful API for managing events, attendees, venues, and bookings with MongoDB Atlas.

## Setup

1. Create virtual environment:
```bash
   python -m venv .venv
   .venv\Scripts\activate
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Create `.env` file with your MongoDB connection string

4. Run the application:
```bash
   uvicorn main:app --reload
```

## API Documentation

Once running, visit: http://127.0.0.1:8000/docs

## Author

Matthew Saliba
Database Essentials Assignment
