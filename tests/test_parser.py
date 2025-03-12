import pytest
from pubmed_fetcher.parser import extract_company_authors  

def test_extract_company_authors():
    """Test parsing author affiliations."""
    data = {"authors": [{"name": "John Doe", "affiliation": "Harvard University"}]}
    parsed = extract_company_authors(data["authors"])
    assert parsed == []  # Harvard University is not a company

def test_extract_company_authors_with_company():
    """Test identifying company-affiliated authors."""
    data = {"authors": [{"name": "Alice Smith", "affiliation": "XYZ Pharma Inc."}]}
    parsed = extract_company_authors(data["authors"])
    assert parsed == [("Alice Smith", "xyz pharma inc.")]
