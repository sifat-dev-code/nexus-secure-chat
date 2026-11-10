from database import engine
import models

print("Purono table gulo drop hocche...")
models.Base.metadata.drop_all(bind=engine)

print("Notun updated table gulo toiri hocche...")
models.Base.metadata.create_all(bind=engine)

print("Database reset ekdom successful!")