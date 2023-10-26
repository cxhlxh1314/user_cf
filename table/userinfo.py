import logging
import orjson
from flask import Flask, request
import csv



app = Flask(__name__)

# @app.post("{}/update_data")
# def get_score(uuid:str,module_id:int):
#     cv_backend = user_store_backend.get_store(uuid)
#     data= cv_backend.chat_score(module_id)
#
#     return Response(
#         orjson.dumps(data),
#         status_code=200)


@app.post('{}/update_user_data')
def update_user_data():
    my_dict = request.get_data()
    # my_dict = {
    #     "userid": "123456789999",
    #     "user_name": "lxh44",
    #     "age": "22",
    #     "gender": "111",
    #     "birthday": "2002-2-5",
    #     "vocation": "student",
    #     "relation": "master",
    #
    # }
    my_list = list(my_dict)

    with open('passwd.txt', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        # print(rows)

    # 遍历列表，更新或添加数据
    found = False

    for row in rows:
        if str(row[0]) == my_dict['userid']:
            # print(type(str(row[0])))
            if any(row[key] != my_dict[key] for key in my_dict if key != 'userid'):
                row.update(my_dict)
                print('update:', my_dict)
            else:
                print('no update needed')
            found = True
            break

    if not found:
        rows.append(my_dict)
        print('new:', my_dict)

    # 打开CSV文件并使用csv.DictWriter类将更新后的列表写回CSV文件
    with open('passwd.txt', 'w', newline='') as file:
        fieldnames = my_list
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return my_dict

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)