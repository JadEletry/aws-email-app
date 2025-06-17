from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')
table = dynamodb.Table('Emails')

@app.route("/", methods=["GET"])
def home():
    return "<h2>Flask is running. Use POST /subscribe to add a subscriber.</h2>"


@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        data = request.get_json()
        email = data.get('email')
        if not email:
            return jsonify({'message': 'Email is required!'}), 400

        response = table.put_item(Item={'email': email})
        return jsonify({'message': 'Subscription successful!'})
    except Exception as e:
        return jsonify({'message': 'An error occurred.', 'error': str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
