import pytest
from unittest.mock import patch
from pubmed_fetcher.fetcher import fetch_pubmed_papers


@patch("pubmed_fetcher.fetcher.requests.get")
def test_fetch_pubmed_data(mock_get):
    """Test fetching PubMed data with a mock API response."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "esearchresult": {"idlist": ["12345"]},
        "result": {"12345": {"title": "Test Article"}},
    }

    result = fetch_pubmed_papers("cancer")
    print(result)
    assert "12345" in result[0]["uid"]  # ✅ Expecting dictionary with paper ID keys
    assert result[0]["title"] == "Test Article"


@patch("pubmed_fetcher.fetcher.requests.get")
def test_fetch_pubmed_data_fail(mock_get):
    """Test failed API call."""
    mock_get.return_value.status_code = 500
    result = fetch_pubmed_papers("invalid_query")
    assert result == []  # ✅ Expect an empty dictionary, not None
