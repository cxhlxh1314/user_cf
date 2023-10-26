import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import warnings
import heapq
from scipy.sparse import csr_matrix

# 稀疏矩阵来存储相似度矩阵，使用了DBSCAN算法来进行聚类，避免了重复计算，使用了更高效的数据结构来处理用户画像数据。


# 禁用scikit-learn库的FutureWarning警告
warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")

# 读取用户画像数据
user_profile = pd.read_csv('user_profile.csv')
# 设定每位用户推荐的人数
num_recommendations = 2
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
age_diff = np.abs(user_profile['age'].values.reshape(-1, 1) - user_profile['age'].values)
gender_diff = (user_profile['gender'].values.reshape(-1, 1) == user_profile['gender'].values).astype(int)
interests_diff = np.zeros((len(user_profile), len(user_profile)))
for i in range(len(user_profile)):
    for j in range(i+1, len(user_profile)):
        interests_i = set(str(user_profile.iloc[i]['interests']).split(','))
        interests_j = set(str(user_profile.iloc[j]['interests']).split(','))
        common_interests = interests_i & interests_j
        interests_diff[i][j] = len(common_interests) / len(interests_i | interests_j)
        interests_diff[j][i] = interests_diff[i][j]
constellation_diff = np.abs(user_profile['constellation'].values.reshape(-1, 1) - user_profile['constellation'].values) / 12
similarity_matrix = tag_weights['age'] * age_diff + tag_weights['gender'] * gender_diff + tag_weights['interests'] * interests_diff + tag_weights['constellation'] * constellation_diff
np.fill_diagonal(similarity_matrix, 1)
similarity_matrix_sparse = csr_matrix(similarity_matrix)

# 对相似度矩阵进行模糊聚类
dbscan = DBSCAN(eps=0.5, min_samples=5, metric='precomputed')
dbscan.fit(similarity_matrix_sparse)

# 对每个用户进行推荐
for i in range(len(user_profile)):
    recommendations = [] # 初始化recommendations列表
    for j in range(len(user_profile)):
        if i != j and dbscan.labels_[i] == dbscan.labels_[j]:
            weighted_similarity = similarity_matrix[i][j] * user_profile.iloc[j]['weight'] * (1 - abs(user_profile.iloc[i]['constellation'] - user_profile.iloc[j]['constellation']) / 12)
            recommendations.append((user_profile.iloc[j]['name'], weighted_similarity)) # 将相似的用户添加到recommendations列表中
    recommendations = [rec for rec in recommendations if rec[0] not in user_profile.iloc[i]['name']]
    recommendations = heapq.nlargest(num_recommendations, recommendations, key=lambda x: x[1])
    print(f"-----------------为用户{user_profile.iloc[i]['name']}推荐可能认识的人：")
    for rec in recommendations:
        print(f"用户{rec[0]}，相似度得分：{rec[1]}")