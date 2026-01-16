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
ITMSD-506-2301 | Database Essentials  
Assignment: A02
```

**Save it!**

---

## ✅ Check Your Project Structure

Your folder should now look like this:
```
event-management-api/
├── .venv/              (virtual environment folder)
├── .env                (MongoDB credentials)
├── .gitignore          (Git ignore rules)
├── main.py             (empty for now)
├── requirements.txt    (your dependencies)
├── vercel.json         (Vercel config)
└── README.md           (documentation)