# Page Pulse Auditor

A lightweight web tool that audits any URL and returns key SEO and accessibility metrics. 

## Setup Instructions
1. Clone the repository: `git clone https://github.com/24f2006230/Page-Pulse-Auditor`
2. Navigate to the directory: `cd Page-Pulse-Auditor`
3. Create a virtual environment: `python -m venv venv`
4. Activate the environment (Windows: `venv\Scripts\activate`, Mac/Linux: `source venv/bin/activate`)
5. Install dependencies: `pip install -r requirements.txt`
6. Run the application: `python app.py`
7. Access the tool at `http://127.0.0.1:5000`

## Running Tests
This project uses `pytest` to ensure the reliability of the backend parsing logic and error handling. 

**To run the test suite:**
1. Ensure your virtual environment is activated.
2. Install the testing requirements:
   ```bash
   pip install pytest pytest-mock
   ```
3. Execute the tests from the root directory:
   ```bash
   pytest test_app.py
   ```
4. The terminal will output the test results, validating the happy path (successful HTML parsing) and failure edge cases (timeouts and non-HTML content).

## API Contract
**Endpoint:** `POST /api/audit`

**Request Body (JSON):**
```json
{
  "url": "[https://example.com](https://example.com)"
}
```

**Success Response (200 OK):**
```json
{
  "approx_word_count": 345,
  "h1_count": 1,
  "http_status": 200,
  "images_missing_alt": 2,
  "meta_description": "Example description",
  "page_title": "Example Domain",
  "response_time_ms": 124.5,
  "target_url": "[https://example.com](https://example.com)"
}
```

**Error Response (e.g., 400, 502, 504):**
```json
{
  "error": "Descriptive error message here."
}
```

## Design Decisions

1. **Flask Backend & Vanilla JS Frontend:** I chose Flask because it is incredibly lightweight and perfect for a single-endpoint microservice. Paired with Vanilla JS and the Fetch API, it removes the need for heavier frontend frameworks, keeping the application fast and easy to deploy.
2. **BeautifulSoup over Headless Browsers:** I opted to use `requests` and `BeautifulSoup4` for parsing rather than a headless browser (like Selenium or Puppeteer). While headless browsers render JavaScript, they are resource-heavy and slow. BeautifulSoup is significantly faster and more defensible for a rapid auditing tool focused on initial HTML payloads.
3. **Graceful Degradation via Extensive Try-Except Blocks:** A key design focus was ensuring the API never crashes. By wrapping the network requests and parsing logic in targeted exception handlers, the application anticipates timeouts, invalid schemas, and non-HTML payloads, always returning a sensible JSON error and a valid HTTP status code rather than a server fault.

## Loom Video
```https://www.loom.com/share/955e64677d28433ba09b439dfb98e4a4```

