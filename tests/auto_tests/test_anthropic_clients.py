import pytest
from pydantic import BaseModel
from instructor.exceptions import InstructorRetryException
from mcp_client.llm_client.supported_clients import SupportedClient
from mcp_client.errors.errors import ClientError


@pytest.fixture
def anthropic_env(monkeypatch): 
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")
    monkeypatch.setenv("ANTHROPIC_DEFAULT_MODEL", "test-anthropic-model")


def test_anthropic_enum_creation(): 
    client = SupportedClient.ANTHROPIC
    assert client.name == "anthropic"
    assert client._api == "ANTHROPIC_API_KEY"
    assert client._defaultModel == "ANTHROPIC_DEFAULT_MODEL"


def test_anthropic_get_api_key_and_model(anthropic_env): 
    client = SupportedClient.ANTHROPIC
    assert client.getAPIKey() == "test-anthropic-key"
    assert client.getModel() == "test-anthropic-model"


def test_anthropic_missing_api_key(monkeypatch): 
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    client = SupportedClient.ANTHROPIC
    with pytest.raises(ClientError):
        client.getAPIKey()


def test_anthropic_missing_model(monkeypatch): 
    monkeypatch.delenv("ANTHROPIC_DEFAULT_MODEL", raising=False)
    client = SupportedClient.ANTHROPIC
    with pytest.raises(ClientError):
        client.getModel()
        
def test_anthropic__call_auth_failure(anthropic_env): 
    class Person(BaseModel):
        name: str
    client = SupportedClient.ANTHROPIC
    with pytest.raises(InstructorRetryException) as exc_info:
        result = client.getClient().chat.completions.create(response_model=Person, messages=[{"role": "user", "content": "Hello, world!"}], max_retries=0)
    assert exc_info.value.args[0].status_code == 401
    assert "invalid x-api-key" in exc_info.value.args[0].message
