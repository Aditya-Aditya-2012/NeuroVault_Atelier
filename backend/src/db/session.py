# backend/src/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# --------------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------------
# Connection string format: postgresql://user:password@localhost/dbname
# We are connecting to the 'neurovault' db you created earlier.
# (Assuming default user 'your_username' or 'postgres' - change if needed)
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://adityamac@localhost/neurovault"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create a session factory
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_db():
    """
    Dependency helper to get a DB session in route handlers.
    """
    async with AsyncSessionLocal() as session:
        yield session