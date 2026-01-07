import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
service_key = os.getenv("SUPABASE_SERVICE_KEY")

print(f"DATABASE_URL_EXISTS={bool(db_url)}")
print(f"SERVICE_KEY_EXISTS={bool(service_key)}")
