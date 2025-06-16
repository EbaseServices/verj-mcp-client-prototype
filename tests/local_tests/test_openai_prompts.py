import pytest
import dotenv
import os
from langfuse import observe
from pydantic import BaseModel
from mcp_client.llm_client.supported_clients import SupportedClient

@pytest.fixture
def openai_env():
    # These tests can only be run locally - that is with a local .env file (which obviously should not be committed)
    dotenv.load_dotenv()

@observe
def test_openai_simple_prompt(openai_env):
    assert os.getenv("OPENAI_API_KEY", None) is not None
    assert os.getenv("OPENAI_DEFAULT_MODEL", None) is not None
    client = SupportedClient.OPENAI
    
    class Person(BaseModel):
        name: str
        age: int
    result = client.getClient().chat.completions.create(response_model=Person, messages=[{"role": "user", "content": "Janet would be 25 on her next birthday."}], max_retries=1)
    assert isinstance(result, Person)
    assert result.name == "Janet"
    assert result.age == 24



        