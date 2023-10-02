import pytest
from unittest.mock import AsyncMock, patch
from gpt.worker import gpt_handler

@pytest.mark.asyncio
async def test_gpt_handler():
    # Mocking Redis get method to return a sample scraped content
    mock_redis = AsyncMock()
    mock_redis.get.return_value = "sample scraped content"

    # Mocking the GPT function to return a sample result
    with patch('gpt.worker.your_gpt_function', return_value="sample gpt result") as mock_gpt_function:
        result = await gpt_handler({"redis": mock_redis}, "sample_job_id")

    # Assertions
    mock_redis.get.assert_called_once_with("sample_job_id")
    mock_gpt_function.assert_called_once_with("sample scraped content")
    assert result == "sample gpt result"
