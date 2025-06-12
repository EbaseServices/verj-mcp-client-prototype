import logging
from .client import Client

# Logging
_logger = logging.getLogger(__name__) # module name

class OpenAIClient(Client) :
    pass
    # This class can be extended in the future to include OpenAI-specific methods or properties.
    # For now, it inherits from the base Client class.