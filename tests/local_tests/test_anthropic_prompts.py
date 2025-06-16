import pytest
import os
import dotenv
from pydantic import BaseModel
from langfuse import observe
from mcp_client.llm_client.supported_clients import SupportedClient


@pytest.fixture
def anthropic_env():
    # These tests can only be run locally - that is with a local .env file (which obviously should not be committed)
    dotenv.load_dotenv()


class Person(BaseModel):
    name: str
    age: int


@observe
def test_anthropic_simple_prompt(anthropic_env):
    assert os.getenv("ANTHROPIC_API_KEY", None) is not None
    assert os.getenv("ANTHROPIC_DEFAULT_MODEL", None) is not None

    client = SupportedClient.ANTHROPIC
    result = client.getClient().chat.completions.create(response_model=Person, messages=[{"role": "user", "content": "Janet would be 25 on her next birthday."}], max_retries=1)

    assert isinstance(result, Person)
    assert result.name == "Janet"
    assert result.age == 24
