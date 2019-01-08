import Tree
import treePlotter
fr=open('lenses.txt')
lense=[inst.strip().split('\t') for inst in fr.readlines()] #用'\t'分割
lenseLabels=['age','prescript','astigmatic','tearRate']
lenseTree=Tree.createTree(lense,lenseLabels)
print(lenseTree)
treePlotter.createPlot(lenseTree)
Tree.storeTree(lenseTree,'lenseTree.txt')