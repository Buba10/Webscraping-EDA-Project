# tests/test_app.py
import pytest
import subprocess
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def run_scraper():
    # Run the scraper without saving to CSV
    subprocess.run(['python', 'web_scraping_script.py', '--no-save'], check=True)

def test_get_items(client):
    run_scraper()  # Run the scraper to ensure it works
    response = client.get('/items')
    assert response.status_code == 200
    assert len(response.json) > 0  # Expecting some items from the scraping

def test_scraper_functionality():
    # Run the scraper and check if it executes without errors
    try:
        run_scraper()  # Run the scraper to ensure it works
        assert True  # If it runs without exceptions, the functionality is confirmed
    except Exception as e:
        assert False, f"Scraper failed with exception: {e}"