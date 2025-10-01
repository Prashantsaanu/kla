from app.database import engine, Base
from app.models import User

# Create all tables
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
