from pubmed_fetcher.cli import main

if __name__ == "__main__":
    main()
# cmd 
# poetry run pytest --cov=pubmed_fetcher --cov-report=term-missing
# python -m src.pubmed_fetcher.cli "cancer research" -f output.csv