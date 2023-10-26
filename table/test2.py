import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import warnings

# 禁用scikit-learn库的FutureWarning警告
warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")

# 读取用户画像数据
user_profile = pd.read_csv('user_profile.csv')

# 添加星座标签权重
tag_weights = {'age': 0.2, 'gender': 0.3, 'interests': 0.5, 'constellation': 0.1}

# 对不同标签进行归一化处理
for tag in tag_weights.keys():
    if tag == 'constellation':
        user_profile[tag] = user_profile[tag].apply(lambda x: ord(x[0]) - 64)
    else:
        user_profile[tag] = pd.to_numeric(user_profile[tag], errors='coerce')
        user_profile[tag] = (user_profile[tag] - user_profile[tag].min()) / (user_profile[tag].max() - user_profile[tag].min())

# 计算用户之间的相似度矩阵
similarity_matrix = np.zeros((len(user_profile), len(user_profile)))
for i in range(len(user_profile)):
    for j in range(len(user_profile)):
        if i == j:
            similarity_matrix[i][j] = 1
        else:
            similarity_matrix[i][j] = tag_weights['age'] * abs(
                user_profile.iloc[i]['age'] - user_profile.iloc[j]['age']) + tag_weights['gender'] * (1 if user_profile.iloc[i]['gender'] == user_profile.iloc[j]['gender'] else 0) + tag_weights['interests'] * len(set(str(user_profile.iloc[i]['interests']).split(',')) & set(
                str(user_profile.iloc[j]['interests']).split(','))) / len(
                set(str(user_profile.iloc[i]['interests']).split(',')) | set(
                    str(user_profile.iloc[j]['interests']).split(','))) + tag_weights['constellation'] * abs(
                user_profile.iloc[i]['constellation'] - user_profile.iloc[j]['constellation']) / 12 if i != j else 0

# 对相似度矩阵进行模糊聚类
kmeans = KMeans(n_clusters=6)
fuzzy_matrix = kmeans.fit_transform(similarity_matrix)

# 对每个用户进行推荐
for i in range(len(user_profile)):
    recommendations = [] # 初始化recommendations列表
    for j in range(len(user_profile)):
        if i != j:
            weighted_similarity = fuzzy_matrix[i][kmeans.labels_[j]] * user_profile.iloc[j]['weight'] * (1 - abs(user_profile.iloc[i]['constellation'] - user_profile.iloc[j]['constellation']) / 12)
            recommendations.append((user_profile.iloc[j]['name'], weighted_similarity)) # 将相似的用户添加到recommendations列表中
    recommendations = [rec for rec in recommendations if rec[0] not in user_profile.iloc[i]['name']]
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
    print(f"为用户{user_profile.iloc[i]['name']}推荐可能认识的人：")
    for rec in recommendations:
        print(f"用户{rec[0]}，相似度得分：{rec[1]}")