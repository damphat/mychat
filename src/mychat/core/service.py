import os
from typing import Generator, List, cast
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from mychat.storage.models import Session, Config
from mychat.storage.persistence import (
    save_session,
    load_session,
    create_new_session,
    load_config,
    save_config,
)


class ChatService:
    def __init__(self):
        # Env var check
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            # We raise a helpful error that the UI can catch or display
            raise ValueError(
                "OPENAI_API_KEY is not set. Please set it in your environment or .env file."
            )

        self.client = OpenAI(api_key=self.api_key)
        self.config: Config = load_config()

        # Load last session if exists, otherwise create new
        self.current_session: Session

        if self.config.last_session_id:
            self.current_session = load_session(self.config.last_session_id)
        else:
            self.current_session = create_new_session()
            self.config.last_session_id = self.current_session.id
            save_config(self.config)

    def start_new_session(self):
        self.current_session = create_new_session()
        self.config.last_session_id = self.current_session.id
        save_config(self.config)

    def get_history(self) -> List[dict]:
        """Returns history including system prompt suitable for display if needed"""
        return [m.model_dump() for m in self.current_session.messages]

    def chat(self, user_input: str) -> Generator[str, None, None]:
        self.current_session.add_message("user", user_input)

        # Prepare messages
        messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.config.system}
        ]
        messages.extend(
            [
                cast(ChatCompletionMessageParam, m.model_dump())
                for m in self.current_session.messages
            ]
        )

        try:
            stream = self.client.chat.completions.create(
                model="gpt-3.5-turbo", messages=messages, stream=True
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
