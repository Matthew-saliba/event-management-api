import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv
import motor.motor_asyncio
import io

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Connect to MongoDB Atlas using connection string from .env
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client.event_management_db

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Event Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "online"
    }

# Security: Pydantic models validate all input data, preventing SQL/NoSQL injection
# by enforcing strict data types and rejecting malformed requests before database operations

# Data Models
class Event(BaseModel):
    name: str
    description: str
    date: str
    venue_id: str
    max_attendees: int

class Attendee(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None

class Venue(BaseModel):
    name: str
    address: str
    capacity: int

class Booking(BaseModel):
    event_id: str
    attendee_id: str
    ticket_type: str
    quantity: int

# Event Endpoints
@app.post("/events")
async def create_event(event: Event):
    event_doc = event.dict()
    result = await db.events.insert_one(event_doc)
    return {"message": "Event created", "id": str(result.inserted_id)}

@app.get("/events")
async def get_events():
    events = await db.events.find().to_list(100)
    for event in events:
        event["_id"] = str(event["_id"])
    return events

# Upload Event Poster (Image)
@app.post("/upload_event_poster/{event_id}")
async def upload_event_poster(event_id: str, file: UploadFile = File(...)):
    content = await file.read()
    poster_doc = {
        "event_id": event_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "content": content,
        "uploaded_at": datetime.utcnow()
    }
    result = await db.event_posters.insert_one(poster_doc)
    return {"message": "Event poster uploaded", "id": str(result.inserted_id)}

# Update Event
@app.put("/events/{event_id}")
async def update_event(event_id: str, event: Event):
    from bson import ObjectId
    event_doc = event.dict()
    result = await db.events.update_one({"_id": ObjectId(event_id)}, {"$set": event_doc})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event updated"}

# Delete Event
@app.delete("/events/{event_id}")
async def delete_event(event_id: str):
    from bson import ObjectId
    result = await db.events.delete_one({"_id": ObjectId(event_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted"}

# Retrieve Event Poster
@app.get("/event_poster/{poster_id}")
async def get_event_poster(poster_id: str):
    from bson import ObjectId
    poster = await db.event_posters.find_one({"_id": ObjectId(poster_id)})
    if not poster:
        raise HTTPException(status_code=404, detail="Poster not found")
    return StreamingResponse(io.BytesIO(poster["content"]), media_type=poster["content_type"])

# Attendee Endpoints
@app.post("/attendees")
async def create_attendee(attendee: Attendee):
    attendee_doc = attendee.dict()
    result = await db.attendees.insert_one(attendee_doc)
    return {"message": "Attendee created", "id": str(result.inserted_id)}

@app.get("/attendees")
async def get_attendees():
    attendees = await db.attendees.find().to_list(100)
    for attendee in attendees:
        attendee["_id"] = str(attendee["_id"])
    return attendees

# Update Attendee
@app.put("/attendees/{attendee_id}")
async def update_attendee(attendee_id: str, attendee: Attendee):
    from bson import ObjectId
    attendee_doc = attendee.dict()
    result = await db.attendees.update_one({"_id": ObjectId(attendee_id)}, {"$set": attendee_doc})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return {"message": "Attendee updated"}

# Delete Attendee
@app.delete("/attendees/{attendee_id}")
async def delete_attendee(attendee_id: str):
    from bson import ObjectId
    result = await db.attendees.delete_one({"_id": ObjectId(attendee_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return {"message": "Attendee deleted"}

# Venue Endpoints
@app.post("/venues")
async def create_venue(venue: Venue):
    venue_doc = venue.dict()
    result = await db.venues.insert_one(venue_doc)
    return {"message": "Venue created", "id": str(result.inserted_id)}

@app.get("/venues")
async def get_venues():
    venues = await db.venues.find().to_list(100)
    for venue in venues:
        venue["_id"] = str(venue["_id"])
    return venues

# Update Venue
@app.put("/venues/{venue_id}")
async def update_venue(venue_id: str, venue: Venue):
    from bson import ObjectId
    venue_doc = venue.dict()
    result = await db.venues.update_one({"_id": ObjectId(venue_id)}, {"$set": venue_doc})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Venue not found")
    return {"message": "Venue updated"}

# Delete Venue
@app.delete("/venues/{venue_id}")
async def delete_venue(venue_id: str):
    from bson import ObjectId
    result = await db.venues.delete_one({"_id": ObjectId(venue_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Venue not found")
    return {"message": "Venue deleted"}

# Booking Endpoints
@app.post("/bookings")
async def create_booking(booking: Booking):
    booking_doc = booking.dict()
    result = await db.bookings.insert_one(booking_doc)
    return {"message": "Booking created", "id": str(result.inserted_id)}

@app.get("/bookings")
async def get_bookings():
    bookings = await db.bookings.find().to_list(100)
    for booking in bookings:
        booking["_id"] = str(booking["_id"])
    return bookings

# Update Booking
@app.put("/bookings/{booking_id}")
async def update_booking(booking_id: str, booking: Booking):
    from bson import ObjectId
    booking_doc = booking.dict()
    result = await db.bookings.update_one({"_id": ObjectId(booking_id)}, {"$set": booking_doc})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking updated"}

# Delete Booking
@app.delete("/bookings/{booking_id}")
async def delete_booking(booking_id: str):
    from bson import ObjectId
    result = await db.bookings.delete_one({"_id": ObjectId(booking_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking deleted"}

# Upload Promotional Video
@app.post("/upload_promo_video/{event_id}")
async def upload_promo_video(event_id: str, file: UploadFile = File(...)):
    content = await file.read()
    video_doc = {
        "event_id": event_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "content": content,
        "uploaded_at": datetime.utcnow()
    }
    result = await db.promo_videos.insert_one(video_doc)
    return {"message": "Promotional video uploaded", "id": str(result.inserted_id)}

# Retrieve Promotional Video
@app.get("/promo_video/{video_id}")
async def get_promo_video(video_id: str):
    from bson import ObjectId
    video = await db.promo_videos.find_one({"_id": ObjectId(video_id)})
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return StreamingResponse(io.BytesIO(video["content"]), media_type=video["content_type"])

# Upload Venue Photo
@app.post("/upload_venue_photo/{venue_id}")
async def upload_venue_photo(venue_id: str, file: UploadFile = File(...)):
    content = await file.read()
    photo_doc = {
        "venue_id": venue_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "content": content,
        "uploaded_at": datetime.utcnow()
    }
    result = await db.venue_photos.insert_one(photo_doc)
    return {"message": "Venue photo uploaded", "id": str(result.inserted_id)}

# Retrieve Venue Photo
@app.get("/venue_photo/{photo_id}")
async def get_venue_photo(photo_id: str):
    from bson import ObjectId
    photo = await db.venue_photos.find_one({"_id": ObjectId(photo_id)})
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return StreamingResponse(io.BytesIO(photo["content"]), media_type=photo["content_type"])