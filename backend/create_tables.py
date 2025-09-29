from app.core.database import engine, Base
from app.models.task import Task

Base.metadata.create_all(bind=engine)
print("Tables created successfully")
