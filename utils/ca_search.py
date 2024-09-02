
import re
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

def extract_ca_id(soup):
    """ Extract the CA ID. """
    return soup.find("th", text="crt.sh CA ID").find_next_sibling("td").text.strip()

def extract_ca_name_and_country(soup):
    """ Extract the CA name and country. """
    ca_info = soup.find("th", string="CA Name/Key").find_next_sibling("td").get_text(separator=" ", strip=True)
    details = {}
    common_name_match = re.search(r"commonName\s*=\s*([^,]+?)(?=\s*\b|$)", ca_info)
    if common_name_match:
        details["ca_name"] = common_name_match.group(1).strip()
    organization_name_match = re.search(r"organizationName\s*=\s*(.*?)(?=\s*[a-zA-Z]+Name\s*=|$)", ca_info)
    if organization_name_match:
        details["organization_name"] = organization_name_match.group(1).replace('\u00a0',' ').strip()
    country_name_match = re.search(r"countryName\s*=\s*([^,]+?)(?=\s*\b|$)", ca_info)
    if country_name_match:
        details["country"] = country_name_match.group(1).strip()
    return details

def extract_certificates(soup):
    """ Extract the certificates. """
    certificates = []
    certificates_table = soup.find("th", string="Certificates").find_next_sibling("td").find("table")
    for row in certificates_table.find_all("tr")[1:]:
        cells = row.find_all("td")
        cert = {
            "crtsh_id": cells[0].text.strip(),
            "not_before": cells[1].text.strip(),
            "not_after": cells[2].text.strip(),
            "issuer_name": cells[3].get_text(strip=True)
        }
        certificates.append(cert)
    return certificates

def extract_parent_cas(soup):
    """ Extract the parent CAs. """
    parent_cas = {}
    parent_cas_table = soup.find("th", string="Parent CAs").find_next_sibling("td").find("table")
    for row in parent_cas_table.find_all("tr"):
        link = row.find("a")
        if link:
            ca_full_name = link.text.strip()
            ca_href = link['href']
            parent_cas[ca_full_name] = ca_href
    return parent_cas


def extract_child_cas(soup):
    """ Extract the child CAs. """
    child_cas = {}
    child_cas_section = soup.find("th", string="Child CAs").find_next_sibling("td")
    if child_cas_section:
        links = child_cas_section.find_all("a")
        if links:
            for link in links:
                child_ca_name = link.text.strip()
                child_ca_href = link['href']
                child_cas[child_ca_name] = child_ca_href
        else:
            return child_cas_section.text.strip()
    return child_cas


def ca_extractor(id):
    route_url = f"https://crt.sh/?caid={id}"
    """ Fetch ca details from crt.sh. """
    html_content = fetch_page(route_url)
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    if len(tables) < 3:
        return {'error': "CA not found"}
    ca_id = extract_ca_id(soup)
    ca_details = extract_ca_name_and_country(soup)
    certificates = extract_certificates(soup)
    parent_cas = extract_parent_cas(soup)
    child_cas = extract_child_cas(soup)

    return {
        "ca_id": ca_id,
        **ca_details,
        "certificates": certificates,
        "parent_cas": parent_cas,
        "child_cas": child_cas
    }
