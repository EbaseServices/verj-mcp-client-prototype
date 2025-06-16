import instructor
from enum import Enum
import os
from typing import Any, Optional, Type
from ..utilities import helpers
from ..errors.errors import ClientError
from .client import Client
from .client_openai import OpenAIClient
from .client_anthropic import AnthropicClient

class SupportedClient(Enum) :

    OPENAI = "openai", "OPENAI_DEFAULT_MODEL", "OPENAI_API_KEY", OpenAIClient  # OpenAI LLM
    ANTHROPIC = "anthropic", "ANTHROPIC_DEFAULT_MODEL", "ANTHROPIC_API_KEY", AnthropicClient  # Anthropic LLM


    def __init__(self, llm_name:str, default_model:str, api_key:str, client_class:Type[Client]) :
        """
        Initialize the SupportedClients enum with the LLM name, API key environment variable, and model environment variable.

        Args:
            llm_name (str): The name of the LLM.
            default_model (str): The environment variable for the model.
            api_key_name (str): The environment variable for the API key.
            client_class (Type[Client]): The class of the client for the LLM.
        """
        self._llm_name:str = llm_name
        self._api_key:str = api_key
        self._default_model:str = default_model
        self._client_class:Type[Client] = client_class

    
    def getClient(self, *args: Any, **kwargs: Any) -> instructor.client.AsyncInstructor:
        """
        Returns the client for the LLM based on the enum value.

        Raises:
            ClientError: If the client is not found.

        Returns:
            Client: The client for the LLM.
        """
        return self._clientClass(*args, **kwargs).getClient(self.name, self.getModel())
    
    
    def getAPIKey(self) -> str:
        """
        Returns the API key for the LLM

        Raises:
            ClientError: If the API key is not found in the environment variable.

        Returns:
            str: The API key for the LLM.
        """
        key:Optional[str] = os.getenv(self._api, None)
        if key is None or helpers.isEmpty(key) :
            raise ClientError(f"SupportedClients::API key for {self.name} not found in environment variable {self._api}.")
        return key
    

    def getModel(self) -> str:
        """
        Returns the model for the LLM

        Raises:
            ClientError: If the model is not found in the environment variable.

        Returns:
            str: The model for the LLM.
        """
        model:Optional[str] = os.getenv(self._defaultModel, None)
        if model is None or helpers.isEmpty(model) :
            raise ClientError(f"SupportedClients::Model for {self.name} not found in environment variable {self._defaultModel}.")
        return model
    
    
    @property
    def name(self) -> str:
        """Get the name of the LLM."""
        return self._llm_name
    
    
    @property
    def _api(self) -> str:
        """Get the name of the environment variable for the API key."""
        return self._api_key
    
    
    @property
    def _defaultModel(self) -> str:
        """Get the name of the environment variable for the model."""
        return self._default_model
    
    @property
    def _clientClass(self) -> Type[Client]:
        """Get the class of the client for the LLM."""
        return self._client_class