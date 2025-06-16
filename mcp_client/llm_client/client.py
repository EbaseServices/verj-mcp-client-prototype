import instructor
from abc import ABC

class Client(ABC) :
    def getClient(self, name:str, model:str) -> instructor.client.AsyncInstructor :
        """
        Get the client for this llm.

        Returns:
            instructor.client.AsyncInstructor: The OpenAI client.
        """
        return instructor.from_provider(f"{name}/{model}")    