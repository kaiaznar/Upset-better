#-------------------------------------------------------------------------------
##
## Apply seeds bellow a y-coordinate
## +
def seedNearZeroTop(instanceName,elementSize,coordinate):
    from abaqus import *
    from assembly import *
    from mesh import *
    assembly = mdb.models['Model-1'].rootAssembly
    e = assembly.instances[instanceName].edges
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if (y <= coordinate):
	    edges = (e[k],)
	    assembly.seedEdgeBySize(edges=edges, size=elementSize)

#-------------------------------------------------------------------------------
##
## Apply seeds above a y-coordinate
## -
def seedNearZeroBottom(instanceName,elementSize,coordinate):
    from abaqus import *
    from assembly import *
    from mesh import *
    assembly = mdb.models['Model-1'].rootAssembly
    e = assembly.instances[instanceName].edges
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if (y >= coordinate):
	    edges = (e[k],)
	    assembly.seedEdgeBySize(edges=edges, size=elementSize)

#-------------------------------------------------------------------------------
##
## Apply seeds left to a x-coordinate
## -
def seedNearZeroLeftTo(instanceName,elementSize,coordinate):
    from abaqus import *
    from assembly import *
    from mesh import *
    assembly = mdb.models['Model-1'].rootAssembly
    e = assembly.instances[instanceName].edges
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if (x <= coordinate):
	    edges = (e[k],)
	    assembly.seedEdgeBySize(edges=edges, size=elementSize)

#-------------------------------------------------------------------------------
##
## Apply seeds above a radius value
## -
def seedNearZeroTopR(instanceName,elementSize,centerX,centerY,radius):
    from abaqus import *
    from assembly import *
    from mesh import *
    assembly = mdb.models['Model-1'].rootAssembly
    e = assembly.instances[instanceName].edges
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	r=sqrt((x-centerX)**2+(y-centerY)**2)
	if ((r >= radius) and (y < centerY)):
	    edges = (e[k],)
	    assembly.seedEdgeBySize(edges=edges, size=elementSize)

#-------------------------------------------------------------------------------
##
## Apply seeds above a y-coordinate
## -
def seedNearZeroBottomR(instanceName,elementSize,centerX,centerY,radius):
    from abaqus import *
    from assembly import *
    from mesh import *
    assembly = mdb.models['Model-1'].rootAssembly
    e = assembly.instances[instanceName].edges
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	r=sqrt((x-centerX)**2+(y-centerY)**2)
	if (r <= radius):
	    edges = (e[k],)
	    assembly.seedEdgeBySize(edges=edges, size=elementSize)

##
## Delete all edge seeds
## +
def removeEdgeSeeds(instanceName):
    from abaqus import *
    from assembly import *
    assembly = mdb.models['Model-1'].rootAssembly
    e = assembly.instances[instanceName].edges
    for k in range(len(e)):
	assembly.deleteSeeds(regions=(e[k],))

##
## Partition an upper part while trying to avoid existing vertices
## + -
def sliceTopInstance(instanceName,cutPosition,nearWeldMeshSize):
    from abaqus import *
    from assembly import *
    from part import *
    a = mdb.models['Model-1'].rootAssembly
    #
    # Move the cut position to avoid cutting too near an existing vertex
    #mainWindow.writeToMessageArea('**********estou no slice')
    while nearestVertexDistance(cutPosition,instanceName) < nearWeldMeshSize:
	cutPosition = cutPosition + nearWeldMeshSize/10.
    a.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=cutPosition)
    d1 = a.datums
    datumList = d1.keys()
    datumList.sort()
    thisPlane = datumList[len(datumList)-1]
    f = a.instances[instanceName].faces
    faceLength = len(f)
    for j in range(faceLength):
	try:
	    a.PartitionFaceByDatumPlane(faces=f[j], datumPlane=d1[thisPlane])
	    a.regenerate()
	except:
	    pass
    return cutPosition

##
## Partition an upper part vertically
## -
def sliceVerticalInstance(instanceName,cutPosition):
    from abaqus import *
    from assembly import *
    from part import *
    a = mdb.models['Model-1'].rootAssembly
    a.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=cutPosition)
    d1 = a.datums
    datumList = d1.keys()
    datumList.sort()
    thisPlane = datumList[len(datumList)-1]
    e = a.instances[instanceName].edges
    allEdges = e[0:len(e)]
    a.PartitionEdgeByDatumPlane(edges=allEdges, datumPlane=d1[thisPlane])
    a.regenerate()

