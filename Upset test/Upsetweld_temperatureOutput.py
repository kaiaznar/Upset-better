from abaqus import *
from abaqusConstants import *
import odbAccess
import annotationToolset
from odbAccess import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()


def MakeXY(baseName,initialX,initialY,limitDistance,historyVariable,remeshPoints):
    remeshNumber = 0
    totalTime = 0.0
    pointX0 = initialX
    pointY0 = initialY
    cont = True
    totalList = []
    remeshPointsList = []
    xyList = []
    xyList.append((initialX, initialY))
    while cont:
        print "Processing remesh number ",remeshNumber
        if remeshNumber == 0:
            fileName = baseName + ".odb"
        else:
            fileName = baseName + "_remesh_" + "%i" % (remeshNumber) + ".odb"
        try:
            odb = session.openOdb(name=fileName)
#-----------pointInfo------------------------
            pointXf = 0.0
            pointYf = 0.0
            dX = 0.0
            dY = 0.0
            weightSum = 0.0
            nodeName=[]
            nodeCoordX1=[]
            nodeCoordY1=[]
            nodeCoordX2=[]
            nodeCoordY2=[]
            nodeWeight=[]
            f1 = odb.steps['Weld step'].frames[1]
            f2 = odb.steps['Weld step'].frames[-1] #Last frame
            for value in f1.fieldOutputs['COORD'].values:
                thisPoint = value.data
                thisDistance=((thisPoint[0]-pointX0)**2+(thisPoint[1]-pointY0)**2)**0.5
                if thisDistance < limitDistance:
                    nodeName.append(value.nodeLabel)
                    nodeCoordX1.append(thisPoint[0])
                    nodeCoordY1.append(thisPoint[1])
                    nodeWeight.append(limitDistance-thisDistance)
            for i in range(len(nodeName)):
                for value in f2.fieldOutputs['COORD'].values:
                    if value.nodeLabel == nodeName[i]:
                        if value.instance.name == "TOPPIPE_WELD-1":
                            thisPoint = value.data
                            nodeCoordX2.append(thisPoint[0])
                            nodeCoordY2.append(thisPoint[1])
            for i in range(len(nodeWeight)):
                weightSum=weightSum+nodeWeight[i]
            for i in range(len(nodeName)):
                dX=dX+nodeWeight[i]/weightSum*(nodeCoordX2[i]-nodeCoordX1[i])
                dY=dY+nodeWeight[i]/weightSum*(nodeCoordY2[i]-nodeCoordY1[i])
            pointXf=pointX0+dX
            pointYf=pointY0+dY
#------------------------
            frameCount = 0
            thisTemp = 0.0
            stepTime = f2.frameValue
            for i in range(len(nodeName)):
                for value in f2.fieldOutputs['NT11'].values:
                    if value.nodeLabel == nodeName[i]:
                        if value.instance.name == "TOPPIPE_WELD-1":
                             thisTemp = thisTemp + value.data*nodeWeight[i]/weightSum
            totalList.append((stepTime+totalTime,thisTemp))
            remeshNumber = remeshNumber + 1
            totalTime = totalTime + stepTime
            xyList.append((pointXf, pointYf))
            pointX0 = pointXf
            pointY0 = pointYf
            session.odbs[fileName].close()
        except:
            cont = False
        
    xQuantity = visualization.QuantityType(type=NONE)
    yQuantity = visualization.QuantityType(type=NONE)
    session.XYData(name=historyVariable, data=tuple(totalList),
                   axis1QuantityType=xQuantity, 
                   axis2QuantityType=yQuantity, )
#
    session.XYData(name='xy' + historyVariable, data=tuple(xyList),
                   axis1QuantityType=xQuantity, 
                   axis2QuantityType=yQuantity, )

#


#MakeXY(baseName,initialX,initialY,limitDistance,historyVariable,remeshPoints):
baseName="Upset_weld"
initialX = 125.25
initialY = 24.49
limitDistance = 2.5
historyVariable = 'Thermocouple Temperature'
remeshPoints = False


MakeXY(baseName,initialX,initialY+15,limitDistance,'Temp15',remeshPoints)
MakeXY(baseName,initialX,initialY+20,limitDistance,'Temp20',remeshPoints)
MakeXY(baseName,initialX,initialY+25,limitDistance,'Temp25',remeshPoints)