import pytest
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.requests.get')
def test_successful_audit_parsing(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.headers = {'Content-Type': 'text/html'}
    mock_get.return_value.text = """
        <html>
            <head>
                <title>Test Title</title>
                <meta name="description" content="Test description">
            </head>
            <body>
                <h1>Header 1</h1>
                <h1>Header 2</h1>
                <img src="img1.jpg" alt="Valid alt">
                <img src="img2.jpg"> <!-- Missing alt -->
                <p>This is a test document with some words.</p>
            </body>
        </html>
    """

    response = client.post('/api/audit', json={'url': 'https://example.com'})
    data = response.get_json()

    assert response.status_code == 200
    assert data['page_title'] == 'Test Title'
    assert data['meta_description'] == 'Test description'
    assert data['h1_count'] == 2
    assert data['images_missing_alt'] == 1
    assert data['approx_word_count'] > 0


@patch('app.requests.get')
def test_audit_timeout(mock_get, client):
    import requests

    mock_get.side_effect = requests.exceptions.Timeout

    response = client.post('/api/audit', json={'url': 'https://example.com'})
    data = response.get_json()

    assert response.status_code == 504
    assert 'error' in data
    assert 'timed out' in data['error'].lower()


@patch('app.requests.get')
def test_audit_non_html_content(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.headers = {'Content-Type': 'application/pdf'}
    
    response = client.post('/api/audit', json={'url': 'https://example.com/file.pdf'})
    data = response.get_json()

    assert response.status_code == 400
    assert 'error' in data
    assert 'did not return an html document' in data['error'].lower()