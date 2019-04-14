
import numpy as np
import operator
import math
import treePlotter

# 计算香农熵 -----------------------------------------------------------------
def calc_shannon_ent(dataSet):
    
    num_entries = len(dataSet)  # 获取数据集的文件数目
    label_counts = {}  # 建立一个便签矩阵 存放对应的标签值

    # 统计所有的标签
    for featrue_vec in dataSet:
        current_labels = featrue_vec[-1]  # 取featureVec的最后一个元素 即标签元素
        
        if current_labels not in label_counts.keys():
            label_counts[current_labels] = 0
        label_counts[current_labels] += 1

    shannon_ent = 0.0  # 熵清零

    # 根据信息熵的公式计算
    for key in label_counts:
        prob = float(label_counts[key]) / num_entries
        shannon_ent -= prob * math.log(prob, 2)

    return shannon_ent
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
def create_data_set():

    data_set = ([
        [1, 1, 'Yes'],
        [1, 1, 'Yes'],
        [1, 0, 'No'],
        [0, 1, 'No'],
        [0, 1, 'No'],
    ])

    labels = ['no surfacing', 'flippers']

    return data_set, labels


def test_shannon_ent():
    my_dat, labels = create_data_set()
    print(my_dat)

    print(calc_shannon_ent(my_dat))
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 按照给定特征对数据集进行划分 输入参数依次是数据集 划分数据集的特征和特征返回值
def split_data_set(data_set, axis, value):

    ret_data_set = []
    for featVec in data_set:
        if featVec[axis] == value:  # 若发现特征与目标值一致
            reduced_feat_vec = featVec[:axis]  # 将axis之前的列的引用添加到reducedFeatVec中
            reduced_feat_vec.extend(featVec[axis+1:])  # 将axis之后的列的引用添加到reducedFeatVec中
            ret_data_set.append(reduced_feat_vec)  # 将去除了指定特征列的数据集放在retDataSet中

    return ret_data_set


def test_split():
    my_dat, labels = create_data_set()
    print(my_dat)

    print(split_data_set(my_dat, 0, 1))
    print(split_data_set(my_dat, 0, 0))
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 选择最好的分割点
def choose_best_feature_to_split(data_set):

    feature_count = len(data_set[0]) - 1  # 对数据集第一行的长度 即特征个数
    data_count = float(len(data_set))  # 数据集的样例个数

    base_shannon_ent = calc_shannon_ent(data_set)  # 算出初始的香农熵
    best_gain = 0.0  # 初始化最高信息增益
    best_feature = -1  # 初始化最佳分割点

    for i in range(feature_count):  # 计算每个特征的信息熵
        feat_list = [example[i] for example in data_set]  # 遍历所有数据的第i个特征
        unique_vals = set(feat_list)  # 去除第i个特征的重复值

        new_ent = 0.0  # 初始化当前信息熵
        for value in unique_vals:  # 遍历第i个特征的所有取值
            sub_data_set = split_data_set(data_set, i, value)  # 不同特征值处分割
            prob = len(sub_data_set) / data_count
            new_ent += prob * calc_shannon_ent(sub_data_set)  # 计算此时的信息熵

        info_gain = base_shannon_ent - new_ent  # 计算信息增益
        if info_gain > best_gain:
            best_gain = info_gain
            best_feature = i  # 记录下最佳分割的特征

    return best_feature
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 多数表决分类函数
def majority_cnt(class_list):
    class_count = {}  # 建立数据字典 存储所有的类别
    for vote in class_list:
        if vote not in class_count.keys():
            class_count[vote] = 0  # 如果有新类别 则创立一个新的元素代表该类
        class_count[vote] += 1

    # 对数据集进行排序 数据的第二个元素(1)作为排序依据
    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]  # 返回出现次数最多的元素


# 构建决策树
def create_tree(data_set, labels):
    # 以训练集的最后一列作为一个新的列表
    class_list = [example[-1] for example in data_set]

    # 如果原本全属于同一类别
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]  # 直接返回该类别

    # 如果候选特征只剩一个
    if len(data_set[0]) == 1:
        return majority_cnt(class_list)  # 返回该特征出现次数最多的类别

    # 从候选的特征中选择一个最佳的特征
    best_feat = choose_best_feature_to_split(data_set)
    best_feat_label = labels[best_feat]  # 记录最优特征的标签

    my_tree = {best_feat_label: {}}  # 根据最优标签生成树
    del(labels[best_feat])  # 去除已经使用过的标签

    # 获取训练集中最优特征属性值
    feat_values = [example[best_feat] for example in data_set]
    unique_vals = set(feat_values)  # 去除重复的值

    for value in unique_vals:  # 遍历所选特征的所有候选值
        sub_labels = labels[:]  # 把label完全复制一遍
        my_tree[best_feat_label][value] = create_tree(split_data_set(data_set, best_feat, value), sub_labels)

    return my_tree


def test_tree_creation():
    my_dat, labels = create_data_set()
    my_tree = create_tree(my_dat, labels)
    print(my_tree)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 利用决策树进行分类
def classify(input_tree, feat_labels, test_vec):

    first_str = list(input_tree)[0]
    second_dict = input_tree[first_str]
    feat_index = feat_labels.index(first_str)

    key = test_vec[feat_index]
    value_of_feat = second_dict[key]

    if isinstance(value_of_feat, dict):
        class_label = classify(value_of_feat, feat_labels, test_vec)
    else:
        class_label = value_of_feat

    return class_label


def test_classify():
    _my_dat, labels = create_data_set()
    print(labels)

    my_tree = treePlotter.retrieve_tree(0)
    print(my_tree)

    print(classify(my_tree, labels, [1, 0]))
    print(classify(my_tree, labels, [1, 1]))
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 把决策树存储到本地文件
def store_tree(input_tree, filename):
    import pickle

    fw = open(filename, 'wb')
    pickle.dump(input_tree, fw)
    fw.close()


# 从本地文件中回复决策树
def grab_tree(filename):
    import pickle
    fr = open(filename, 'rb')
    return pickle.load(fr)


def test_tree_store():
    my_tree = treePlotter.retrieve_tree(0)
    store_tree(my_tree, 'classifierStorage.bin')
    print(grab_tree('classifierStorage.bin'))
# ---------------------------------------------------------------------------


test_tree_store()