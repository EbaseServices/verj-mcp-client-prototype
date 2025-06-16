import pytest
from pydantic import BaseModel
from instructor.exceptions import InstructorRetryException
from mcp_client.llm_client.supported_clients import SupportedClient
from mcp_client.errors.errors import ClientError

@pytest.fixture
def openai_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("OPENAI_DEFAULT_MODEL", "test-openai-model")


def test_openai_get_api_key_and_model(openai_env):
    client = SupportedClient.OPENAI
    assert client.getAPIKey() == "test-openai-key"
    assert client.getModel() == "test-openai-model"


def test_openai_enum_creation():
    client = SupportedClient.OPENAI
    assert client.name == "openai"
    assert client._api == "OPENAI_API_KEY"
    assert client._defaultModel == "OPENAI_DEFAULT_MODEL"


def test_openai_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    client = SupportedClient.OPENAI
    with pytest.raises(ClientError):
        client.getAPIKey()


def test_openai_missing_model(monkeypatch):
    monkeypatch.delenv("OPENAI_DEFAULT_MODEL", raising=False)
    client = SupportedClient.OPENAI
    with pytest.raises(ClientError):
        client.getModel()


def test_openai_call_auth_failure(openai_env):
    class Person(BaseModel):
        name: str
    client = SupportedClient.OPENAI
    with pytest.raises(InstructorRetryException) as exc_info:
        result = client.getClient().chat.completions.create(response_model=Person, messages=[{"role": "user", "content": "Hello, world!"}], max_retries=0)
    assert exc_info.value.args[0].status_code == 401
    assert "Incorrect API key provided" in exc_info.value.args[0].message
    assert exc_info.value.args[0].type == "invalid_request_error"
    assert exc_info.value.args[0].code == "invalid_api_key"


        