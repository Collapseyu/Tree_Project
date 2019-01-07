import matplotlib.pyplot as plt
decisionNode=dict(boxstyle="sawtooth",fc="0.8")#字典 决策节点
leafNode=dict(boxstyle="round4",fc="0.8")#叶节点
arrow_args=dict(arrowstyle="<-")
"""
定义文本框和箭头
"""
def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    #annotate()该函数的作用是为绘制的图上指定的数据点xy添加一个注释nodeTxt,注释的位置由xytext指定
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,
                                xycoords='axes fraction',xytext=centerPt,
                                textcoords='axes fraction',va="center",ha="center"
                                ,bbox=nodeType,arrowprops=arrow_args)
    #用的createPlot时下列
    """
def createPlot():
    fig=plt.figure(1,facecolor='white')
    fig.clf()
    createPlot.ax1=plt.subplot(111,frameon=False)
    plotNode('a decision node',(0.5,0.1),(0.1,0.5),decisionNode)#(标识，箭头指向点，起始点，样式)
    plotNode('a leaf node ',(0.8,0.1),(0.3,0.8),leafNode)
    plt.show() 
    """
def getNumLeafs(myTree):
    #获取决策树的叶节点数量
    numLeafs=0
    firstStr=list(myTree.keys())[0]#字典中的第一个键值
    secondDict=myTree[firstStr]#第一个键值中存储的数据
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':    #如果当前key为一个字典 就用递归获取叶节点数量
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs
def getTreeDepth(myTree):
    maxDepth=0
    firstStr=list(myTree.keys())[0]
    secondDict=myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':            #如果当前key值的数据为一个字典，则递归调用 在secondDict中遍历
            thisDepth = 1+getTreeDepth(secondDict[key])
        else:
            thisDepth = 1                        #否则最大深度+1
        if thisDepth > maxDepth: maxDepth = thisDepth   #判断子树下是否有深度更深的
    return maxDepth
def retrieveTree(i):
    listOfTrees=[{'no surfacing':{0:'no',1:
                                        {'flippers':{0:'no',1:'yes'}}}},
                 {'no surfacing':{0:'no',1:
                                        {'flippers':{0:
                                                    {'head':{0:'no',1:'yes'}},
                                                     1:'no'}}}}]
    return listOfTrees[i]
def plotMidText(cntrPt, parentPt, txtString):#父子节点间填充文本信息
    xMid=(parentPt[0]-cntrPt[0])/2.0+cntrPt[0]  #（父节点-子节点)/2+子节点
    yMid=(parentPt[1]-cntrPt[1])/2.0+cntrPt[1]
    createPlot.ax1.text(xMid,yMid,txtString)
def plotTree(myTree, parentPt, nodeTxt):
    numLeafs=getNumLeafs(myTree)
    depth=getTreeDepth(myTree)
    firstStr=list(myTree.keys())[0]  #获取数的第一个key值
    cntrPt=(plotTree.xOff+(1.0+float(numLeafs))/2.0/plotTree.totalW,plotTree.yOff)
    plotMidText(cntrPt,parentPt,nodeTxt)
    plotNode(firstStr,cntrPt,parentPt,decisionNode) #指向子树
    secondDict=myTree[firstStr]
    plotTree.yOff=plotTree.yOff-1.0/plotTree.totalD #减少y偏移
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            plotTree(secondDict[key],cntrPt,str(key))
        else:
            plotTree.xOff=plotTree.xOff+1.0/plotTree.totalW
            plotNode(secondDict[key],(plotTree.xOff,plotTree.yOff),cntrPt,leafNode)
            plotMidText((plotTree.xOff,plotTree.yOff),cntrPt,str(key))
    plotTree.yOff=plotTree.yOff+1.0/plotTree.totalD
def createPlot(inTree):
    fig=plt.figure(1,facecolor='white')
    fig.clf()
    axprops=dict(xticks=[] ,yticks=[])
    createPlot.ax1=plt.subplot(111,frameon=False,**axprops)
    plotTree.totalW=float(getNumLeafs(inTree))
    plotTree.totalD=float(getTreeDepth(inTree))
    plotTree.xOff = -0.5 / plotTree.totalW;
    plotTree.yOff = 1.0;
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()







