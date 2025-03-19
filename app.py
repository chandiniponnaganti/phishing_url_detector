from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)  # Make sure this line exists!

VIRUSTOTAL_API_KEY = "a4ecc720b840f23ef9df0c7848208af12fd20128ab2a89d007523bbe37025382"
VIRUSTOTAL_URL = "https://www.virustotal.com/api/v3/urls"

def scan_url(url):
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    data = {"url": url}
    response = requests.post(VIRUSTOTAL_URL, headers=headers, data=data)

    if response.status_code == 200:
        result = response.json()
        scan_id = result["data"]["id"]
        return get_scan_results(scan_id)
    else:
        return {"error": "Error scanning the URL"}

def get_scan_results(scan_id):
    url = f"https://www.virustotal.com/api/v3/analyses/{scan_id}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        return result["data"]["attributes"]["stats"]
    else:
        return {"error": "Error retrieving scan results"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    url = request.form.get("url")
    result = scan_url(url)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
