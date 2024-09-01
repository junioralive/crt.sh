from flask import Flask, jsonify, request, render_template, Response
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

app = Flask(__name__)

def fetch_certificates(domain):
    url = f'https://crt.sh/?q={domain}'

    try:
        response = requests.get(url)
        response.raise_for_status()
    except RequestException as e:
        return {'error': f"Error fetching data from crt.sh: {e}"}

    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')
    if len(tables) < 3:
        return {'error': "Unable to find the expected certificate table."}

    cert_table = tables[2]
    rows = cert_table.find_all('tr')[1:]

    certificates = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 7:
            continue

        issuer_anchor = cols[6].find('a')
        issuer_link = issuer_anchor['href'].strip() if issuer_anchor else ''
        
        cert_data = {
            'crt.sh ID': cols[0].text.strip(),
            'Logged At': cols[1].text.strip(),
            'Not Before': cols[2].text.strip(),
            'Not After': cols[3].text.strip(),
            'Common Name': cols[4].text.strip(),
            'Matching Identities': cols[5].text.strip(),
            'Issuer Name': cols[6].text.strip(),
            'Certificate Link': f'https://crt.sh/?id={cols[0].text.strip()}',
            'Issuer Link': f'https://crt.sh/{issuer_link}',
        }
        certificates.append(cert_data)
    
    return certificates

@app.route('/css/<path:filename>')
def serve_css(filename):
    with open(f'templates/{filename}', 'r') as f:
        css = f.read()
    return Response(css, mimetype='text/css')

@app.route('/')
def documentation():
    return render_template('documentation.html')

@app.route('/site/<domain>')
def get_certificates(domain):
    certificates = fetch_certificates(domain)
    if not certificates or 'error' in certificates:
        return jsonify({'error': 'No certificates found or an error occurred.'}), 404
    return jsonify(certificates)

if __name__ == '__main__':
    app.run(debug=True)