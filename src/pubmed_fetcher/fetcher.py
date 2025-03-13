# import requests
# import logging

# BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
# DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

# logging.basicConfig(level=logging.INFO)


# def fetch_pubmed_papers(query: str, max_results: int = 10) -> dict:
#     """Fetches research papers from PubMed based on the query."""
#     params = {
#         "db": "pubmed",
#         "term": query,
#         "retmode": "json",
#         "retmax": max_results,
#     }

#     response = requests.get(BASE_URL, params=params)
#     if response.status_code != 200:
#         logging.error(f"Failed to fetch data: {response.text}")
#         return {}  # Return an empty dictionary instead of an empty list

#     paper_ids = response.json().get("esearchresult", {}).get("idlist", [])

#     return fetch_paper_details(paper_ids) if paper_ids else {}


# def fetch_paper_details(paper_ids: list[str]) -> dict:
#     """Fetches details of papers using PubMed IDs."""
#     if not paper_ids:
#         return {}

#     params = {
#         "db": "pubmed",
#         "id": ",".join(paper_ids),
#         "retmode": "json",
#     }

#     response = requests.get(DETAILS_URL, params=params)
#     if response.status_code != 200:
#         logging.error(f"Failed to fetch paper details: {response.text}")
#         return {}

#     data = response.json().get("result", {})

#     return {paper_id: data[paper_id] for paper_id in paper_ids if paper_id in data}


# if __name__ == "__main__":
#     print(fetch_pubmed_papers("cancer research"))  # 🔍 Debugging print


import requests
import logging

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

logging.basicConfig(level=logging.INFO)


def fetch_pubmed_papers(query: str, max_results: int = 10) -> list:
    """Fetches research papers from PubMed based on the query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch data: {e}")
        return []

    paper_ids = response.json().get("esearchresult", {}).get("idlist", [])
    return fetch_paper_details(paper_ids) if paper_ids else []


def fetch_paper_details(paper_ids: list) -> list:
    """Fetches details of papers using PubMed IDs."""
    if not paper_ids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "json",
    }

    try:
        response = requests.get(DETAILS_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch paper details: {e}")
        return []

    data = response.json().get("result", {})
    # return {paper_id: data[paper_id] for paper_id in paper_ids if paper_id in data}

    return [
        {
            "uid": paper_id,
            "title": data.get(paper_id, {}).get("title", "N/A"),
            "pubdate": data.get(paper_id, {}).get("pubdate", "N/A"),
            "authors": data.get(paper_id, {}).get("authors", []),
            "affiliations": data.get(paper_id, {}).get("affiliations", ""),
        }
        for paper_id in paper_ids if paper_id in data
    ]
    
if __name__ == "__main__":
    print(fetch_pubmed_papers("cancer research"))

# import requests
# import logging

# BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
# DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

# logging.basicConfig(level=logging.INFO)


# def fetch_pubmed_papers(query: str, max_results: int = 10) -> dict:
#     """Fetches research papers from PubMed based on the query."""
#     params = {
#         "db": "pubmed",
#         "term": query,
#         "retmode": "json",
#         "retmax": max_results,
#     }

#     response = requests.get(BASE_URL, params=params)
#     if response.status_code != 200:
#         logging.error(f"Failed to fetch data: {response.text}")
#         return {}  # Return an empty dictionary instead of an empty list

#     paper_ids = response.json().get("esearchresult", {}).get("idlist", [])

#     return fetch_paper_details(paper_ids) if paper_ids else {}


# def fetch_paper_details(paper_ids: list[str]) -> dict:
#     """Fetches details of papers using PubMed IDs."""
#     if not paper_ids:
#         return {}

#     params = {
#         "db": "pubmed",
#         "id": ",".join(paper_ids),
#         "retmode": "json",
#     }

#     response = requests.get(DETAILS_URL, params=params)
#     if response.status_code != 200:
#         logging.error(f"Failed to fetch paper details: {response.text}")
#         return {}

#     data = response.json().get("result", {})

#     return {paper_id: data[paper_id] for paper_id in paper_ids if paper_id in data}


# if __name__ == "__main__":
#     print(fetch_pubmed_papers("cancer research"))  # 🔍 Debugging print
