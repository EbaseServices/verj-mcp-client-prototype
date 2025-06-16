import instructor
from langfuse.openai import OpenAI
from .client import Client


class OpenAIClient(Client):

    def getClient(self, name: str, model: str) -> instructor.client.AsyncInstructor:
        """
        Get the OpenAI client.

        Returns:
            instructor.client.AsyncInstructor: The OpenAI client.
        """
        instructor.patch(OpenAI())  # integrate with instructor with langfuse to calls to OpenAI can be traced
        return super().getClient(name, model)
