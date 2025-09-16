# 🧪 Mini Event Management System

A complete event management application demonstrating clean architecture, scalability, and data integrity. Built with **FastAPI** (backend) and **Next.js** (frontend) following all assignment requirements.

## Assignment Requirements Fulfilled

✅ **All Core API Endpoints Implemented:**
- `POST /events` - Create events with name, location, start_time, end_time, max_capacity
- `GET /events` - List all upcoming events  
- `POST /events/{event_id}/register` - Register attendees with overbooking prevention
- `GET /events/{event_id}/attendees` - Get registered attendees with pagination

✅ **Frontend Requirements:**
- Next.js with Shadcn UI components
- Responsive design and user-friendly experience

✅ **Technical Requirements:**
- **Database**: SQLite with SQLAlchemy ORM
- **Architecture**: Clean architecture with separation of concerns (models, services, repositories, routes)
- **Async Implementation**: Full async/await support throughout the application
- **Input Validation**: Comprehensive validation with meaningful error messages
- **Data Integrity**: Prevents overbooking and duplicate email registrations
- **Timezone Management**: Events created in IST with timezone conversion support

✅ **Bonus Features Implemented:**
- ✅ Pagination on attendee lists
- ✅ Swagger/OpenAPI documentation at `/docs`

## 🛠 Tech Stack

**Backend (FastAPI):**
- FastAPI with Python 3.8+
- SQLite database with SQLAlchemy async ORM
- Pydantic for data validation
- Async/await throughout the application
- Automatic OpenAPI/Swagger documentation

**Frontend (Next.js):**
- Next.js 15 with TypeScript
- Shadcn UI components with Tailwind CSS
- React Hook Form + Zod validation
- Timezone handling with date-fns



## 🚀 Quick Start & Setup Instructions

### Prerequisites
- Python 3.8+ 
- Node.js 18+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/VenkataRohan/omnify_assignment.git
cd omnify_assignment
```

### 2. Backend Setup (FastAPI)
```bash
cd backend

# Copy .env.example to .env
cp .env.example .env  # On Windows: copy .env.example .env

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
fastapi dev app/main.py
```

**Backend will be available at:**
- Main API: `http://localhost:8000`
- **Swagger Documentation**: `http://localhost:8000/docs` 📖
- Alternative docs: `http://localhost:8000/redoc`

### 3. Frontend Setup (Next.js)
```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

**Frontend will be available at:** `http://localhost:3000`

## API Endpoints (Assignment Requirements)

### Core Endpoints

#### 1. Create Event
```http
POST /api/v1/events
Content-Type: application/json

{
  "name": "Tech Conference 2025",
  "location": "Hyderabad, India", 
  "start_time": "2024-12-15T10:00:00",
  "end_time": "2024-12-15T18:00:00",
  "max_capacity": 100
}
```

#### 2. Get All Events
```http
GET /api/v1/events
```

#### 3. Register Attendee
```http
POST /api/v1/events/{event_id}/attendees
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```

#### 4. Get Event Attendees (with Pagination)
```http
GET /api/v1/events/{event_id}/attendees?page=1&size=10
```

### Sample cURL Commands or use (http://localhost:8000/docs for Swagger Docs)

```bash
# Create a new event
curl --location -X POST "http://localhost:8000/api/v1/events" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Meetup",
    "location": "Hyderabad, India",
    "start_time": "2025-10-03T14:20:00.000Z",
    "end_time": "2025-10-04T14:20:00.000Z",
    "max_capacity": 10
  }'

# Get all events
# Get events
curl --location "http://localhost:8000/api/v1/events"

# Register an attendee
curl --location -X POST "http://localhost:8000/api/v1/events/1/attendees" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "rohan",
    "email": "rohan@example.com"
  }'

# Get attendees with pagination
curl --location "http://localhost:8000/api/v1/events/1/attendees?page=1&size=10"
```


## 🏗 Project Architecture & Structure

**Clean Architecture Implementation:**

```
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # Application entry point
│   │   ├── api/v1/            # API route handlers (Controllers)
│   │   │   ├── router.py      # Main router
│   │   │   └── endpoints/     # Endpoint definitions
│   │   ├── models/            # Database models (SQLAlchemy)
│   │   ├── schemas/           # Pydantic schemas (Data validation)
│   │   ├── services/          # Business logic layer
│   │   ├── repositories/      # Data access layer (Repository pattern)
│   │   ├── core/              # Core configurations
│   │   ├── middleware/        # Custom middleware
│   │   └── db/                # Database configuration
│   ├── app.db                 # SQLite database file
│   └── requirements.txt       # Python dependencies
├── frontend/                   # Next.js Frontend
│   ├── src/
│   │   ├── app/               # Next.js app router
│   │   ├── components/        # React components (Shadcn UI)
│   │   ├── types/             # TypeScript definitions
│   │   ├── services/          # API service layer
│   │   ├── contexts/          # React contexts (Timezone)
│   │   └── lib/               # Utility functions
│   └── package.json
└── README.md
```

**Architecture Principles Applied:**
- **Separation of Concerns**: Models, Services, Repositories, and Controllers are clearly separated
- **Dependency Injection**: Repository pattern with dependency injection
- **Data Validation**: Pydantic schemas for request/response validation
- **Error Handling**: Centralized error handling with meaningful messages
- **Async/Await**: Full async implementation for better performance

## ⚙️ Configuration & Environment

**Backend** (create `backend/.env`):
```env
# Environment Configuration
ENVIRONMENT=development
DEBUG=True

# Database Configuration
DATABASE_URL=sqlite+aiosqlite:///./app.db

# API Configuration
API_PREFIX=/api
API_VERSION=v1


# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
ALLOWED_METHODS=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
ALLOWED_HEADERS=["*"]


# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

```

**Frontend** (create `frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🗄️ Database Schema

**SQLite Database with SQLAlchemy ORM:**

### Events Table
- `id` (Primary Key)
- `name` (String, required)
- `location` (String, required)  
- `start_time` (DateTime, required)
- `end_time` (DateTime, required)
- `max_capacity` (Integer, required)
- `created_at` (DateTime, auto-generated)
- `updated_at` (DateTime, auto-updated)

### Attendees Table  
- `id` (Primary Key)
- `name` (String, required)
- `email` (String, required, unique per event)
- `event_id` (Foreign Key to Events)
- `created_at` (DateTime, auto-generated)

**Constraints:**
- Unique constraint on (email, event_id) to prevent duplicate registrations
- Capacity checking before attendee registration

##  Key Implementation Details

### Data Integrity & Business Logic
- **Overbooking Prevention**: Validates max_capacity before attendee registration
- **Duplicate Prevention**: Unique constraint on email per event
- **Input Validation**: Comprehensive validation using Pydantic schemas
- **Error Handling**: Meaningful error messages with proper HTTP status codes

### Timezone Management
- **Events created in IST timezone**
- **Frontend timezone conversion**: Automatically detects user timezone
- **Manual timezone selection**: Users can switch between timezones
- **Consistent datetime handling**: All timestamps properly converted

### Performance & Scalability
- **Async/Await**: Full async implementation throughout the backend
- **Pagination**: Implemented on attendee lists (default: page=1, size=10)
- **Database Optimization**: Proper indexing and efficient queries
- **Connection Pooling**: SQLAlchemy async session management

### Code Quality
- **Clean Architecture**: Separation of concerns with services, repositories, models
- **Type Safety**: Full TypeScript implementation on frontend
- **DRY Principle**: Reusable components and utility functions
- **Naming Conventions**: Clear, descriptive naming throughout