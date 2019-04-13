
import matplotlib.pyplot as plt


# 定制文本框和箭头格式
decisionNode = dict(boxstyle = "sawtooth", fc = "1.5")
leafNode     = dict(boxstyle = "round4",   fc = "1.5")
arrow_args   = dict(arrowstyle = "<-")


# -----------------------------------------------------------------------
# 获取叶节点的数目
def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree)[0]
    secondDict = myTree[firstStr]

    for key in secondDict.keys():
        # Test to see if the nodes are dictionaries, if not they are leaf nodes
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1

    return numLeafs

# 获取树的层数
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree)[0]
    secondDict = myTree[firstStr]

    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        
        maxDepth = max(thisDepth, maxDepth)

    return maxDepth


def retrieveTree(i):
    listOfTrees = [
        {
            'no surfacing': {
                0: 'no',
                1: {
                    'flippers': {
                        0: 'no',
                        1: 'yes',
                    }
                }
            }
        },
        {
            'no surfacing': {
                0: 'no',
                1: {
                    'flippers': {
                        0: {
                            'head': {
                                0: 'no',
                                1: 'yes',
                            }
                        },
                        1: 'no'
                    }
                }
            }
        }
    ]

    return listOfTrees[i]


def testRetrieveTree():
    myTree = retrieveTree(0)
    print(getNumLeafs(myTree))
    print(getTreeDepth(myTree))
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
# 绘制带箭头的注解
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(
        nodeTxt, xy = parentPt, xycoords = 'axes fraction',
        xytext = centerPt, textcoords = 'axes fraction',
        va = 'center', ha = 'center', bbox = nodeType, arrowprops = arrow_args)
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va = 'center', ha = 'center', rotation = 30)


# if the first key tells you what feat was split on
def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree) # this determines the x width of this tree
    depth    = getTreeDepth(myTree)

    firstStr = list(myTree)[0] # the text label for this node should be this
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)

    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD

    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], cntrPt, str(key)) # recursion
        else:
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))

    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD

# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
def createPlot(inTree):
    fig = plt.figure(num = 1, facecolor='white') # 创建一个新图形
    fig.clf() # 清空绘图区
    axprops = dict(xticks = [], yticks = [])
    createPlot.ax1 = plt.subplot(111, frameon = False, **axprops) # no ticks
    # createPlot.ax1 = plt.subplot(111, frameon = False) # ticks for demo purposes

    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff   = -0.5 / plotTree.totalW;
    plotTree.yOff   = 1.0
    
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()

#def createPlot():
#    fig = plt.figure(num = 1, facecolor='white') # 创建一个新图形
#    fig.clf() # 清空绘图区
#    createPlot.ax1 = plt.subplot(111, frameon = False) # createPlot.ax1 是全局变量
    
#    plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
#    plotNode('a leaf node',     (0.8, 0.1), (0.3, 0.8), leafNode)
#    plt.show()
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
def testPlotTree():
    myTree = retrieveTree(1)
    createPlot(myTree)
# -----------------------------------------------------------------------


testPlotTree()