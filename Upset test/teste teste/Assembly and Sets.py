#ASSEMBLY
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
from UpsetWeld_utils import *

execfile('UpsetWeld_utils.py')

a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByThreePoints(coordSysType=CYLINDRICAL, origin=(0.0, 0.0, 0.0),
    point1=(1.0, 0.0, 0.0), point2=(0.0, 0.0, -1.0))
p = mdb.models['Model-1'].parts['Glovepipe_weld']
a.Instance(name='Glovepipe_weld-1', part=p, dependent=OFF)
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Upset_weld']
a.Instance(name='Upset_weld-1', part=p, dependent=OFF)

#SETS
a = mdb.models['Model-1'].rootAssembly
r1 = a.instances['Upset_weld-1'].referencePoints
refPoints1=(r1[2], )
a.Set(referencePoints=refPoints1, name='topFlywheelAttachment')

a = mdb.models['Model-1'].rootAssembly
r1 = a.instances['Glovepipe_weld-1'].referencePoints
refPoints1=(r1[2], )
a.Set(referencePoints=refPoints1, name='bottomFlywheelAttachment')

a = mdb.models['Model-1'].rootAssembly
belowCoordEdgeSet(a,'Glovepipe_weld-1','bottomAttachment',0.0)
highestEdgeSet('Upset_weld-1','topAttachment')
mostRightEdgeSet('Upset_weld-1','rightAttachment')


a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Glovepipe_weld-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
a.Set(faces=faces1, name='bottomFullFace')

a = mdb.models['Model-1'].rootAssembly
f2 = a.instances['Upset_weld-1'].faces
faces2 = f2.getSequenceFromMask(mask=('[#1 ]', ), )
a.Set(faces=faces2, name='topFullFace')


#SURFACES

perimeterSurface('Upset_weld-1','topWeldSurface')
perimeterSurface('Glovepipe_weld-1','bottomWeldSurface')