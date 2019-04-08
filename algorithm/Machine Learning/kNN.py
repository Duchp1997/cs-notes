
import numpy as np;
import operator;
import matplotlib;
import matplotlib.pyplot as plt;

def createDataSet():
    group = np.array([[1.0, 1.1], [1.0, 1.0], [0.0, 0.0], [0.0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

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
def knn_test1():
    group, labels = createDataSet()
    result = classify0([0, 0], group, labels, 3)
    print(result)
# ----------------------------------------------------------------


# ----------------------------------------------------------------
# 将文本记录转化为Numpy矩阵
def file2matrix(filename):
    love_dictionary = {'largeDoses':3, 'smallDoses':2, 'didntLike':1}

    fr = open(filename) # 打开文件
    array_lines = fr.readlines() # 按行读取 array_lines
    lines_count = len(array_lines) # 获取其行数

    # result_matrix 存储最终结果 lines_count行 3列
    result_matrix = np.zeros((lines_count, 3))
    classLabelVector = [] # 建立一个列向量 存储类别
    index = 0 # 开始时索引值为0
    
    # 按行读取文本 并依次贴上label
    for line in array_lines:
        line = line.strip() # 去掉字符串中的首尾多余空格
        listFromLine = line.split('\t') # 以 '\t' 分割每行的数据
        result_matrix[index,:] = listFromLine[0: 3] # 将每一行的前3个元素依次存储到矩阵中
        # 对于每行的最后一列 按照值的不同 给列向量赋值
        if(listFromLine[-1].isdigit()):
            classLabelVector.append(int(listFromLine[-1]))
        else:
            classLabelVector.append(love_dictionary.get(listFromLine[-1]))
        
        index += 1
    
    # 一个为由三个特征组成的特征矩阵 另一个为类别的类向量
    return result_matrix, classLabelVector
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

# ----------------------------------------------------------------
# 对数据进行测试
def datingClassTest():

    hoRatio = 0.1 # 10%数据作为测试集
    
    # 得到数据集矩阵 和 类别label
    datingDataMat, datingLabels = file2matrix("datingTestSet.txt")
    # 归一化数据
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0] # 获取数据集矩阵的行数
    numTestVecs = int(m * hoRatio) # 获取测试集的行数
    errorCount = 0.0 # 错误数

    # 计算测试集错误率
    for i in range(numTestVecs):
        # 执行分类器
        classifierResult = classify0(normMat[i,:], normMat[numTestVecs:m,:], datingLabels[numTestVecs:m], 3)

        print('the classifier came back with: %d, the read answer is %d'%(classifierResult, datingLabels[i]))
        # 如果分类器结果与label值不一致 统计为错误
        if classifierResult != datingLabels[i]:
            errorCount += 1
    
    # 输出错误率
    print('the total error rate is %f%%'%(errorCount / float(numTestVecs) * 100))

# ----------------------------------------------------------------

# ----------------------------------------------------------------
# 约会对象评价预测
def classifyPerson():
    # 输出的所有可能结果
    resultList = ['not at all', 'in small doses', 'in large doses']
    # 输入在游戏上花时间的比重
    percentTats = float(input('Percentage of time wpent playing video games?'))
    # 输入每年的飞行里程
    ffmiles = float(input('frequent flier miles sarned per year?'))
    # 输入冰淇淋消耗量
    icecream = float(input('liters of ice cream consumed per year?'))

    # 把训练集文本数据转化为向量 便于后续处理
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    # 数据归一化
    normMat, ranges, minVals = autoNorm(datingDataMat)
    # 测试样本
    inArr = np.array([ffmiles, percentTats, icecream])
    # 归一化测试样本
    inArr = (inArr - minVals) / ranges

    # 计数预测结果
    classifierResult = classify0(inArr, normMat, datingLabels, 3)
    print('You will probably like this guy: ', resultList[classifierResult - 1])
# ----------------------------------------------------------------

# ----------------------------------------------------------------
def showFirstPlot():
    
    datingDataMat, labels = file2matrix('datingTestSet.txt')
    # datingDataMat, _ranges, _minVals = autoNorm(datingDataMat)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    # 生成散点图 显示矩阵第2和第3列的数据
    ax.scatter(
        datingDataMat[:,1], # 横轴
        datingDataMat[:,2], # 纵轴
        c = 15.0 * np.array(labels), # c为颜色序列
        s = 15.0 * np.array(labels)  # s为大小
    )
    ax.axis([-2,25,-0.2,2.0])
    plt.xlabel('Percentage of Time Spent Playing Video Games')
    plt.ylabel('Liters of Ice Cream Consumed Per Week')
    plt.show()
# ----------------------------------------------------------------



# showFirstPlot()