##
## Partition a lower part while trying to avoid existing vertices
## + -
def sliceBottomInstance(instanceName,cutPosition,nearWeldMeshSize): 
    from abaqus import *
    from assembly import *
    from part import *
    a = mdb.models['Model-1'].rootAssembly
    #
    # Move the cut position to avoid cutting too near an existing vertex
    while nearestVertexDistance(cutPosition,instanceName) < nearWeldMeshSize:
	cutPosition = cutPosition - nearWeldMeshSize/10.
    a.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=cutPosition)
    d1 = a.datums
    datumList = d1.keys()
    datumList.sort()
    thisPlane = datumList[len(datumList)-1]
    f = a.instances[instanceName].faces
    faceLength = len(f)
    for j in range(faceLength):
	try:
	    a.PartitionFaceByDatumPlane(faces=f[j], datumPlane=d1[thisPlane])
	    a.regenerate()
	except:
	    pass
    return cutPosition

##
## Create a surface comprised of edges near the top of a part
## +
def surfaceNearTop(instanceName,surfaceName,distance):
    from abaqus import *
    from assembly import *
    #
    # Note: This isn't useful for defining contact surfaces
    # since it will pick up internal edges generally
    # 
    assembly = mdb.models['Model-1'].rootAssembly
    e = assembly.instances[instanceName].edges
    sideEdges = []
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if (y >= distance):
	    sideEdges.append(e[k:k+1])
    assembly.GeometrySurface(name=surfaceName, geometrySurfaceSeq=((sideEdges, SIDE1), ))
##
## Create a surface comprised of edges near the bottom of a part
## +
def surfaceNearBottom(instanceName,surfaceName,distance):
    from abaqus import *
    from assembly import *
    #
    # Note: This isn't useful for definining contact surfaces
    # since it will pick up internal edges generally
    # 
    assembly = mdb.models['Model-1'].rootAssembly
    e = assembly.instances[instanceName].edges
    sideEdges = []
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if (y <= distance):
	    sideEdges.append(e[k:k+1])
    assembly.GeometrySurface(name=surfaceName, geometrySurfaceSeq=((sideEdges, SIDE1), ))
	
##
## Return the elevation difference to the nearest vertex
## + 
def nearestVertexDistance(position,instanceName):
    from abaqus import *
    from assembly import *
    a = mdb.models['Model-1'].rootAssembly
    v = a.instances[instanceName].vertices
    nearestDistance = 99999
    for k in range(len(v)):
	((x,y,z),) = v[k].pointOn
	distance = abs(position-y)
	if distance < nearestDistance:
	    nearestDistance = distance
    return nearestDistance

##
## Return the block location of the first occurence a keyword in the input file
## +
def whereIsBlock(keyword):
    from abaqus import *
    blocks = mdb.models['Model-1'].keywordBlock.sieBlocks
    for i in range(len(blocks)):
         b=blocks[i]
         if b[:len(keyword)] == keyword:
             break
    return i

##
## Return the block location of the last occurence a keyword in the input file
## +
def whereIsLastBlock(keyword):
    from abaqus import *
    blocks = mdb.models['Model-1'].keywordBlock.sieBlocks
    for i in range(len(blocks)):
         b=blocks[i]
         if b[:len(keyword)] == keyword:
             blockFound = i
    return blockFound

##
## Return the block location of the last occurence a keyword in the input file
## -
def whereIsSecondLastBlock(keyword):
    from abaqus import *
    blocks = mdb.models['Model-1'].keywordBlock.sieBlocks
    blockFound=0
    for i in range(len(blocks)):
         b=blocks[i]
         if b[:len(keyword)] == keyword:
             secondLast = blockFound
             blockFound = i
    return secondLast

##
## Return the block location of the last occurence a keyword in the input file
## -
def whereIsThirdLastBlock(keyword):
    from abaqus import *
    blocks = mdb.models['Model-1'].keywordBlock.sieBlocks
    blockFound=0
    secondLast=0
    for i in range(len(blocks)):
         b=blocks[i]
         if b[:len(keyword)] == keyword:
             thirdLast = secondLast
             secondLast = blockFound
             blockFound = i
    return thirdLast

