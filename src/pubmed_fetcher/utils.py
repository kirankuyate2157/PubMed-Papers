import csv
import pandas as pd


def save_to_csv(data: list[dict], filename: str) -> None:
    """Saves the extracted paper data to a CSV file."""
    if not data:
        print("No data to save.")
        return

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


def print_results(data: list[dict]) -> None:
    """Prints the results to the console."""
    for paper in data:
        print(f"Title: {paper.get('title', 'N/A')}")
        print(f"Publication Date: {paper.get('pub_date', 'N/A')}")
        print(f"Authors: {', '.join(paper.get('authors', []))}")
        print(f"Corresponding Email: {paper.get('email', 'N/A')}")
        print("-" * 50)
