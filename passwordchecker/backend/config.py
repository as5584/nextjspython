from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
API_TITLE = "Password Strength Checker"
API_VERSION = "1.0.0"
CORS_ORIGINS = []
for p in range(3000, 3020):
    CORS_ORIGINS.extend([f"http://localhost:{p}", f"http://127.0.0.1:{p}"])
CORS_ORIGINS = sorted(set(CORS_ORIGINS))
