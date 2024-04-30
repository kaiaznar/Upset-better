#geometry - base CAE Module Creation/Simulation Run

from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
#from diskweld_utils import *

#execfile('diskweld_utils.py')

#GEOMETRY

iOffSet=5.0 #lembrar de arrumar subrotina!
jOffSet=50.0
iesp=-0.25

s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.sketchOptions.setValues(viewStyle=AXISYM)
s.setPrimaryObject(option=STANDALONE)
s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
s.FixedConstraint(entity=g[2])
#-------------Upset ---------------------------------------------------
s.Line(point1=(50.81,90.0), point2=(50.81,160.0))
s.Line(point1=(50.81,160.0), point2=(63.5,160.0))
s.Line(point1=(63.5,160.0), point2=(59.83,90.0))
s.Line(point1=(59.83,90.0), point2=(50.81,90.0))
#-----------------------------------------------------------------------------
p = mdb.models['Model-1'].Part(name='Upset_weld',
    dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY, twist=ON)
p = mdb.models['Model-1'].parts['Upset_weld']
p.BaseShell(sketch=s)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Upset_weld']
#p.ReferencePoint(point=(0.0, 29.39, 0.0))
p.ReferencePoint(point=(0.0, 30.0, 0.0))
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
    sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.sketchOptions.setValues(viewStyle=AXISYM)
s1.setPrimaryObject(option=STANDALONE)
s1.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
s1.FixedConstraint(entity=g[2])
#-------------Glove e pipe---------------------------------------------------------
s1.Line(point1=(42.8,-30.0), point2=(42.8,100.0))
s1.Line(point1=(42.8,100.0), point2=(50.8,100.0))
s1.Line(point1=(50.8,100.0), point2=(50.8,30.0))
s1.Line(point1=(50.8,30.0), point2=(60.1, 30.0))
s1.Line(point1=(60.1,30.0), point2=(63.5,100.0))
s1.Line(point1=(63.5,100.0), point2=(68.5,100.0))
s1.Line(point1=(68.5,100.0), point2=(68.5,20.0))
s1.Line(point1=(68.5,20.0), point2=(55.3,20.0))
s1.Arc3Points(point1=(55.3,20.0), point2=(50.8,15.5), 
    point3=(53.98,16.82))
s1.Line(point1=(50.8,15.5), point2=(50.8,-30.0))
s1.Line(point1=(50.8,-30.0), point2=(42.8,-30.0))
#---------------------------------------------------------------------------------
p = mdb.models['Model-1'].Part(name='Glovepipe_weld',
    dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY, twist=ON)
p = mdb.models['Model-1'].parts['Glovepipe_weld']
p.BaseShell(sketch=s1)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Glovepipe_weld']
p.ReferencePoint(point=(0.0, 6.35, 0.0))
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']