#------------------------------------------------------------------------------------------
#Log files, etc
# +
def openLogFile(name):
    from sys import *
    import osutils
    try:
	osutils.remove(name + "_simulation.log")
    except:
	pass
    logFile = open(name + "_simulation.log",'w')
    return logFile
# +
def writeHeading(logFile):
    from sys import *
    logFile.write('******************************************\n')
    logFile.write('*** Weld simulation job log           ****\n')
    logFile.write('******************************************\n')
    logFile.write(' \n')
    logFile.flush()
# +
def timeStamp(logFile):
    from sys import *
    import time
    logFile.write(' \n')
    logFile.write(' >>>>> ' + time.ctime(time.time()) + '\n')
    logFile.write(' \n')
# +
def writeModelInfo(logFile,name,timeRemaining,remeshNumber):
    from sys import *
    timeStamp(logFile)
    if remeshNumber > 0:
	logFile.write('Remesh ' + '%g' % remeshNumber + '\n')
    logFile.write('Running job ' + name + '\n')
    logFile.write('for an attempted duration of ' + '%g' % timeRemaining + '\n')
    logFile.flush()


def searchMsgFile(jobName,searchStr,beginLoc,endLoc):
    import os
    a = "0"
    b = "0"
    try:
        f = open(jobName+".msg","r")
    except:
        return 0
    for line in f.readlines():
        if searchStr in line:
          b = a
          a = line[beginLoc:endLoc]
    f.close()
    return float(b)
##
## Search msg file
## -
def searchMsgFileOld(jobName,searchStr,beginLoc,endLoc):
    import os
    a = "0"
    try:
        f = open(jobName+".msg","r")
    except:
        return 0
    for line in f.readlines():
        if searchStr in line:
          a = line[beginLoc:endLoc]
    f.close()
    return float(a)
##
## Search msg file and return string
## -
def searchMsgFileStr(jobName,searchStr,beginLoc,endLoc):
    import os
    a = "NO ERROR?"
    try:
        f = open(jobName+".msg","r")
    except:
        return "NO FILE?"
    for line in f.readlines():
        if searchStr in line:
          a = line[beginLoc:endLoc]
    f.close()
    return a
##
## Determine the elapsed time for a job
## +
def elapsedTime(jobName):
    return  searchMsgFile(jobName,"STEP TIME COM",22,36)
##
## Determine the elapsed time for a job
## -
def elapsedTimeOld(jobName):
    return  searchMsgFile(jobName,"STEP TIME COM",22,36)

##
## Determine the number of increments for a job
## + 
def numberOfIncrements(jobName):
    import os
    a = "0"
    try:
        f = open(jobName+".msg","r")
    except:
        return 0
    for line in f.readlines():
        if 'TOTAL OF' in line and 'INCREMENT' in line:
          a = line[15:25]
    f.close()
    return float(a)

##
## Determine the number of iterations for a job
## +
def numberOfIterations(jobName):
    import os
    a = '0'
    try:
        f = open(jobName+".msg","r")
    except:
        return 0
    for line in f.readlines():
        if 'PASSES' in line:
          a = line[15:25]
    f.close()
    print "Total number of iterations:", a
    return float(a)
# +
def writeAnalysisInfo(logFile,name,totalTime,timeRemaining,endReason):
    from sys import *
    timeStamp(logFile)
    logFile.write('Completed job ' + name + '\n')
    logFile.write('Because ' + endReason + '\n')
    logFile.write('\n')
    logFile.write('\n')
    elapsed = elapsedTime(name)
    increments = numberOfIncrements(name)
    iterations = numberOfIterations(name)
    logFile.write('simulation time elapsed           = ' + '%g' % elapsed + '\n')
    logFile.write('total simulation time elapsed     = ' + '%g' % totalTime + '\n')
    logFile.write('simulation time remaining         = ' + '%g' % timeRemaining + '\n')
    logFile.flush()
# +
def writeEnding(logFile):
    from sys import *
    logFile.write(' \n')
    logFile.write(' \n')
    logFile.write('******************************************\n')
    logFile.write('*** Weld simulation complete          ****\n')
    logFile.write('******************************************\n')
    logFile.flush()

#-----------------------------------------------------------------------------------------
##
## Determine the name of the new job
## +
def newJobName(referenceName,remeshNumber):

    return referenceName + "_remesh_" + '%i' % remeshNumber

	
