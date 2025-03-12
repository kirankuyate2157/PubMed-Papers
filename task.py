import argparse
import csv
import logging
import re
from typing import List, Dict, Optional
from Bio import Entrez

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set Entrez email (replace with your email)
Entrez.email = "kiranrkuyate2024@gmail.com"

# Heuristics for identifying company affiliations
NON_ACADEMIC_KEYWORDS = ["Pharma", "Biotech", "Therapeutics", "Inc", "Ltd", "Corp"]
ACADEMIC_KEYWORDS = ["University", "Hospital", "Institute", "College"]


def search_pubmed(query: str, max_results: int = 50) -> List[str]:
    """Searches PubMed and returns a list of PubMed IDs."""
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)
        return record.get("IdList", [])
    except Exception as e:
        logging.error(f"Error searching PubMed: {e}")
        return []


def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict[str, str]]:
    """Fetches paper details from PubMed using the given IDs."""
    try:
        handle = Entrez.efetch(db="pubmed", id=pubmed_ids, rettype="xml")
        records = Entrez.read(handle)
        results = []
        for article in records["PubmedArticle"]:
            title = article["MedlineCitation"]["Article"].get("ArticleTitle", "")
            pub_date = article["MedlineCitation"]["Article"].get("Journal", {}).get("JournalIssue", {}).get("PubDate", {}).get("Year", "")
            authors = article["MedlineCitation"]["Article"].get("AuthorList", [])
            
            non_academic_authors = []
            company_affiliations = []
            corresponding_email = None

            for author in authors:
                if "AffiliationInfo" in author:
                    for aff in author["AffiliationInfo"]:
                        affiliation = aff["Affiliation"]
                        if any(word in affiliation for word in NON_ACADEMIC_KEYWORDS) and not any(word in affiliation for word in ACADEMIC_KEYWORDS):
                            non_academic_authors.append(author.get("LastName", "") + " " + author.get("ForeName", ""))
                            company_affiliations.append(affiliation)
                
                # Extract corresponding author email
                if "ElectronicAddress" in author and not corresponding_email:
                    corresponding_email = author["ElectronicAddress"]

            results.append({
                "PubmedID": article["MedlineCitation"]["PMID"].strip(),
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": ", ".join(non_academic_authors),
                "Company Affiliation(s)": ", ".join(company_affiliations),
                "Corresponding Author Email": corresponding_email or "N/A"
            })
        return results
    except Exception as e:
        logging.error(f"Error fetching paper details: {e}")
        return []


def save_to_csv(filename: str, data: List[Dict[str, str]]):
    """Saves data to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    logging.info(f"Data saved to {filename}")


def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed based on a query.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename.")
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logging.info(f"Searching PubMed for: {args.query}")
    pubmed_ids = search_pubmed(args.query)
    
    if not pubmed_ids:
        logging.info("No results found.")
        return
    
    logging.info(f"Fetching details for {len(pubmed_ids)} papers...")
    papers = fetch_paper_details(pubmed_ids)
    
    if args.file:
        save_to_csv(args.file, papers)
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()
