from flask import Flask, jsonify, render_template
from utils.identity_search import identity_extractor
from utils.certificate_search import certificate_extractor
from utils.ca_search import ca_extractor

app = Flask(__name__, static_folder='utils/static', template_folder='utils/templates')

@app.route('/')
def documentation():
    return render_template('documentation.html')

@app.route('/identity/<domain>')
def get_identity(domain):
    try:
        data = identity_extractor(domain)
        if not data or 'error' in data:
            return jsonify({'error': "Host/Certificates not found"}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/certificate/<id>')
def get_certificate(id):
    try:
        data = certificate_extractor(id)
        if not data or 'error' in data:
            return jsonify({'error': "Certificate not found"}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ca/<id>')
def get_ca(id):
    try:
        data = ca_extractor(id)
        if not data or 'error' in data:
            return jsonify({'error': "CA not found"}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
