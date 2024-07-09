from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

def check_auth(username, password):
    return username == 'admin' and password == 'garden'

def authenticate():
    return jsonify({"message": "Authentication required"}), 401

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/update', methods=['POST'])
@requires_auth
def update_repo():
    try:
        result = subprocess.run(['/home/pi/ota_update/update_from_github.sh'], capture_output=True, text=True)
        return result.stdout, 200
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