##
## Determine the name of the prior-model ODB
## +
def priorJobName(referenceName,remeshNumber):
    ancestorResultsName = referenceName
    if remeshNumber > 1:
	priorRemesh = remeshNumber - 1
	ancestorResultsName = referenceName + "_remesh_" + '%i' % priorRemesh
    ancestorResultsName = ancestorResultsName
    return ancestorResultsName
    

#-----------------------------------------------------------------------------------------
##
## Replace the geometry for a part with a boundary based
## on the deformed configuration of the part instance in
## an earlier job
##

# +
def updateGeometry(partName,instanceName,odbFileName,featureAngle):
    from abaqus import *
    from part import *
    import abaqus
	
    
    model=mdb.models['Model-1']
    deformed = model.PartFromOdb(name='orphan',
                                 fileName=odbFileName,
                                 instance=instanceName,
                                 shape=DEFORMED,
                                 twist=ON)
    try:
	p1 = model.Part2DGeomFrom2DMesh(name=partName,
                                        part=deformed,
                                        featureAngle=featureAngle,
                                        twist=ON)
    
    except:
	#
	# Assume failure means the feature angle is too big
	# and results in an invalid part
	#
	print "Trying a feature angle of ",featureAngle/2
	try:
	    p1 = model.Part2DGeomFrom2DMesh(name=partName,
                                            part=deformed,
                                            featureAngle=featureAngle/2,
                                            twist=ON)
	except:
	    print "Trying a feature angle of ",featureAngle/4
	    try:
		p1 = model.Part2DGeomFrom2DMesh(name=partName,
                                                part=deformed,
                                                featureAngle=featureAngle/4,
                                                twist=ON)
	    except:
		print "Trying a feature angle of ",featureAngle/8
		try:
		    p1 = model.Part2DGeomFrom2DMesh(name=partName,
                                                    part=deformed,
                                                    featureAngle=featureAngle/8,
                                                    twist=ON)
		except:
		    print "Trying a feature angle of ",0
		    try:
			p1 = model.Part2DGeomFrom2DMesh(name=partName,
                                                        part=deformed,
                                                        featureAngle=0,
                                                        twist=ON)
		    except:
			pass

tolerance = 1.e-8

##
## Assign an edge set to the lowest (lowest y) edge on a
## part instance
## +
def lowestEdgeSet(a,instanceName,setName):
    from abaqus import *
    e = a.instances[instanceName].edges
    lowestLocation = 99999
    sideEdge = []
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if y < lowestLocation:
	    lowestLocation = y
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if abs(y-lowestLocation) < tolerance:
	    sideEdge.append(e[k:k+1])
    a.Set(edges=sideEdge, name=setName)

##
## Assign an edge set to any edge below coord on a
## part instance
## -
def belowCoordEdgeSet(a,instanceName,setName,coord):
    from abaqus import *
    e = a.instances[instanceName].edges
    sideEdge = []
    thisLocation = coord
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if y < (0.1+thisLocation):
	    sideEdge.append(e[k:k+1])
    a.Set(edges=sideEdge, name=setName)
    
    
##
## Assign an edge set to the highest (greatest y) edge on a
## part instance
## +
def highestEdgeSet(instanceName,setName):
    from abaqus import *
    from part import *
    import abaqus
    a = mdb.models['Model-1'].rootAssembly
    e = a.instances[instanceName].edges
    highestLocation = -99999
    sideEdge = []
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if y > highestLocation:
	    highestLocation = y
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if abs(y-highestLocation) < tolerance:
	    sideEdge.append(e[k:k+1])
    a.Set(edges=sideEdge, name=setName)

##
## Assign an edge set to the highest (greatest y) edge on a
## part instance
## -
def mostRightEdgeSet(instanceName,setName):
    from abaqus import *
    from part import *
    import abaqus
    a = mdb.models['Model-1'].rootAssembly
    e = a.instances[instanceName].edges
    rightLocation = -99999
    sideEdge = []
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if x > rightLocation:
	    rightLocation = x
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if abs(x-rightLocation) < tolerance:
	    sideEdge.append(e[k:k+1])
    a.Set(edges=sideEdge, name=setName)


