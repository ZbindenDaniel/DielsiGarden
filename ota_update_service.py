from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/update', methods=['POST'])
def update_repo():
    try:
        # Call the update script
        result = subprocess.run(['/home/pi/ota_update/update_from_github.sh'], capture_output=True, text=True)
        return result.stdout, 200
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
