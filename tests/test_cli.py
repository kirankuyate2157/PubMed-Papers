import unittest
from unittest.mock import patch
import sys
from io import StringIO
from pubmed_fetcher.cli import main

class TestCLI(unittest.TestCase):
    
    @patch("pubmed_fetcher.cli.fetch_pubmed_papers")
    @patch("pubmed_fetcher.cli.extract_company_authors")
    @patch("pubmed_fetcher.cli.extract_corresponding_email")
    @patch("pubmed_fetcher.cli.save_to_csv")
    @patch("pubmed_fetcher.cli.print_results")
    def test_main_with_output_file(self, mock_print_results, mock_save_to_csv, mock_extract_email, mock_extract_authors, mock_fetch_papers):
        mock_fetch_papers.return_value = [{
            "uid": "12345",
            "title": "Sample Research Paper",
            "pubdate": "2024-01-01",
            "authors": ["John Doe"],
            "affiliations": "Sample Company"
        }]
        mock_extract_authors.return_value = [("John Doe", "Sample Company")]
        mock_extract_email.return_value = "john.doe@example.com"

        test_args = ["cli.py", "cancer research", "-f", "output.csv"]
        with patch.object(sys, 'argv', test_args):
            main()
        
        mock_fetch_papers.assert_called_once_with("cancer research")
        mock_extract_authors.assert_called()
        mock_extract_email.assert_called()
        mock_save_to_csv.assert_called_once()
        mock_print_results.assert_not_called()
    
    @patch("pubmed_fetcher.cli.fetch_pubmed_papers")
    @patch("pubmed_fetcher.cli.extract_company_authors")
    @patch("pubmed_fetcher.cli.extract_corresponding_email")
    def test_main_without_output_file(self, mock_extract_email, mock_extract_authors, mock_fetch_papers):
        mock_fetch_papers.return_value = [{
            "uid": "12345",
            "title": "Sample Research Paper",
            "pubdate": "2024-01-01",
            "authors": ["John Doe"],
            "affiliations": "Sample Company"
        }]
        mock_extract_authors.return_value = [("John Doe", "Sample Company")]
        mock_extract_email.return_value = "john.doe@example.com"

        test_args = ["cli.py", "cancer research"]
        with patch.object(sys, 'argv', test_args), patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
        
        mock_fetch_papers.assert_called_once_with("cancer research")
        mock_extract_authors.assert_called()
        mock_extract_email.assert_called()

        # Ensure expected output appears in stdout
        self.assertIn("Sample Research Paper", output)
        self.assertIn("John Doe", output)
        self.assertIn("Sample Company", output)
        self.assertIn("john.doe@example.com", output)
        self.assertIn("Title: Sample Research Paper", output)
        self.assertIn("Publication Date: 2024-01-01", output)
        self.assertIn("Authors: John Doe", output)
        self.assertIn("Corresponding Email: john.doe@example.com", output)


if __name__ == "__main__":
    unittest.main()
