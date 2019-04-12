
import numpy as np
import operator
import math

# 计算香农熵 -----------------------------------------------------------------
def calcShannonEnt(dataSet):
    
    numEntries = len(dataSet) # 获取数据集的文件数目
    labelCounts = {} # 建立一个便签矩阵 存放对应的标签值

    # 统计所有的标签
    for featrueVec in dataSet:
        currentLabels = featrueVec[-1] # 取featureVec的最后一个元素 即标签元素
        
        if currentLabels not in labelCounts.keys():
            labelCounts[currentLabels] = 0
        labelCounts[currentLabels] += 1

    shannonEnt = 0.0 # 熵清零

    # 根据信息熵的公式计算
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * math.log(prob, 2)

    return shannonEnt
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
def createDataSet():

    dataSet = ([
        [1,1,'Yes'],
        [1,1,'Yes'],
        [1,0,'No'],
        [0,1,'No'],
        [0,1,'No'],
    ])

    labels = ['no surfacing', 'flippers']

    return dataSet, labels

def testShannonEnt():
    myDat, labels = createDataSet()
    print(myDat)

    print(calcShannonEnt(myDat))
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 按照给定特征对数据集进行划分 输入参数依次是数据集 划分数据集的特征和特征返回值
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value: # 若发现特征与目标值一致
            reducedFeatVec = featVec[:axis] # 将axis之前的列的引用添加到reducedFeatVec中
            reducedFeatVec.extend(featVec[axis+1:]) # 将axis之后的列的引用添加到reducedFeatVec中
            retDataSet.append(reducedFeatVec) # 将去除了指定特征列的数据集放在retDataSet中

    return retDataSet


def testSplit():
    myDat, labels = createDataSet()
    print(myDat)

    print(splitDataSet(myDat, 0, 1))
    print(splitDataSet(myDat, 0, 0))
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 选择最好的分割点
def chooseBestFeatureToSplit(dataSet):

    featureCount = len(dataSet[0]) - 1 # 对数据集第一行的长度 即特征个数
    dataCount = float(len(dataSet)) # 数据集的样例个数

    baseShannonEnt = calcShannonEnt(dataSet) # 算出初始的香农熵
    bestGain = 0.0 # 初始化最高信息增益
    bestFeature = -1 # 初始化最佳分割点

    for i in range(featureCount): # 计算每个特征的信息熵
        featList = [example[i] for example in dataSet] # 遍历所有数据的第i个特征
        uniqueVals = set(featList) # 去除第i个特征的重复值

        newEnt = 0.0 # 初始化当前信息熵
        for value in uniqueVals: # 遍历第i个特征的所有取值
            subDataSet = splitDataSet(dataSet, i, value) # 不同特征值处分割
            prob = len(subDataSet) / dataCount
            newEnt += prob * calcShannonEnt(subDataSet) # 计算此时的信息熵

        infoGain = baseShannonEnt - newEnt # 计算信息增益
        if infoGain > bestGain:
            bestGain = infoGain
            bestFeature = i # 记录下最佳分割的特征

    return bestFeature
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 多数表决分类函数
def majorityCnt(classList):
    classCount = {} # 建立数据字典 存储所有的类别
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0 # 如果有新类别 则创立一个新的元素代表该类
        classCount[vote] += 1

    # 对数据集进行排序 数据的第二个元素(1)作为排序依据
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reversed=True)
    return sortedClassCount[0][0] # 返回出现次数最多的元素

# 构建决策树
def createTree(dataSet, labels):
    # 以训练集的最后一列作为一个新的列表
    classList = [example[-1] for example in dataSet]

    # 如果原本全属于同一类别
    if classList.count(classList[0]) == len(classList):
        return classList[0] # 直接返回该类别

    # 如果候选特征只剩一个
    if len(dataSet[0]) == 1:
        return majorityCnt(classList) # 返回该特征出现次数最多的类别

    # 从候选的特征中选择一个最佳的特征
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat] # 记录最优特征的标签

    myTree = {bestFeatLabel:{}} # 根据最优标签生成树
    del(labels[bestFeat]) # 去除已经使用过的标签

    # 获取训练集中最优特征属性值
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues) # 去除重复的值

    for value in uniqueVals: #遍历所选特征的所有候选值
        subLabels = labels[:] # 把label完全复制一遍
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)

    return myTree


def testTreeCreation():
    myDat, labels = createDataSet()
    myTree = createTree(myDat, labels)
    print(myTree)
# ---------------------------------------------------------------------------
