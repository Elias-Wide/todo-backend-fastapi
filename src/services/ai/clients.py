from abc import ABC, abstractmethod
from typing import Any

from groq import Groq
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class BaseAiClient(ABC):
    """Abstract Base Class for all AI-related service clients."""

    def __init__(self, key: str, model: str):
        self.api_key = key
        self.model = model

    @abstractmethod
    def get_client(self) -> Any:
        """Initialize and return the specific provider client."""
        pass


class BaseSpeechClient(BaseAiClient, ABC):
    """Abstract client for Speech-to-Text (STT) services."""

    def __init__(self, key: str, model: str):
        super().__init__(key, model)
        self.client = self.get_client()

    @abstractmethod
    def transcribe(self, audio_path: str) -> str:
        """Convert audio file to text transcription."""
        pass


class GroqSpeechClient(BaseSpeechClient):
    """Groq implementation for audio transcription using Whisper."""

    def get_client(self) -> Groq:
        """Return a native Groq client instance."""
        return Groq(api_key=self.api_key)

    def transcribe(self, audio_path: str) -> str:
        """Transcribe audio file using Groq's API."""
        with open(audio_path, 'rb') as file:
            return self.client.audio.transcriptions.create(
                file=(audio_path, file.read()), model=self.model
            ).text


class BaseTextClient(BaseAiClient, ABC):
    """Abstract client for Large Language Models (LLM)."""

    def __init__(self, key: str, model: str, system_prompt: str):
        super().__init__(key, model)
        self.system_prompt = system_prompt
        self.llm = self.get_client()

    @abstractmethod
    def send_request(self, text: str) -> str:
        """Send a text prompt to the AI model and return response."""
        pass


class GroqTextClient(BaseTextClient):
    """Groq implementation for text generation using LangChain."""

    def __init__(self, key: str, model: str, system_prompt: str):
        super().__init__(key, model, system_prompt)
        self.prompt_template = self._create_template()
        self.chain = self.prompt_template | self.llm

    def get_client(self) -> ChatGroq:
        """Return a ChatGroq instance for LangChain integration."""
        return ChatGroq(groq_api_key=self.api_key, model_name=self.model)

    def _create_template(self) -> ChatPromptTemplate:
        """Create a standard ChatPromptTemplate for LLM requests."""
        return ChatPromptTemplate.from_messages(
            [('system', self.system_prompt), ('human', '{text}')]
        )

    def send_request(self, text: str) -> str:
        """Invoke the LangChain sequence and return string content."""
        response = self.chain.invoke({'text': text})
        return str(response.content)
