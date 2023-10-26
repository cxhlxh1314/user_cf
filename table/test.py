import csv
def update_user_data():
    my_dict = {
        "userid": "111",
        "user_name": "lxh",
        "age": "22",
        "gender": "1",
        "birthday": "2002-2-5",
        "vocation": "student",
        "relation": "master",

    }
    my_list = list(my_dict)
    # print(my_list)

    # 打开CSV文件并读取所有行
    with open('passwd.txt', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # 遍历列表，更新或添加数据
    found = False

    for row in rows:
        if row['userid'] == my_dict['userid']:
            if any(row[key] != my_dict[key] for key in my_dict if key != 'userid'):
                row.update(my_dict)
                print('update:',my_dict)
            else:
                print('no update needed')
            found = True
            break

    if not found:
        rows.append(my_dict)
        print('new:',my_dict)

    # 打开CSV文件并使用csv.DictWriter类将更新后的列表写回CSV文件
    with open('passwd.txt', 'w', newline='') as file:
        fieldnames = my_list
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
if __name__== "__main__":
    update_user_data()