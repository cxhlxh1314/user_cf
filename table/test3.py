import pandas as pd
import numpy as np

# 读取用户画像数据
user_profile = pd.read_csv('user_profile.csv')


# 定义标签权重
tag_weights = {'age': 0.2, 'gender': 0.3, 'interests': 0.5}
# 根据年龄分组
age_groups = user_profile.groupby(pd.cut(user_profile['age'], bins=[0, 18, 30, 45, 60, 100], labels=['<18', '18-30', '30-45', '45-60', '>60']))

# 对不同标签进行归一化处理
for tag in tag_weights.keys():
    user_profile[tag] = pd.to_numeric(user_profile[tag], errors='coerce')
    user_profile[tag] = (user_profile[tag] - user_profile[tag].min()) / (user_profile[tag].max() - user_profile[tag].min())




# 对每个年龄段内的用户进行推荐
for age_group, group_data in age_groups:
    # 确保所有用户都被添加到group_data中
    group_data = group_data.reset_index(drop=True)
    # 计算用户之间的相似度矩阵
    similarity_matrix = np.zeros((len(group_data), len(group_data)))
    for i in range(len(group_data)):
        for j in range(len(group_data)):
            if i == j:
                similarity_matrix[i][j] = 1
            else:
                similarity_matrix[i][j] = tag_weights['age'] * abs(
                    group_data.iloc[i]['age'] - group_data.iloc[j]['age']) +tag_weights['gender'] * (1 if group_data.iloc[i]['gender'] == group_data.iloc[j]['gender'] else 0) +tag_weights['interests'] * len(set(str(group_data.iloc[i]['interests']).split(',')) & set(
                    str(group_data.iloc[j]['interests']).split(','))) / len(
                    set(str(group_data.iloc[i]['interests']).split(',')) | set(
                        str(group_data.iloc[j]['interests']).split(','))) if i != j else 0

    # 对加权后的相似度矩阵进行求和，得到推荐结果
    for i in range(len(group_data)):
        recommendations = [group_data.iloc[i]['name']] # 初始化recommendations列表
        for j in range(len(group_data)):
            if i != j and group_data.iloc[j]['name'] not in recommendations:
                weighted_similarity = similarity_matrix[i][j] * group_data.iloc[j]['weight']
                for k in range(len(group_data)):
                    if k != i and k != j:
                        weighted_similarity += similarity_matrix[j][k] * group_data.iloc[k]['weight']
                similarity_matrix[i][j] = weighted_similarity
                recommendations.append(group_data.iloc[j]['name']) # 将相似的用户添加到recommendations列表中
        recommendations = [rec for rec in recommendations if rec in group_data['name'].values]
        print(group_data.iloc[i]['name'])
        if len(recommendations) > 1: # 判断recommendations列表是否为空
            recommendations = sorted(recommendations, key=lambda x: similarity_matrix[i][group_data[group_data['name'] == x].index[0]], reverse=True)
            print(f"---------为{age_group}岁的用户{group_data.iloc[i]['name']}推荐可能认识的人：")
            for rec in recommendations:
                if rec != group_data.iloc[i]['name']:
                    # print("ok")
                    print(f"用户{rec}，相似度得分：{similarity_matrix[i][group_data[group_data['name'] == rec].index[0]]}")
