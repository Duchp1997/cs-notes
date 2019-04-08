
import numpy as np
import kNN

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
# 对数据进行测试
def datingClassTest():

    hoRatio = 0.1 # 10%数据作为测试集
    
    # 得到数据集矩阵 和 类别label
    datingDataMat, datingLabels = file2matrix("datingTestSet.txt")
    # 归一化数据
    normMat, _ranges, _minVals = kNN.autoNorm(datingDataMat)
    m = normMat.shape[0] # 获取数据集矩阵的行数
    numTestVecs = int(m * hoRatio) # 获取测试集的行数
    errorCount = 0.0 # 错误数

    # 计算测试集错误率
    for i in range(numTestVecs):
        # 执行分类器
        classifierResult = kNN.classify0(normMat[i,:], normMat[numTestVecs:m,:], datingLabels[numTestVecs:m], 3)

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
    normMat, ranges, minVals = kNN.autoNorm(datingDataMat)
    # 测试样本
    inArr = np.array([ffmiles, percentTats, icecream])
    # 归一化测试样本
    inArr = (inArr - minVals) / ranges

    # 计数预测结果
    classifierResult = kNN.classify0(inArr, normMat, datingLabels, 3)
    print('You will probably like this guy: ', resultList[classifierResult - 1])
# ----------------------------------------------------------------
