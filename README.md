# Pokie Dokie Backend

A FastAPI-based backend for a poker planning application.

## Features

- JWT-based authentication
- Real-time updates using WebSocket
- Session management
- Story tracking
- Voting system with timer
- Vote revealing and final estimate calculation

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd pokie-dokie-back
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following content:
```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/pokie_dokie
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Create the database:
```bash
createdb pokie_dokie
```

6. Initialize the database:
```bash
python -c "from app.db.init_db import init_db; import asyncio; asyncio.run(init_db())"
```

## Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## WebSocket Connection

Connect to the WebSocket endpoint:
```
ws://localhost:8000/ws/{session_id}?token={jwt_token}
```

## Testing

Run the tests:
```bash
pytest
```

## Project Structure

```
pokie-dokie-back/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── websocket.py
│   ├── db/
│   │   ├── init_db.py
│   │   └── session.py
│   ├── models/
│   │   ├── base.py
│   │   └── models.py
│   ├── schemas/
│   │   └── schemas.py
│   └── main.py
├── tests/
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

## License

MIT 