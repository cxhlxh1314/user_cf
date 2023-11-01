from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

@app.route('/create_user', methods=['POST'],endpoint="userinfo")
def create_user():
    user_data = request.json
    with open('user_info.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(user_data.values())

    return jsonify({'status': 'success'})

@app.route('/user_ip', methods=['POST'],endpoint="userip")
def create_user():
    user_data = request.json
    with open('user_ip.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(user_data.values())

    return jsonify({'status': 'successed'})

@app.route('/user_time', methods=['POST'],endpoint="usertime")
def create_user():
    user_data = request.json
    with open('user_time.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(user_data.values())

    return jsonify({'status': 'successed'})

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=5001,debug=True)