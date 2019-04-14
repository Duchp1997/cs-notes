
import tree
import treePlotter


def test_lenses():

    fr = open('lenses.txt')
    lenses_data = [inst.strip().split('\t') for inst in fr.readlines()]

    lenses_labels = ['age', 'prescript', 'astigmatic', 'tearRate']
    lenses_tree = tree.create_tree(lenses_data, lenses_labels)

    print(lenses_tree)
    treePlotter.create_plot(lenses_tree)


test_lenses()
