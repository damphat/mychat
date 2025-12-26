from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import uuid
from datetime import datetime


class Config(BaseModel):
    system: str = "You are a helpful assistant."
    last_session_id: Optional[str] = None


class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str


class Session(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    messages: List[Message] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)

    def add_message(self, role: str, content: str):
        self.messages.append(Message(role=role, content=content))