##
## Assign an edge set to the lowest (lowest y) edge on a
## part instance
## -
def lowestVertexSet(instanceName,setName):
    from abaqus import *
    a =  mdb.models['Model-1'].rootAssembly
    v = a.instances[instanceName].vertices
    lowestLocation = 99999
    for k in range(len(v)):
#	print v[k].coordinates
	((x,y,z),) = v[k].pointOn
	if y < lowestLocation:
	    lowestLocation = y
    for k in range(len(v)):
	((x,y,z),) = v[k].pointOn
	if abs(y-lowestLocation) < tolerance:
	    lowVertex = []
	    lowVertex.append(v[k:k+1])
	    a.Set(vertices=lowVertex, name=setName)

##
## Assign an edge set to the lowest (lowest y) edge on a
## part instance
## -
def lowestNodeSet(instanceName,setName):
    from abaqus import *
    a =  mdb.models['Model-1'].rootAssembly
    n = a.instances[instanceName].nodes
    lowestLocation = 99999
    for k in range(len(n)):
#	print n[k].coordinates
	(x,y,z) = n[k].coordinates
	if y < lowestLocation:
	    lowestLocation = y
    for k in range(len(n)):
	(x,y,z) = n[k].coordinates
	if abs(y-lowestLocation) < tolerance:
	    lowNode = []
	    lowNode.append(n[k:k+1])
	    a.Set(nodes=lowNode, name=setName)


##
## Assign a set to the ref point on a
## part instance
## +
def refSet(instanceName,setName):
    from abaqus import *
    from part import *
    import abaqus
    a = mdb.models['Model-1'].rootAssembly
    r = a.instances[instanceName].referencePoints
    featureId = r.keys()[0]
    refPoint=(r[featureId], )
    a.Set(referencePoints=refPoint, name=setName)

##
## Assign a surface to the perimeter of a part instance
## +
def perimeterSurface(instanceName,surfaceName):
    from abaqus import *
    from part import *
    import abaqus
    a = mdb.models['Model-1'].rootAssembly
    e = a.instances[instanceName].edges
    sideEdges = e[0:len(e)]
    a.Surface(side1Edges=sideEdges, name=surfaceName)

##
## Assign a set to the perimeter of a part instance - not in use
## -
def perimeterSet(instanceName,setName):
    from abaqus import *
    from part import *
    import abaqus
    a = mdb.models['Model-1'].rootAssembly
    e = a.instances[instanceName].edges
    sideEdges = e[0:len(e)]
    a.Set(edges=sideEdges, name=setName)

##
## Assign a surface to the highest (greatest y) edge on a
## part instance
## +
def highestSurface(instanceName,surfaceName):
    from abaqus import *
    from part import *
    import abaqus
    a = mdb.models['Model-1'].rootAssembly
    e = a.instances[instanceName].edges
    highestLocation = -99999
    sideEdge = []
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if y > highestLocation:
	    highestLocation = y
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if abs(y-highestLocation) < tolerance:
	    sideEdge.append(e[k:k+1])
    a.Surface(side1Edges=sideEdge, name=surfaceName)

##
## Assign a surface to the lowest (smallest y) edge on a
## part instance
## -
def lowestSurface(instanceName,surfaceName):
    from abaqus import *
    from part import *
    import abaqus
    a = mdb.models['Model-1'].rootAssembly
    e = a.instances[instanceName].edges
    lowestLocation = 99999
    sideEdge = []
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if y < lowestLocation:
	    lowestLocation = y
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if abs(y-lowestLocation) < tolerance:
	    sideEdge.append(e[k:k+1])
    a.Surface(side1Edges=sideEdge, name=surfaceName)

##
## Assign a surface to the most right (greatest x) edge on a
## part instance
## -
def mostRightSurface(instanceName,surfaceName):
    from abaqus import *
    from part import *
    import abaqus
    a = mdb.models['Model-1'].rootAssembly
    e = a.instances[instanceName].edges
    rightLocation = -99999
    sideEdge = []
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if x > rightLocation:
	    rightLocation = x
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if abs(x-rightLocation) < tolerance:
	    sideEdge.append(e[k:k+1])
    a.Surface(side1Edges=sideEdge, name=surfaceName)

