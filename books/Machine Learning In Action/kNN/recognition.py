
from os import listdir # listdir能输出目录文件名
from sklearn.neighbors import KNeighborsClassifier as kNN

import numpy as np

# ----------------------------------------------------------------
# 将32x32的文本图像转化为向量
def img2Vector(filename):
    
    fr = open(filename)
    
    # 构建一个行向量
    returnVector = np.zeros((1, 32 * 32), dtype=int)

    for i in range(32):
        lineStr = fr.readline() # 从文件中读取一行
        for j in range(32):
            # 将每行的字符存到行向量中
            returnVector[0, 32 * i + j] = int(lineStr[j])
    
    return returnVector
# ----------------------------------------------------------------


# ----------------------------------------------------------------
# 手写图像识别
def handwritingClassTest():
    
    hwLabels = [] # 测试集的标签矩阵
    trainingFileList = listdir('trainingDigits') # 返回trainingDigits目录下的文件名
    m = len(trainingFileList) # 返回文件夹下文件的个数
    # 初始化训练的Mat矩阵 一个图像一行
    trainingMat = np.zeros((m, 1024))

    # 从文件名中解析出训练集的类别标签
    for i in range(m):
        fileNameStr = trainingFileList[i] # 获取文件名
        # 从文件名中提取图像的类别标签(即识别的数字是多少)
        classNumber = int(fileNameStr.split('_')[0])
        hwLabels.append(classNumber) # 统计标签到hwLabels中
        trainingMat[i,:] = img2Vector('trainingDigits/%s'%(fileNameStr)) # 将文件数据存储到矩阵中
    
    # 构建kNN分类器 近邻数为3 算法为权重均衡算法
    neigh = kNN(n_neighbors = 3, algorithm = 'auto')
    neigh.fit(trainingMat, hwLabels) # 拟合模型 trainingMat为测试矩阵 hwLabels为对应的标签

    testFileList = listdir("testDigits") # 返回 testDigits目录下的文件名
    errorCount = 0.0 # 错误检测计数 初始值为0
    mTest = len(testFileList) # 测试数据量

    # 从文件中解析出测试集的类别并进行测试
    for i in range(mTest):
        fileNameStr = testFileList[i] # 获取文件名
        classNumber = int(fileNameStr.split('_')[0]) # 获取分类的数字标签

        vectorUnderTest = img2Vector("trainingDigits/%s"%(fileNameStr)) # 获取测试集的 1x1024向量 用于训练
        classifierResult = neigh.predict(vectorUnderTest) # 获取预测结果

        print("The classifier came back with: %d, the read answer is: %d"%(classifierResult, classNumber))
        if classifierResult != classNumber:
            errorCount += 1.0

    print("\nThe total number of errors is: %d"%errorCount)
    print("\nThe total error rate is: %f%%"%(errorCount / float(mTest) * 100.0))
# ----------------------------------------------------------------

handwritingClassTest()
