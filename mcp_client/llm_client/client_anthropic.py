import instructor
from opentelemetry.instrumentation.anthropic import AnthropicInstrumentor
from .client import Client


class AnthropicClient(Client):

    def getClient(self, name: str, model: str) -> instructor.client.AsyncInstructor:
        """
        Get the client for anthropic-based models.

        Returns:
            instructor.client.AsyncInstructor: The OpenAI client.
        """
        AnthropicInstrumentor().instrument()
        return super().getClient(name, model)
