import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

def identity_extractor(domain):
    """ Fetch SSL/TLS certificates information for a given domain from crt.sh. """
    url = f'https://crt.sh/?q={domain}'

    try:
        response = requests.get(url)
        response.raise_for_status()
    except RequestException as e:
        return {'error': f"Error fetching data from crt.sh: {str(e)}"}

    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')
    if len(tables) < 3:
        return {'error': "Host/Certificates not found"}

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
            'crtsh_id': cols[0].text.strip(),
            'logged_at': cols[1].text.strip(),
            'not_before': cols[2].text.strip(),
            'not_after': cols[3].text.strip(),
            'common_name': cols[4].text.strip(),
            'matching_identities': cols[5].text.strip(),
            'issuer_name': cols[6].text.strip(),
            'certificate': f'https://crt.sh/?id={cols[0].text.strip()}',
            'issuer': f'https://crt.sh/{issuer_link}',
        }
        certificates.append(cert_data)

    return {'certificates': certificates}
