import os
from openai import OpenAI
from typing import Generator, Optional, List
from mychat.storage.models import Session, Config
from mychat.storage.persistence import save_session, load_session, create_new_session, load_config, save_config

class ChatService:
    def __init__(self):
        # Env var check
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            # We raise a helpful error that the UI can catch or display
            raise ValueError("OPENAI_API_KEY is not set. Please set it in your environment or .env file.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.config = load_config()
        self.current_session: Optional[Session] = None
        
        # Load last session if exists
        if self.config.last_session_id:
             self.current_session = load_session(self.config.last_session_id)
        else:
             self.start_new_session()

    def start_new_session(self):
        self.current_session = create_new_session()
        self.config.last_session_id = self.current_session.id
        save_config(self.config)

    def get_history(self) -> List[dict]:
        """Returns history including system prompt suitable for display if needed"""
        if not self.current_session:
            return []
        return [m.model_dump() for m in self.current_session.messages]

    def chat(self, user_input: str) -> Generator[str, None, None]:
        if not self.current_session:
            self.start_new_session()
            
        self.current_session.add_message("user", user_input)
        
        # Prepare messages
        messages = [{"role": "system", "content": self.config.system}]
        messages.extend([m.model_dump() for m in self.current_session.messages])

        try:
            stream = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True
            )

            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
            
            self.current_session.add_message("assistant", full_response)
            save_session(self.current_session)
            
        except Exception as e:
            # Graceful error handling
            yield f"\n[Error: {str(e)}]"
