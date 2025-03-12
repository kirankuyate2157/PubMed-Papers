import re


def extract_company_authors(author_affiliations: list[dict]) -> list[tuple]:
    """
    Identifies authors affiliated with pharmaceutical or biotech companies.
    Returns a list of tuples (Author Name, Company Name).
    """
    non_academic_authors = []
    company_keywords = ["pharma", "biotech", "inc", "ltd", "corp", "gmbh"]

    for author in author_affiliations:
        name = author.get("name", "Unknown Author")
        affiliation = author.get("affiliation", "").lower()

        if any(keyword in affiliation for keyword in company_keywords):
            non_academic_authors.append((name, affiliation))

    return non_academic_authors


def extract_corresponding_email(text: str) -> str:
    """
    Extracts a corresponding author’s email using regex.
    """
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else "N/A"

