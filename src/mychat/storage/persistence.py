import json
import os
from pathlib import Path
from .models import Config, Session

DATA_DIR = Path("data")
CONFIG_FILE = DATA_DIR / "config.json"
SESSIONS_DIR = DATA_DIR / "sessions"

def _ensure_dirs():
    DATA_DIR.mkdir(exist_ok=True)
    SESSIONS_DIR.mkdir(exist_ok=True)

def load_config() -> Config:
    _ensure_dirs()
    if not CONFIG_FILE.exists():
        config = Config()
        save_config(config)
        return config
    
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return Config.model_validate_json(f.read())
    except Exception:
        # Fallback if corrupt
        return Config()

def save_config(config: Config):
    _ensure_dirs()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(config.model_dump_json(indent=2))

def load_session(session_id: str) -> Session:
    _ensure_dirs()
    session_file = SESSIONS_DIR / f"chat-{session_id}.json"
    
    if not session_file.exists():
        # Raise error or return new? 
        # Instructions say "Sessions: Save at ...". Doesn't specify load behavior for missing.
        # But usually we want to return a new one or error. 
        # "Loading: Always load JSON into dataclass... type-safe and default values"
        # If ID is provided but file doesn't exist, we probably shouldn't create a blank one with that ID unless requested.
        # But for simplicity, let's assume valid ID is passed or handle gracefully.
        return Session(id=session_id)

    try:
        with open(session_file, "r", encoding="utf-8") as f:
            return Session.model_validate_json(f.read())
    except Exception:
        return Session(id=session_id)

def save_session(session: Session):
    _ensure_dirs()
    session_file = SESSIONS_DIR / f"chat-{session.id}.json"
    with open(session_file, "w", encoding="utf-8") as f:
        f.write(session.model_dump_json(indent=2))

def create_new_session() -> Session:
    session = Session()
    save_session(session)
    return session
