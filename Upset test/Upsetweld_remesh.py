# create remeshed model and restart input file


from UpsetWeld_utils import *

Mdb()


#ancestorJobName = primaryJobName
openMdb(primaryJobName + '.cae')
mdb.saveAs(remeshJobName + '.cae')
openMdb(remeshJobName + '.cae')

model=mdb.models['Model-1']
a = model.rootAssembly
try:
    a.deleteFeatures(('Datum plane-4', 'Partition face-4', ))
    a.deleteFeatures(('Datum plane-3', 'Partition face-3', ))
    a.deleteFeatures(('Datum plane-2', 'Partition face-2', ))
    a.deleteFeatures(('Datum plane-1', 'Partition face-1', ))
except:
    pass
a.regenerate()

# Replace the pipes with the deformed configuration outlines
#input
remeshFeatureAngle = 6.0

updateGeometry('Glovepipe_weld','GLOVEPIPE_WELD-1',ancestorJobName + '.odb',remeshFeatureAngle)
updateGeometry('Upset_weld',   'UPSET_WELD-1',   ancestorJobName + '.odb',remeshFeatureAngle)
p = model.parts['Glovepipe_weld']
p.ReferencePoint(point=(0.0, 6.35, 0.0))
p = model.parts['Upset_weld']
p.ReferencePoint(point=(0.0, 29.39, 0.0))

from part import *
from assembly import *
a = model.rootAssembly
a.backup()
a.regenerate()


# Re-establish attributes


# ------------------materials

from caeModules import *
p = model.parts['Glovepipe_weld']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
region = regionToolset.Region(faces=faces)
p = model.parts['Glovepipe_weld']
p.SectionAssignment(region=region, sectionName='pipe material', offset=0.0)
p = model.parts['Upset_weld']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = model.parts['Upset_weld']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
region = regionToolset.Region(faces=faces)
p = model.parts['Upset_weld']
p.SectionAssignment(region=region, sectionName='pipe material', offset=0.0)

# -------------------sets
from assembly import *
belowCoordEdgeSet(model.rootAssembly,'Glovepipe_weld-1','bottomAttachment',0.0)
highestEdgeSet('Upset_weld-1','topAttachment')
mostRightEdgeSet('Glovepipe_weld-1','rightAttachment')
refSet('Upset_weld-1','topFlywheelAttachment')
refSet('Glovepipe_weld-1','bottomFlywheelAttachment')

a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Glovepipe_weld-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
a.Set(faces=faces1, name='bottomFullFace')

a = mdb.models['Model-1'].rootAssembly
f2 = a.instances['Upset_weld-1'].faces
faces2 = f2.getSequenceFromMask(mask=('[#1 ]', ), )
a.Set(faces=faces2, name='topFullFace')

# ---------------surfaces
highestSurface('Upset_weld-1','topPipeHighestSurface')
lowestSurface('Glovepipe_weld-1','bottomPipeLowestSurface')
mostRightSurface('Glovepipe_weld-1','bottomPipeMostRightSurface')

perimeterSurface('Upset_weld-1','topWeldSurface')
perimeterSurface('Glovepipe_weld-1','bottomWeldSurface')


# ---------------Redefine the step

from step import *
model.steps['Weld step'].setValues( 
    description='Weld step', timePeriod=weldStepTime,
    maxInc=outputFrequency, initialInc=firstInc, minInc=1e-12)
try:
    del model.predefinedFields['Predefined Field-1']
except:
    pass


# --------------Get Parameter state variables
try:
    searchedForce=searchMsgFile(ancestorJobName, "force= ",10,34)
except:
    searchedForce = 0
if searchedForce != 0:
    lastForce = searchedForce

try:
    searchedUpset=searchMsgFile(ancestorJobName, "upset= ",10,34)
except:
    searchedUpset = 0
if searchedUpset != 0:
    lastUpset = searchedUpset
writeStuff(remeshJobName,lastUpset)

    


try:
    searchedSpinR=searchMsgFile(ancestorJobName, "spinR= ",10,34)
except:
    searchedSpinR = 0
lastSpinR = searchedSpinR



# --------------Redefine BCs
if lastUpset > dispChange:
	mdb.models['Model-1'].boundaryConditions['Goupglove'].suppres()
	mdb.models['Model-1'].loads['ForcUpUpset'].resume()
	
# Reset values of velocito to aproach parts
#velEncontro=upperCutPosition-
resetDownVelocity=mdb.models['Model-1'].boundaryConditions['SpeeedUpGlove']
resetDownVelocity.setValues(v1=0., v2=100.0e09, v3=0., vr1=0., vr2=0., vr3=0.)	
resetUpVelocity= mdb.models['Model-1'].boundaryConditions['SpeeedDownGlove']
resetUpVelocity.setValues(v1=0., v2=-(100.0e09), v3=0., vr1=0., vr2=0., vr3=0.)

