import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

def fetch_page(url):
    """ Fetch the HTML content. """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        return {'error': f"Error fetching data from crt.sh: {str(e)}"}
    
def extract_crt_id(soup):
    """ Extract certificate ID using CSS selectors. """
    return soup.select_one('td.outer a').text

def extract_summary(soup):
    """ Extract certificate summary. """
    summary = soup.select_one('th.outer:-soup-contains("Summary") + td.outer')
    return summary.text if summary else "Summary not found"

def extract_logs(soup):
    """ Extract certificate log entries. """
    logs = []
    log_rows = soup.select('div[style*="overflow-y:scroll"] table.options tr')[2:]
    for row in log_rows:
        cells = row.select('td, th')
        if len(cells) == 4:
            logs.append({
                'timestamp': cells[0].text.replace('\xa0', ' ').strip(),
                'entry': cells[1].text.strip(),
                'log_operator': cells[2].text.strip(),
                'log_url': cells[3].text.strip()
            })
    return logs

def extract_revocation_status(soup):
    """ Extract certificate revocation status. """
    status_list = []
    status_table = soup.select_one('th:-soup-contains("Revocation") + td table.options')
    if status_table:
        status_rows = status_table.select('tr')[1:]
        for row in status_rows:
            cells = row.select('td')
            if len(cells) == 6:
                status = {
                    'mechanism': cells[0].text.strip(),
                    'provider': cells[1].text.strip(),
                    'status': cells[2].text.strip(),
                    'revocation_date': cells[3].select_one('span').text.strip() if cells[3].select_one('span') else cells[3].text.strip(),
                    'last_observed_in_crl': cells[4].select_one('span').text.strip() if cells[4].select_one('span') else cells[4].text.strip(),
                    'last_checked': cells[5].select_one('span').text.strip() if cells[5].select_one('span') else cells[5].text.strip()
                }
                for key, value in status.items():
                    status[key] = value.replace('\xa0', ' ').strip()
                status_list.append(status)
    return status_list

def extract_fingerprints(soup):
    """ Extract certificate fingerprints. """
    fingerprints = {}
    fingerprint_table = soup.select_one('th:-soup-contains("Certificate Fingerprints") + td table.options')
    if fingerprint_table:
        fingerprint_rows = fingerprint_table.select('tr')
        for row in fingerprint_rows:
            cells = row.find_all(['th', 'td'])
            for i in range(0, len(cells), 3):
                if i+1 < len(cells):
                    th = cells[i].text.strip()
                    td = cells[i+1]
                    value = td.find('a').text.strip() if td.find('a') else td.text.strip()
                    if value:
                        fingerprints[th] = value
                    else:
                        fingerprints[th] = "n/a"
    return fingerprints

def certificate_extractor(id):
    route_url = f"https://crt.sh/?id={id}"
    """ Fetch certificates details from crt.sh. """
    html_content = fetch_page(route_url)
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    if len(tables) < 3:
        return {'error': "Certificate not found"}

    crt_id = extract_crt_id(soup)
    summary = extract_summary(soup)
    logs = extract_logs(soup)
    revocation_status = extract_revocation_status(soup)
    fingerprints = extract_fingerprints(soup)

    return {
        'certificate_id': crt_id,
        'summary': summary,
        'certificate_transparency': logs,
        'revocation': revocation_status,
        'certificate_fingerprints': fingerprints,
        'download_link': f'https://crt.sh/?d={crt_id}'
    }
