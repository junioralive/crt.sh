# 🌐 crt.sh REST API

crt.sh REST API is a unofficial, free and open-source service that retrieves SSL certificate details from crt.sh for specified domains. Designed with simplicity and ease of integration in mind, this API supports seamless integration into various services or applications that programmatically require SSL certificate data. It's a no-CORS, no-authentication-required API, making it publicly accessible and easily self-hostable for anyone needing direct and unrestricted access to SSL certificate information.

## 🌟 Features

- 📜 Fetch SSL certificate details by domain.
- 🚀 More features coming soon...

## 🛠 Setup

### Prerequisites

- Python 3.x 🐍
- Flask 🍶
- BeautifulSoup4 📦
- Requests 📬

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/junioralive/crt.sh
   cd crt.sh
   ```

2. Install the necessary packages:
   ```bash
   pip install flask beautifulsoup4 requests
   ```

3. Run the application:
   ```bash
   python app.py
   ```

### 🔍 Usage

Visit `http://localhost:5000/` to view the documentation and learn how to use the API. Use the endpoint `/site/{domain}` to fetch SSL certificate details, replacing `{domain}` with the actual domain name you wish to query.

## 📝 To-Do List

- [ ] Add Certificate Search 🔍
- [ ] Add CA Search 🔎

## **📞 Contact:**

[![Discord Server](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/cwDTVKyKJz)
[![GitHub Project](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/junioralive)
[![Email](https://img.shields.io/badge/Email-D44638?style=for-the-badge&logo=gmail&logoColor=white)](mailto:support@junioralive.in)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.