##
## Assign a surface to the highest (greatest y) edge on a
## part instance
## -
def leftCoordSurface(instanceName,surfaceName,coord):
    from abaqus import *
    from part import *
    import abaqus
    a = mdb.models['Model-1'].rootAssembly
    e = a.instances[instanceName].edges
    sideEdge = []
    thisLoacation = coord
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if x < thisLoacation+0.1:
	    sideEdge.append(e[k:k+1])
    a.Surface(side1Edges=sideEdge, name=surfaceName)

##
## Assign a surface to all instance edges except the lowest 
## (smallest y) and the highest edges 
## -
def midleSurface(instanceName,surfaceName,myOffset):
    from abaqus import *
    from part import *
    import abaqus
    a = mdb.models['Model-1'].rootAssembly
    e = a.instances[instanceName].edges
    lowestLocation = 99999
    highestLocation = -99999
    thisOffset = myOffset
    sideEdge = []
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if y > highestLocation:
	    highestLocation = y
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if y < lowestLocation:
	    lowestLocation = y
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if y > (lowestLocation + thisOffset):
	    if y < highestLocation - tolerance:
		    sideEdge.append(e[k:k+1])
    a.Surface(side1Edges=sideEdge, name=surfaceName)

#
# Add U displacement field without rotation angle to ODB
# with a new field name UNEW in ODB
# +
def add_unew_odb(odbName):

    from odbAccess import *
    import sys, numpy.oldnumeric as Numeric
    from textRepr import prettyPrint

	
    odb = openOdb(odbName + ".odb")
	
    for step in odb.steps.values():
        for frame in step.frames:
		    
            try:
                frame.FieldOutput(name='UNEW', field=frame.fieldOutputs['U'])
            except KeyError:
                pass
				
    
# Add Arc face partition based on sketch geometry points
# -
def arcFacePartition(instanceName, leftPoint, rightPoint, centerPoint):

    from abaqus import *
    from assembly import *
    from part import *

    s11 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
        sheetSize=200.0)
    g, v, d, c = s11.geometry, s11.vertices, s11.dimensions, s11.constraints
    s11.sketchOptions.setValues(viewStyle=AXISYM)
    s11.setPrimaryObject(option=STANDALONE)
    s11.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s11.FixedConstraint(entity=g[2])
    s11.Arc3Points(point1=leftPoint, point2=rightPoint, 
        point3=centerPoint)
    f11=mdb.models['Model-1'].rootAssembly.instances[instanceName].faces
    mdb.models['Model-1'].rootAssembly.PartitionFaceBySketch(faces=f11,
        sketch=s11)

#
#

##
## Clean up file
## -
def cleanupFile(logFile,referenceName,remeshNumber):
	import osutils
	jobName = referenceName + "_remesh_" + '%i' % remeshNumber
        logFile.write('Remove files of ' +jobName + '\n')
	try:
	    osutils.remove(jobName + ".stt")
	except:
	    pass
	try:
	    osutils.remove(jobName + ".mdl")
	except:
	    pass
	try:
	    osutils.remove(jobName + ".size")
	except:
	    pass
	try:
	    osutils.remove(jobName + ".ipm")
	except:
	    pass
	try:
	    osutils.remove(jobName + ".stt")
	except:
	    pass
	try:
	    osutils.remove(jobName + ".res")
	except:
	    pass
	try:
	    osutils.remove(jobName + ".dat")
	except:
	    pass
	try:
	    osutils.remove(jobName + ".prt")
	except:
	    pass
	try:
	    osutils.remove(jobName + ".msg")
	except:
	    pass
	try:
	    osutils.remove(jobName + ".jnl")
	except:
	    pass
	try:
	    osutils.remove(jobName + ".lck")
	except:
	    pass
		
		
		
#-------------Debuggers meu
def WriteMeioCaminho(logFile,OndeEstou):
	from sys import *
	
	logFile.write('\n' + 'passei por:' + OndeEstou)
	logFile.flush()
	
##
## Escreve no logFile pra dizer aonde esta

def writeStuff(remesh,what):
	from abaqus import *
	import abaqus
	import sys
	import os
	
	# Read Info
	arqTxt=open('txtTeste.txt', 'r')
	tAntigo = arqTxt.read()
	arqTxt.close()
	# Write info
	arqTxt=open('txtTeste.txt', 'w')
	arqTxt.write(tAntigo + '\n' + 'Remesh ' + '%s - %s' % (remesh,what))
	arqTxt.close()
	

	
	
