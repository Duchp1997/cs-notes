
import matplotlib.pyplot as plt
import numpy as np
import dating

# ----------------------------------------------------------------
def showFirstPlot():
    
    datingDataMat, labels = dating.file2matrix('datingTestSet.txt')
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

showFirstPlot()