#--------------- Remesh

# Apply partitions
#input
#nearWeldZone 
#
# Find the lowest point on the top pipe
e = a.instances['Upset_weld-1'].edges
v = a.instances['Upset_weld-1'].vertices
upperCutPosition = 0
lowestLocation = 99999
for k in range(len(v)):
    ((x,y,z),) = v[k].pointOn
    if y < lowestLocation:
	lowestLocation = y
upperCutPosition = nearWeldZone+lowestLocation
upperCutPosition = sliceTopInstance('Upset_weld-1',upperCutPosition, nearWeldMeshSize)



sliceVerticalInstance('Glovepipe_weld-1',rightCutPosition)

#--------mesh seeds
removeEdgeSeeds('Upset_weld-1')
removeEdgeSeeds('Glovepipe_weld-1')
seedNearZeroTop('Upset_weld-1',nearWeldMeshSize,upperCutPosition +0.001)
seedNearZeroLeftTo('Glovepipe_weld-1',nearWeldMeshSize,rightCutPosition+0.001)



a = model.rootAssembly
f1 = a.instances['Upset_weld-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
f2 = a.instances['Glovepipe_weld-1'].faces
faces2 = f2.getSequenceFromMask(mask=('[#1 ]', ), )
pickedRegions = faces1+faces2
#a.setMeshControls(regions=pickedRegions, elemShape=QUAD_DOMINATED, technique=FREE, 
#    allowMapped=True)
a.setMeshControls(regions=pickedRegions, elemShape=QUAD_DOMINATED, technique=FREE, 
    allowMapped=True)
partInstances =(a.instances['Upset_weld-1'], 
    a.instances['Glovepipe_weld-1'], )
a.generateMesh(regions=partInstances)

mdb.models['Model-1'].interactionProperties['weld contact'].TangentialBehavior(
    formulation=USER_DEFINED, nStateDependentVars=0, useProperties=ON, table=((
    totalTime, ), ))

#---------Node reSet
#lowestNodeSet('Upset_weld-1','lowestNode')

#
forceFlux=searchMsgFileOld(ancestorJobName, "TIME AVG. FORCE",70,80)
momentFlux=searchMsgFileOld(ancestorJobName, "TIME AVG. MOMENT",70,80)
heatFlux=searchMsgFileOld(ancestorJobName, "TIME AVG. HEAT FLUX",70,80)




##
## Add additional keywords
##

import job
from job import *
model.keywordBlock.synchVersions()
model.keywordBlock.setValues(edited = 0)
model.keywordBlock.synchVersions()

modelBlock = whereIsThirdLastBlock("*Step") - 1
model.keywordBlock.insert(modelBlock, """*map solution""")
#model.keywordBlock.insert(modelBlock, """*map solution, UNBALANCED STRESS=STEP""")

amplitudeBlockPos = whereIsLastBlock('*Amplitude, name=ROT_AMP, definition=USER, variables=4')
newAmplitudeBlock = '*Amplitude, name=ROT_AMP, definition=USER, variables=4, properties=4'
propAmplitudeStr = '%s' % (totalTime) + "," + '%s' % (lastForce)+ "," + '%s' % (lastUpset)+ "," + '%s' % (lastSpinR)
mdb.models['Model-1'].keywordBlock.replace(amplitudeBlockPos, newAmplitudeBlock)
mdb.models['Model-1'].keywordBlock.insert(amplitudeBlockPos, propAmplitudeStr)

contactBlockPos = whereIsLastBlock('*Contact Pair, interaction="weld contact", type=SURFACE TO SURFACE')
newContactBlock = '*Contact Pair, interaction="weld contact", type=SURFACE TO SURFACE, SLIDING TRANSITION=QUADRATIC'
nxtContactBlock = 'topWeldSurface, bottomWeldSurface'
mdb.models['Model-1'].keywordBlock.replace(contactBlockPos, newContactBlock)
mdb.models['Model-1'].keywordBlock.insert(contactBlockPos, nxtContactBlock)

historyBlock = whereIsSecondLastBlock("*End Step") - 1
model.keywordBlock.insert(historyBlock, """*controls,analysis=discontinuous""")


mdb.models['Model-1'].setValues(noPartsInputFile=OFF)
mdb.jobs.changeKey(fromName=primaryJobName, toName=remeshJobName)
mdb.jobs[remeshJobName].writeInput()
mdb.save()

