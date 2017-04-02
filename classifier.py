import os
from numpy import *
import KNN
from img2Vector import img2Vector

import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt


class Classifier(object):
    def __init__(self):
        #self.createLib('training_ori')
        #self.createLib('testing_ori')
        if os.path.exists('k'):
            with open('k') as fr:
                self.k = int(fr.readline())
        else:
            self.k = 3
    def createLib(self, imgDir):
        imgList = os.listdir(imgDir)
        vectorDir = imgDir.split('_')[0]
        labelCounter = {}
        if not os.path.exists(vectorDir):
            os.mkdir(vectorDir)
            labels = os.listdir(vectorDir)
            for label in labels:
                labelCounter[label] = len(os.listdir(vectorDir + '/' + label))
            for imgName in imgList:
                print("converting %s..." % imgName)
                vectorList = img2Vector(imgDir + '/' + imgName)
                for i in range(4):
                    label = imgName[i]
                    vector = vectorList[i]
                    fullVectorPath = vectorDir + '/' + label
                    if not os.path.exists(fullVectorPath):
                        os.mkdir(fullVectorPath)
                    labelCounter[label] = labelCounter.get(label, 0) + 1
                    with open(fullVectorPath + '/' + str(labelCounter[label]), 'w') as f:
                        for num in vector:
                            f.write(str(num))
    def readFile(self, fileNameStr):
        returnMat = zeros((1,324))
        with open(fileNameStr) as f:
            vectorStr = f.readline()
        for i in range(324):
            returnMat[0, i] = int(vectorStr[i])
        return returnMat
    def loadTrainingMat(self):
        trainingFileList = []
        self.labels = []
        for label in os.listdir('training'):
            for each in os.listdir('training/' + label):
                trainingFileList.append('training/' + label + '/' + each)
                self.labels.append(label)
        m = len(trainingFileList)
        self.trainingMat = zeros((m, 324))
        for i in range(m):
            self.trainingMat[i, :] = self.readFile(trainingFileList[i])
    def checkCodeTest(self):
        testFileList = []
        errorCount = 0

        for label in os.listdir('testing'):
            for each in os.listdir('testing/' + label):
                testFileList.append('testing/' + label + '/' + each)
        mTest = len(testFileList)
        for i in range(mTest):
            fileNameStr = testFileList[i]
            classChar = fileNameStr.split('/')[1]
            vectorUnderTest = self.readFile(fileNameStr)
            classifierResult = KNN.classify0(vectorUnderTest, self.trainingMat, self.labels, self.k)
            print("the classifier came back with: %s, the real answer is: %s" %(classifierResult, classChar))
            if(classChar != classifierResult):
                errorCount += 1.0
        print("the total number of class is %d, number of error is %d" % (mTest, errorCount))
        print("the total error rate is %f" % (errorCount/float(mTest)))
    def autoRename(self):
        for imgName in os.listdir('rename'):
            nameList = []
            vectorList = img2Vector('rename/'+imgName)
            for vector in vectorList:
                nameList.append(KNN.classify0(vector, self.trainingMat, self.labels, self.k))
            os.rename('rename/'+imgName, 'rename/'+''.join(nameList)+'.gif')
            print("renaming " + ''.join(nameList)+ '.gif...')
    def findBestk(self, kMin, kMax):
        plotMat = zeros((2, kMax-kMin))
        for i in range(kMax - kMin):
            plotMat[0, i] = i
            plotMat[1, i] = checkCodeTest(i)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(plotMat[0, :], plotMat[1, :])
        plt.show()
    def recognizer(self, imgPath):
        vectorList = img2Vector(imgPath)
        nameList = []
        for vector in vectorList:
            nameList.append(KNN.classify0(vector, self.trainingMat, self.labels, self.k))
        return ''.join(nameList)
