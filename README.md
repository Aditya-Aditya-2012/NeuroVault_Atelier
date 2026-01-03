🎨 NeuroVault Atelier

NeuroVault Atelier is a local-first, privacy-focused "AI Art Vault" that allows users to upload high-resolution landscapes, automatically tag them using zero-shot classification (CLIP), and blend them into new artistic creations using an asynchronous "Alchemy" pipeline.

Designed as a Full-Stack ML Application, it demonstrates a decoupled architecture where heavy AI inference is offloaded to background workers, ensuring a responsive user experience even on local hardware (MacBook M2).

🛠 Tech Stack & Architecture

Backend (The Brain)

FastAPI: High-performance, async Python web framework. Handles authentication (OAuth2/JWT), file management, and API orchestration.

SQLAlchemy 2.0 (Async): Modern ORM for database interactions, utilizing asyncpg for non-blocking I/O.

Alembic: Database migration tool for version-controlling the schema.

Pydantic: Data validation and serialization schemas.

The "Atelier" Engine (The Muscles)

Celery: Distributed task queue to manage long-running AI jobs (Auto-tagging, Image Stitching).

Redis: In-memory message broker acting as the "waiting room" for tasks between FastAPI and Celery.

PyTorch (MPS): Deep learning framework optimized for Apple Silicon (Metal Performance Shaders).

Hugging Face Transformers: Runs the CLIP model for zero-shot image classification ("The Automatic Librarian").

Pillow: Image processing library for stitching and pixel-level manipulation.

Frontend (The Gallery)

React (Vite): Blazing fast SPA framework.

TypeScript: For type-safe interactions with the backend API.

Tailwind CSS v4: Utility-first styling with a custom "Glassmorphism" design system.

Framer Motion: For fluid layout transitions (Masonry grid) and micro-interactions.

TanStack Query: Managing server state, caching, and polling for task updates.

🏗️ System Architecture

The application follows a Decoupled Micro-service Architecture (monolithic repo):

Client (React): Sends an upload request or an "Alchemy" trigger (combine 3 images).

FastAPI: Authenticates the user, saves the file to disk (backend/data/uploads), and pushes a "Job Ticket" to Redis.

Redis: Queues the task (e.g., auto_tag_image or process_multi_alchemy).

Celery Worker:

Picks up the task.

Loads the AI Model (CLIP) onto the M2 GPU (MPS).

Processes the image.

Updates the PostgreSQL database with new tags or output paths.

Saves generated results to backend/data/generated.

Client Polling: The frontend polls the API to see if the is_processed flag has flipped to True, then renders the new data.

🗄️ Database Schema

We use PostgreSQL with specific features like Arrays and Enums.

Entity Relationship Diagram (ERD)

erDiagram
    User ||--o{ Image : uploads
    User ||--o{ AITask : initiates
    AITask ||--|{ Output : produces
    
    User {
        int id PK
        string email
        string hashed_password
    }

    Image {
        int id PK
        int owner_id FK
        string filename
        string file_path
        jsonb keywords "['sunset', 'mountain']"
        bool is_processed
    }

    AITask {
        int id PK
        int user_id FK
        int[] input_image_ids
        string prompt
        enum status "PENDING, PROCESSING, COMPLETED"
    }

    Output {
        int id PK
        int task_id FK
        string gen_file_path
        string[] source_filenames
    }


Table Details

users: Stores credentials. Passwords are hashed with bcrypt.

images: The "Source" assets.

keywords: A PostgreSQL ARRAY(String) column. Populated by the CLIP model.

is_processed: Boolean flag. False = "Scanning...", True = "Ready".

ai_tasks: Represents an "Alchemy" request.

input_image_ids: An array of integers, linking to multiple source images (1-3).

status: A custom Postgres ENUM type (taskstatus).

outputs: The generated "Child" images.

source_filenames: An array of strings tracking exactly which files created this result (Data Lineage).

📂 Directory Structure

NeuroVault_Atelier/
├── alembic/                # Database migration scripts
├── backend/
│   ├── data/               # Local file storage (Git-ignored)
│   │   ├── uploads/
│   │   └── generated/
│   ├── src/
│   │   ├── ai_engine/      # Pure AI Logic (Separated from Tasks)
│   │   │   ├── librarian.py # CLIP Model Class
│   │   │   └── artisan.py   # (Planned) Diffusers/Stitching Logic
│   │   ├── api/            # FastAPI Routes
│   │   │   ├── auth.py     # Login/Signup
│   │   │   ├── images.py   # Upload, Gallery, Alchemy
│   │   │   └── deps.py     # Auth Dependencies
│   │   ├── core/           # Config (Celery, Security)
│   │   ├── db/             # Database Session & Base
│   │   ├── models/         # SQLAlchemy Tables
│   │   ├── schemas/        # Pydantic Models
│   │   ├── tasks/          # Celery Task Definitions
│   │   └── main.py         # App Entrypoint
│   └── tests/
├── frontend/               # Vite + React Project
│   ├── src/
│   │   ├── api/            # Axios Service Layer
│   │   ├── components/     # UI Components (GalleryGrid, AuthModal)
│   │   └── features/       # (Planned) Domain-specific logic
├── .env                    # Secrets (DB URL, Secret Key)
└── docker-compose.yml      # (Planned) Containerization


🚀 Running the Project

Prerequisites

Python 3.10+ (Virtual Environment recommended)

Node.js 18+ (via NVM)

PostgreSQL (Running locally via Brew or Docker)

Redis (Running locally via Brew or Docker)

1. Backend & Worker

# Terminal 1: Start FastAPI
source venv/bin/activate
uvicorn backend.src.main:app --reload

# Terminal 2: Start Celery (Solo pool for Mac M2 stability)
source venv/bin/activate
celery -A backend.src.core.celery_app worker --loglevel=info -Q ai_queue --pool=solo


2. Frontend

# Terminal 3: Start Vite
cd frontend
npm run dev


3. Database Migrations

If you modify models, update the schema:

alembic revision --autogenerate -m "describe_change"
alembic upgrade head


🔮 Current Status (MVP)

Authentication: ✅ Working (JWT)

Uploads: ✅ Working (UUID renaming + Atomic Transactions)

Auto-Tagging: ✅ Working (CLIP on M2 GPU)

Gallery: ✅ Working (Masonry Grid + Optimistic UI)

Alchemy (Stitching): ✅ Working (Horizontal Stitching of 3 images)

Search: ✅ Working (DB-level filtering by keyword & owner)