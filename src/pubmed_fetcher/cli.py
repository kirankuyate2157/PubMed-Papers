import argparse
from pubmed_fetcher.fetcher import fetch_pubmed_papers
from pubmed_fetcher.parser import extract_company_authors, extract_corresponding_email
from pubmed_fetcher.utils import save_to_csv, print_results


def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV file name.")

    args = parser.parse_args()
    papers = fetch_pubmed_papers(args.query)

    processed_data = []
    for paper in papers:
        title = paper.get("title", "N/A")
        pub_date = paper.get("pubdate", "N/A")
        authors = paper.get("authors", [])
        affiliations = paper.get("affiliations", "")

        non_academic_authors = extract_company_authors(authors)
        email = extract_corresponding_email(affiliations)

        processed_data.append({
            "PubmedID": paper.get("uid"),
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": ", ".join(a[0] for a in non_academic_authors),
            "Company Affiliation(s)": ", ".join(a[1] for a in non_academic_authors),
            "Corresponding Author Email": email,
        })
    print("✨🔥🔥📌 1: Final Processed Data:", processed_data) 
    if args.file:
        save_to_csv(processed_data, args.file)
    else:
        print_results(processed_data)


if __name__ == "__main__":
    main()
