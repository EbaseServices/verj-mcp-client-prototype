import instructor
from abc import ABC, abstractmethod

class Client(ABC) :
    def getClient(self, name:str, model:str) -> instructor.client.AsyncInstructor :
        """
        Get the OpenAI client.

        Returns:
            instructor.client.AsyncInstructor: The OpenAI client.
        """
        return instructor.from_provider(f"{name}/{model}")    