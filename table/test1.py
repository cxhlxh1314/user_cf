from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

@app.route('/create_user', methods=['POST'])
def create_user():
    user_data = request.json
    with open('user_profile.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(user_data.values())

    return jsonify({'status': 'success'})

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=5001,debug=True)