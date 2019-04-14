
import matplotlib.pyplot as plt


# 定制文本框和箭头格式
decisionNode = dict(boxstyle = "sawtooth", fc = "1.5")
leafNode     = dict(boxstyle = "round4",   fc = "1.5")
arrow_args   = dict(arrowstyle = "<-")


# -----------------------------------------------------------------------
# 获取叶节点的数目
def get_num_leafs(my_tree):
    num_leafs = 0
    first_str = list(my_tree)[0]
    second_dict = my_tree[first_str]

    for key in second_dict.keys():
        # Test to see if the nodes are dictionaries, if not they are leaf nodes
        if type(second_dict[key]).__name__ == 'dict':
            num_leafs += get_num_leafs(second_dict[key])
        else:
            num_leafs += 1

    return num_leafs


# 获取树的层数
def get_tree_depth(myTree):
    max_depth = 0
    first_str = list(myTree)[0]
    second_dict = myTree[first_str]

    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            this_depth = 1 + get_tree_depth(second_dict[key])
        else:
            this_depth = 1

        max_depth = max(this_depth, max_depth)

    return max_depth


def retrieve_tree(i):
    list_of_trees = [
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

    return list_of_trees[i]


def test_retrieve_tree():
    my_tree = retrieve_tree(0)
    print(get_num_leafs(my_tree))
    print(get_tree_depth(my_tree))
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
# 绘制带箭头的注解
def plot_node(node_txt, center_pt, parent_pt, node_type):
    create_plot.ax1.annotate(
        node_txt, xy = parent_pt, xycoords ='axes fraction',
        xytext = center_pt, textcoords ='axes fraction',
        va = 'center', ha = 'center', bbox = node_type, arrowprops = arrow_args)
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
def plot_mid_text(cntr_pt, parent_pt, txt_string):
    x_mid = (parent_pt[0] - cntr_pt[0]) / 2.0 + cntr_pt[0]
    y_mid = (parent_pt[1] - cntr_pt[1]) / 2.0 + cntr_pt[1]
    create_plot.ax1.text(x_mid, y_mid, txt_string, va ='center', ha ='center', rotation = 30)


# if the first key tells you what feat was split on
def plot_tree(my_tree, parent_pt, node_txt):
    num_leafs = get_num_leafs(my_tree)  # this determines the x width of this tree
    _depth     = get_tree_depth(my_tree)

    first_str = list(my_tree)[0]  # the text label for this node should be this
    cntr_pt = (plot_tree.xOff + (1.0 + float(num_leafs)) / 2.0 / plot_tree.totalW, plot_tree.yOff)
    plot_mid_text(cntr_pt, parent_pt, node_txt)
    plot_node(first_str, cntr_pt, parent_pt, decisionNode)

    second_dict = my_tree[first_str]
    plot_tree.yOff = plot_tree.yOff - 1.0 / plot_tree.totalD

    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            plot_tree(second_dict[key], cntr_pt, str(key))  # recursion
        else:
            plot_tree.xOff = plot_tree.xOff + 1.0 / plot_tree.totalW
            plot_node(second_dict[key], (plot_tree.xOff, plot_tree.yOff), cntr_pt, leafNode)
            plot_mid_text((plot_tree.xOff, plot_tree.yOff), cntr_pt, str(key))

    plot_tree.yOff = plot_tree.yOff + 1.0 / plot_tree.totalD

# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
def create_plot(in_tree):

    fig = plt.figure(num = 1, facecolor='white')  # 创建一个新图形
    fig.clf()  # 清空绘图区
    axprops = dict(xticks = [], yticks = [])
    create_plot.ax1 = plt.subplot(111, frameon = False, **axprops)  # no ticks
    # createPlot.ax1 = plt.subplot(111, frameon = False)  # ticks for demo purposes

    plot_tree.totalW = float(get_num_leafs(in_tree))
    plot_tree.totalD = float(get_tree_depth(in_tree))
    plot_tree.xOff   = -0.5 / plot_tree.totalW
    plot_tree.yOff   = 1.0

    plot_tree(in_tree, (0.5, 1.0), '')
    plt.show()

#def create_plot():
#    fig = plt.figure(num = 1, facecolor='white') # 创建一个新图形
#    fig.clf() # 清空绘图区
#    createPlot.ax1 = plt.subplot(111, frameon = False) # createPlot.ax1 是全局变量

#    plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
#    plotNode('a leaf node',     (0.8, 0.1), (0.3, 0.8), leafNode)
#    plt.show()
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
def test_plot_tree():
    my_tree = retrieve_tree(1)
    create_plot(my_tree)
# -----------------------------------------------------------------------

