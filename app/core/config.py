import os
from dotenv import load_dotenv

# load server/.env
load_dotenv(os.path.join(os.path.dirname(__file__), os.pardir, ".env"))

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30