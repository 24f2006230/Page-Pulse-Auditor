from flask import Flask,request,jsonify,render_template
from bs4 import BeautifulSoup
import time
import requests
from urllib.parse import urlparse

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/audit', methods=['POST'])
def audit():
    data=request.get_json()
    if not data or 'url' not in data or not data['url'].strip():
        return jsonify({"error": "Please provide a valid URL."}), 400
    
    target_url=data['url']

    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url


    parsed_url = urlparse(target_url)
    if not parsed_url.netloc:
        return jsonify({"error": "Invalid URL format."}), 400

    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        start_time = time.time()
        response = requests.get(target_url, headers=headers, timeout=5, allow_redirects=True)
        response_time_ms = round((time.time() - start_time) * 1000, 2)

    except requests.exceptions.Timeout:
        return jsonify({"error": "The request timed out. The server took too long to respond."}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Failed to connect to the URL. Please check domain or network."}), 502
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"An error occurred while fetching the URL: {str(e)}"}), 400

    
    content_type = response.headers.get('Content-Type', '')
    if 'text/html' not in content_type.lower():
        return jsonify({
            "error": f"URL did not return an HTML document. Received content-type: '{content_type}'"
        }), 400

    try:
        soup = BeautifulSoup(response.text, 'html.parser')

        
        page_title = soup.title.string.strip() if soup.title and soup.title.string else "No Title Found"

        meta_desc_tag = soup.find('meta', attrs={'name': lambda x: x and x.lower() == 'description'})
        meta_description = meta_desc_tag['content'].strip() if meta_desc_tag and meta_desc_tag.has_attr('content') else "No Meta Description Found"

        h1_count = len(soup.find_all('h1'))

        images = soup.find_all('img')
        images_missing_alt = sum(1 for img in images if not img.get('alt') or not img.get('alt').strip())

        for element in soup(["script", "style", "head", "title", "meta"]):
            element.extract()
        text = soup.get_text()
        words = [word for word in text.split() if word.isalnum()]
        approx_word_count = len(words)


        report = {
            "target_url": target_url,
            "http_status": response.status_code,
            "response_time_ms": response_time_ms,
            "page_title": page_title,
            "meta_description": meta_description,
            "h1_count": h1_count,
            "images_missing_alt": images_missing_alt,
            "approx_word_count": approx_word_count
        }

        return jsonify(report), 200

    except Exception as e:
        return jsonify({"error": f"Failed to parse page content: {str(e)}"}), 500

if __name__ == '__main__':
    app.run()