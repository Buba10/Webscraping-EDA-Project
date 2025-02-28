import sys
import os
import pytest
import subprocess

# Adjust the path to include the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    """
    Fixture that provides a test client for the Flask application.
    This client can be used in tests to simulate requests to the app. 
    The client is created at the beginning of the test and properly 
    cleaned up afterwards. Any necessary setup or teardown actions 
    can be added if needed.
    """
    with app.test_client() as client:
        yield client

def run_scraper():
    # Run the scraper without saving to CSV
    subprocess.run(['python', 'scraper.py', '--no-save'], check=True)

def test_get_items(client):
    # Tests the /items endpoint after running the scraper.
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
        pytest.fail(f"Scraper failed with exception: {e}")