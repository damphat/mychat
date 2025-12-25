from mychat.storage.models import Config, Session
from mychat.storage.persistence import load_config, save_config, load_session, save_session, create_new_session, DATA_DIR
import os
import shutil

def setup_module():
    # Clean up data dir before tests
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)

def teardown_module():
    # Clean up after tests
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)

def test_config_persistence():
    # Test default creation
    config = load_config()
    assert config.system == "You are a helpful assistant."
    assert config.last_session_id is None
    
    # Test saving
    config.system = "New system"
    save_config(config)
    
    loaded_config = load_config()
    assert loaded_config.system == "New system"

def test_session_persistence():
    # Test creation
    session = create_new_session()
    assert session.id is not None
    assert len(session.messages) == 0
    
    # Test adding message
    session.add_message("user", "Hello")
    save_session(session)
    
    # Test loading
    loaded_session = load_session(session.id)
    assert len(loaded_session.messages) == 1
    assert loaded_session.messages[0].content == "Hello"
    assert loaded_session.messages[0].role == "user"
