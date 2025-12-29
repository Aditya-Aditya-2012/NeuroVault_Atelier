# NeuroVault Atelier: MVP Roadmap & Progress
## Phase 1: Identity & Security (COMPLETED)
[x] Project Initialization: Set up FastAPI, PostgreSQL, and project structure.
[x] User Authentication: Implemented JWT-based login and registration.
[x] Dependency Injection: Created get_current_user to protect routes.
[x] Environment Security: Moved secrets to .env.
## Phase 2: Image Management (COMPLETED)
[x] Secure Uploads: Created endpoint to save images with UUID-renaming to prevent collisions.
[x] Database Linkage: Images are correctly associated with the owner_id.
[x] Atomic Transactions: Implemented file-system cleanup if the database commit fails.
[x] Gallery Logic: Created GET /my-images with ownership filtering.
[x] Alembic Integration: Initialized database migrations to handle schema changes.
## Phase 3: The AI Atelier (IN PROGRESS)
[x] Task Infrastructure: Set up Redis as a broker and Celery as the worker engine.
[x] Asynchronous Pipeline: API successfully triggers background tasks using .delay().
[x] Task Tracking: Added is_processed column to track worker progress via Alembic.
[x] Status Polling: Created GET /images/{id}/status with security checks.
[ ] Real Image Transformation: Replace time.sleep(10) with Pillow to generate a grayscale version of the image.
[ ] Multi-Image Logic: Update the AI_Tasks schema to support combining 1-3 source images.
[ ] Keyword Indexing: Add a keywords column and a background task to tag images for search.
[ ] Result Lineage: Implement the source_filenames column in the Outputs table.
## Phase 4: Serving & Discovery (UPCOMING)
[ ] Static Assets: Configure FastAPI to serve the uploads and generated folders.
[ ] Semantic Search: Build a search endpoint that filters images by keywords (e.g., "sunset").
[ ] Full Gallery View: Create a unified API response that returns an original image alongside all its generated "AI Art" variations.
## Phase 5: The Frontend & Deployment (FUTURE)
[ ] Frontend MVP: Build a React/Vue interface for uploading, searching, and triggering "Alchemy" combinations.
[ ] Stable Diffusion Integration: Replace Pillow with actual AI model calls (local or API).
[ ] Dockerization: Containerize the API, Worker, Redis, and Postgres for easy deployment.
## Current Workdir Status
Branch: feature/image-management-and-celery
Last Successful Test: GET /images/{id}/status returns is_processed: true after the 10-second Celery sleep.
