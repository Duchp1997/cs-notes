
import numpy as np
import kNN

# ----------------------------------------------------------------
def createDataSet():
    group = np.array([[1.0, 1.1], [1.0, 1.0], [0.0, 0.0], [0.0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels
# ----------------------------------------------------------------


# ----------------------------------------------------------------
def knn_test():
    group, labels = createDataSet()
    result = kNN.classify0([0, 0], group, labels, 3)
    print(result)
# ----------------------------------------------------------------

knn_test()
