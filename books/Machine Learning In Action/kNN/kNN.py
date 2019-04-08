
import numpy as np
import operator

# ----------------------------------------------------------------
# 简单的knn分类器
def classify0(inX, dataSet, labels, k):

    # 1.计算已知类别数据集与当前点的距离
    # dataSetSize为读取数据集的行数
    dataSetSize = dataSet.shape[0] # shape[0]读取矩阵行数 shape[1]读取矩阵列数
    # 复制比较向量inX 复制成一个 dataSetSize 行 1 列的矩阵 然后与数据集矩阵相减 结果存到diffMat中
    diffMat = np.tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2 # 把矩阵各元素依次平方 结果存到sqDiffMat中
    sqDistances = sqDiffMat.sum(axis=1) # 把每行元素相加 得到一个列向量sqDistances
    distances = sqDistances ** 0.5 # 对列向量sqDistances每个元素开根号 结果为列向量distances

    sortedDistanceIndices = distances.argsort() # 使用argsort排序 返回从小到大的顺序值 如{2, 4, 1}返回{1, 2, 0}
    classCount = {} # classCount字典 用于计数

    # 2.选择与当前点距离最小的k各点
    for i in range(k):
        # 按照之前排序值依次对标签进行计数
        voteIlabel = labels[sortedDistanceIndices[i]]
        # 统计票数到字典中
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1 # 初始lable的票数为0
    
    # 3.返回一个列表按照字典的value值(key为0 value为1)降序排列
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)

    # sortedClassCount[0]为label数最大的字典元素 sortedClassCount[0][0]返回label(key)的值
    return sortedClassCount[0][0]
# ----------------------------------------------------------------


# ----------------------------------------------------------------
# 对每个特征进行归一化处理
# 归一化处理即 newValue = (oldValue - min) / (max - min)
def autoNorm(dataSet):
    print(type(dataSet))
    # dataSet的维数为 nx3 n为样例个数
    minVals = dataSet.min(0) # 从列中选取数据集的最小值
    maxVals = dataSet.max(0) # 从列中选取数据集的最大值
    ranges = maxVals - minVals

    normDataSet = np.zeros(np.shape(dataSet)) # 建立一个零矩阵 其维数和dataSet相同
    m = dataSet.shape[0] # 读取数据集的行数
    normDataSet = dataSet - np.tile(minVals, (m, 1)) # 现有数据集减去最小值矩阵
    normDataSet = normDataSet / np.tile(ranges, (m, 1)) # 归一化处理

    return normDataSet, ranges, minVals
# ----------------------------------------------------------------
