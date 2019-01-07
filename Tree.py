from math import log
import operator
def calcShannonEnt(dataSet):
    #熵越高 混合的数据越多
    numEntries= len(dataSet) #数据集中数据个数
    labelCounts={}#创建一个空的字典用存储label
    for featVec in dataSet:
        #统计dataSet中的各个label的个数
        currentLabel=featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel]+=1
    shannonEnt=0.0
    for key in labelCounts:
        prob=float(labelCounts[key]/numEntries) #计算每个label出现的概率
        shannonEnt-=prob*log(prob,2)    #计算期望
    return shannonEnt
def createDataSet():
    dataSet=[[1,1,'yes'],
             [1,1,'yes'],
             [1,0,'no'],
             [0,1,'no'],
             [0,0,'no']]
    lables=['no surfacing','flippers']
    return dataSet,lables
def splitDataSet(dataSet, axis, value):
    #待划分的数据集 划分数据集的特征 特征的返回值
    retDataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            #if里将axis值抽取出来，将除了axis值的其他值存入
            reducedFeatVec=featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet
def chooseBestFeatureToSplit(dataSet):
    """
    按照每一个特征值先划分好
    然后计算按照各个特征值划分好之后的信息熵
    取最高的信息熵作为最佳划分依据
    """
    numFeatures=len(dataSet[0])-1 #数据集中的一个的数据个数
    baseEntropy=calcShannonEnt(dataSet) #计算香农熵
    bestInfoGain=0.0;bestFeature=-1
    for i in range(numFeatures):
        featList=[example[i] for example in dataSet] #取一列分列标签列
        uniqueVals=set(featList) # 转化为集合类型 创建唯一的分类标签列表
        newEntropy=0.0
        for value in uniqueVals:
            #计算每种划分方式的信息熵
            subDataSet=splitDataSet(dataSet,i,value)
            prob=len(subDataSet)/float(len(dataSet))
            newEntropy+=prob*calcShannonEnt(subDataSet)
        infoGain=baseEntropy-newEntropy
        if infoGain>bestInfoGain:               #如果当前所得的熵比最佳熵要高，就替换
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature      #返回信息熵最高的那一列信息值
def majorityCnt(classList):
    """
    用来处理特征值用光了但是
    下列分列中任然有不同类型
    值的时候通过多数表决来确
    定这种情况下属于哪一种类
    型
    """
    classCount={} #建立一个空的字典
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote]=0
        classCount[vote] += 1
    #记录每个类标签出现的次数
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reversed=True)#降序排序
    return sortedClassCount[0][0]
def createTree(dataSet,labels):
    classList=[example[-1] for example in dataSet]
    #读取dataSet中每一个的类别写入classList
    if classList.count(classList[0])==len(classList):
    #count用于统计某个数据在列表中出现的次数，
    #这里意思是如果classList中所有的都是同一
    #个类别，说明类别完全相同，停止划分
        return classList[0]
    if len(dataSet[0])==1:          #说明特征值用完了 dataSet[0]指从dataSet中取第一个元素，看长度
        return majorityCnt(classList)
    bestFeat=chooseBestFeatureToSplit(dataSet)  #取到最佳划分的特征值
    bestfeatLabel=labels[bestFeat]              #抽出最佳特征值
    myTree={bestfeatLabel:{}}
    del(labels[bestFeat])
    featValues=[example[bestFeat] for example in dataSet]   #取出最佳特征值的那一列数据
    uniqueVals=set(featValues) #转成集合
    for value in uniqueVals:
        subLabels=labels[:]#python中的函数参数是列表类型时，参数按照引用传递，避免递归调用中改变list的原始数据
        myTree[bestfeatLabel][value]=createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree








