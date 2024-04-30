
#Upsetweld - Base CAE Module Creation/Simulation Run

from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
from UpsetWeld_utils import *


execfile('UpsetWeld_utils.py')

#-------------------------------------GEOMETRY

iOffSet=5.0 #lembrar de arrumar subrotina!
jOffSet=50.0	
iesp=-0.25

#Upset 
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.sketchOptions.setValues(viewStyle=AXISYM)
s.setPrimaryObject(option=STANDALONE)
s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
s.FixedConstraint(entity=g[2])

s.Line(point1=(50.81,35.), point2=(50.81,105.0))
s.Line(point1=(50.81,105.0), point2=(63.5,105.0))
s.Line(point1=(63.5,105.0), point2=(59.83,35.0))
s.Line(point1=(59.83,35.0), point2=(50.81,35.0))
#-----------------------------------------------------------------------------
p = mdb.models['Model-1'].Part(name='Upset_weld',
    dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY, twist=ON)
p = mdb.models['Model-1'].parts['Upset_weld']
p.BaseShell(sketch=s)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Upset_weld']
p.ReferencePoint(point=(0.0, 30.0, 0.0))
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']

#Glove e pipe
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
    sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.sketchOptions.setValues(viewStyle=AXISYM)
s1.setPrimaryObject(option=STANDALONE)
s1.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
s1.FixedConstraint(entity=g[2])

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


#-------------------MATERIAL 
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON,
    engineeringFeatures=ON)
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((1.0, 0.2), ))
mdb.models['Model-1'].Material('astroloy')
mdb.models['Model-1'].materials['astroloy'].Density(table=((7.8e-06, ), ))
mdb.models['Model-1'].materials['astroloy'].Conductivity(
    temperatureDependency=ON, table=((0.014854, 20), (0.01587, 100), (0.01714, 200), 
    (0.01841, 300), (0.01968, 400), (0.02095, 500), (0.02222, 600), (0.02349, 700), 
    (0.02476, 800), (0.02603, 900), (0.0273, 1000), (0.02857, 1100), (0.02984, 1200)))
mdb.models['Model-1'].materials['astroloy'].SpecificHeat(law=CONSTANTPRESSURE, 
    temperatureDependency=ON, table=((455.484672, 20), (475.224, 100), (495.432, 200), 
    (511.428, 300), (524.016, 400), (534, 500), (542.184, 600), (549.372, 700), 
    (556.368, 800), (563.976, 900), (573, 1000), (584.244, 1100), (598.512, 1200)))
mdb.models['Model-1'].materials['astroloy'].Expansion(table=((0.0, ), ))
#---------------Elastic 190GPa------------------------------------------------
mdb.models['Model-1'].materials['astroloy'].Elastic(
    temperatureDependency=ON, table=((190000, 0.3, 20), (182400, 0.3, 100), 
    (174800, 0.3, 200), (167200, 0.3, 300), (159600, 0.3, 400), (152000, 0.3, 500), 
    (144400, 0.3, 600), (134900, 0.3, 700), (119700, 0.3, 800), (85500, 0.3, 900), 
    (38000, 0.3, 1000), (19000, 0.3, 1100)))
#-----------SAF 2205 UNS 31803 EN 1.4462- LINEAR + rate v1.7------------------------------------
mdb.models['Model-1'].materials['astroloy'].Plastic(temperatureDependency=ON, rate=ON, 
    table=((600.01,0.0,0.0,20),(597.18,0.0,0.0,25),(583.02,0.0,0.0,50),(568.86,0.0,0.0,75),
    (554.7,0.0,0.0,100),(540.54,0.0,0.0,125),(526.39,0.0,0.0,150),(512.23,0.0,0.0,175),
    (498.07,0.0,0.0,200),(483.91,0.0,0.0,225),(469.75,0.0,0.0,250),(455.59,0.0,0.0,275),
    (441.44,0.0,0.0,300),(427.28,0.0,0.0,325),(413.12,0.0,0.0,350),(398.96,0.0,0.0,375),
    (384.8,0.0,0.0,400),(370.65,0.0,0.0,425),(356.49,0.0,0.0,450),(342.33,0.0,0.0,475),
    (328.17,0.0,0.0,500),(314.01,0.0,0.0,525),(299.85,0.0,0.0,550),(285.7,0.0,0.0,575),
    (271.54,0.0,0.0,600),(257.38,0.0,0.0,625),(243.22,0.0,0.0,650),(229.06,0.0,0.0,675),
    (214.91,0.0,0.0,700),(200.75,0.0,0.0,725),(186.59,0.0,0.0,750),(172.43,0.0,0.0,775),
    (158.27,0.0,0.0,800),(144.11,0.0,0.0,825),(129.96,0.0,0.0,850),(115.8,0.0,0.0,875),
    (101.64,0.0,0.0,900),(87.48,0.0,0.0,925),(73.32,0.0,0.0,950),(59.17,0.0,0.0,975),
    (45.01,0.0,0.0,1000),(41.25,0.0,0.0,1025),(37.5,0.0,0.0,1050),(33.75,0.0,0.0,1075),
    (30,0.0,0.0,1100),(26.25,0.0,0.0,1125),(22.5,0.0,0.0,1150),(18.75,0.0,0.0,1175),
    (15,0.0,0.0,1200),(11.25,0.0,0.0,1225),(7.5,0.0,0.0,1250),(3.74,0.0,0.0,1275),
    (600.01,0.0,0.1,20),(597.18,0.0,0.1,25),(583.02,0.0,0.1,50),(568.86,0.0,0.1,75),
    (554.7,0.0,0.1,100),(540.54,0.0,0.1,125),(526.39,0.0,0.1,150),(512.23,0.0,0.1,175),
    (498.07,0.0,0.1,200),(483.91,0.0,0.1,225),(469.75,0.0,0.1,250),(455.59,0.0,0.1,275),
    (441.44,0.0,0.1,300),(427.28,0.0,0.1,325),(413.12,0.0,0.1,350),(398.96,0.0,0.1,375),
    (384.8,0.0,0.1,400),(370.65,0.0,0.1,425),(356.49,0.0,0.1,450),(342.33,0.0,0.1,475),
    (328.17,0.0,0.1,500),(314.01,0.0,0.1,525),(299.85,0.0,0.1,550),(285.7,0.0,0.1,575),
    (271.54,0.0,0.1,600),(257.38,0.0,0.1,625),(243.22,0.0,0.1,650),(229.06,0.0,0.1,675),
    (214.91,0.0,0.1,700),(200.75,0.0,0.1,725),(186.59,0.0,0.1,750),(172.43,0.0,0.1,775),
    (158.27,0.0,0.1,800),(144.11,0.0,0.1,825),(129.96,0.0,0.1,850),(115.8,0.0,0.1,875),
    (101.64,0.0,0.1,900),(87.48,0.0,0.1,925),(73.32,0.0,0.1,950),(59.17,0.0,0.1,975),
    (45.01,0.0,0.1,1000),(41.25,0.0,0.1,1025),(37.5,0.0,0.1,1050),(33.75,0.0,0.1,1075),
    (30,0.0,0.1,1100),(26.25,0.0,0.1,1125),(22.5,0.0,0.1,1150),(18.75,0.0,0.1,1175),
    (15,0.0,0.1,1200),(11.25,0.0,0.1,1225),(7.5,0.0,0.1,1250),(3.74,0.0,0.1,1275),
    (1e5, 0.0, 200, 20), (1e5, 0.0, 200, 1200),
    (1e8, 0.0, 1000, 20), (1e8, 0.0, 1000, 1200)))

mdb.models['Model-1'].HomogeneousSolidSection(name='pipe material',
    material='astroloy', thickness=1.0)

p = mdb.models['Model-1'].parts['Glovepipe_weld']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
region = regionToolset.Region(faces=faces)
p = mdb.models['Model-1'].parts['Glovepipe_weld']
p.SectionAssignment(region=region, sectionName='pipe material', offset=0.0)
p = mdb.models['Model-1'].parts['Upset_weld']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Upset_weld']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
region = regionToolset.Region(faces=faces)
p = mdb.models['Model-1'].parts['Upset_weld']
p.SectionAssignment(region=region, sectionName='pipe material', offset=0.0)


#---------------ASSEMBLY
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

#----------------#SETS
#refPoints

a = mdb.models['Model-1'].rootAssembly
r1 = a.instances['Upset_weld-1'].referencePoints
refPoints1=(r1[2], )
a.Set(referencePoints=refPoints1, name='topFlywheelAttachment')

a = mdb.models['Model-1'].rootAssembly
r1 = a.instances['Glovepipe_weld-1'].referencePoints
refPoints1=(r1[2], )
a.Set(referencePoints=refPoints1, name='bottomFlywheelAttachment')

#edges +-

a = mdb.models['Model-1'].rootAssembly
belowCoordEdgeSet(a,'Glovepipe_weld-1','bottomAttachment',0.0)
highestEdgeSet('Upset_weld-1','topAttachment')
mostRightEdgeSet('Glovepipe_weld-1','rightAttachment')

#faces -

a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Glovepipe_weld-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
a.Set(faces=faces1, name='bottomFullFace')

a = mdb.models['Model-1'].rootAssembly
f2 = a.instances['Upset_weld-1'].faces
faces2 = f2.getSequenceFromMask(mask=('[#1 ]', ), )
a.Set(faces=faces2, name='topFullFace')


#------------SURFACES -

perimeterSurface('Upset_weld-1','topWeldSurface')
perimeterSurface('Glovepipe_weld-1','bottomWeldSurface')


#-------------STEP
#input

simulationTime = 150.0
totalTime = 0.0
timeRemaining = simulationTime - totalTime
weldStepTimeA = 0.5
weldStepTime = weldStepTimeA
outputFrequency = weldStepTime/5
firstIncA = 0.0001
firstInc = firstIncA

initialTemperature = 25.0
#+-
mdb.models['Model-1'].CoupledTempDisplacementStep(name='Step-1',
    previous='Initial', description="Step-1", response=TRANSIENT,
    creepIntegration=CREEP_OFF, timePeriod=1.e-09, maxNumInc=500, 
    timeIncrementationMethod=AUTOMATIC, initialInc=1e-09, minInc=1e-12, maxInc=1e-09,
    deltmx=300, cetol=None, amplitude=STEP, 
    extrapolation=PARABOLIC, 
    matrixStorage=UNSYMMETRIC,nlgeom=ON)
#-
mdb.models['Model-1'].CoupledTempDisplacementStep(name='Weld step',
    previous='Step-1', description="Weld step", response=TRANSIENT,
    creepIntegration=CREEP_OFF, timePeriod=weldStepTime, maxNumInc=500, 
    timeIncrementationMethod=AUTOMATIC, initialInc=firstInc, minInc=1e-12, maxInc=outputFrequency,
    deltmx=300, cetol=None, amplitude=STEP, 
    extrapolation=PARABOLIC, 
    matrixStorage=UNSYMMETRIC,nlgeom=ON)
#-
mdb.models['Model-1'].CoupledTempDisplacementStep(name='Step-3',
    previous='Weld step', description="Step-3", response=TRANSIENT,
    creepIntegration=CREEP_OFF, timePeriod=1e-09, maxNumInc=500, 
    timeIncrementationMethod=AUTOMATIC, initialInc=1e-09, minInc=1e-12, maxInc=1e-09,
    deltmx=300, cetol=None, amplitude=STEP, 
    extrapolation=PARABOLIC,
    matrixStorage=UNSYMMETRIC,nlgeom=ON)

mdb.models['Model-1'].steps['Step-3'].Restart(frequency=1,
    numberIntervals=0, overlay=ON, timeMarks=OFF)
mdb.models['Model-1'].FieldOutputRequest(name='F-Output-1',
    createStepName='Step-1', variables=('S', 'U', 'NT', 'PEEQ', 'HFL', 'COORD', 'CSTATUS', 
    'CSTRESS'))
mdb.models['Model-1'].HistoryOutputRequest(name='H-Output-1',
    createStepName='Step-1', variables=('ALLWK', 'ALLKE' ))
regionDef=mdb.models['Model-1'].rootAssembly.sets['topFlywheelAttachment']
mdb.models['Model-1'].HistoryOutputRequest(name='UPSET',
    createStepName='Step-1', variables=('U2', ), region=regionDef,
    sectionPoints=DEFAULT, rebar=EXCLUDE, sensor=ON)
	#-
mdb.models['Model-1'].HistoryOutputRequest(name='FORCE',
    createStepName='Step-1', variables=('TF2', ), region=regionDef,
    sectionPoints=DEFAULT, rebar=EXCLUDE, sensor=ON)
mdb.models['Model-1'].HistoryOutputRequest(name='TORQUE',
    createStepName='Step-1', variables=('TM2', ), region=regionDef,
    sectionPoints=DEFAULT, rebar=EXCLUDE)

#-------------------------INTERACTIONS
#input
weldContactDistance = -0.005
weldContactPressure = 300.0

selfContactDistance = 0.03
selfContactPressure = 20000.
contactOffset = 1.0

# interaction properties
#WELD CONTACT
mdb.models['Model-1'].ContactProperty('weld contact')
mdb.models['Model-1'].interactionProperties['weld contact'].NormalBehavior(
    pressureOverclosure=TABULAR, table=(
    (0.0,weldContactDistance*2), (weldContactPressure/100, weldContactDistance), (weldContactPressure,0.0)),
    constraintEnforcementMethod=DEFAULT)
#+-
mdb.models['Model-1'].interactionProperties['weld contact'].TangentialBehavior(
    formulation=USER_DEFINED, nStateDependentVars=0, useProperties=ON, table=((
    0., ), ))
#-
mdb.models['Model-1'].interactionProperties['weld contact'].HeatGeneration(
    conversionFraction=0.001, slaveFraction=0.5)
#-
mdb.models['Model-1'].interactionProperties['weld contact'].ThermalConductance(
    clearanceDepTable=((1.0, 0.0), (0.0, 0.21)))

# sELF CONTACT
mdb.models['Model-1'].ContactProperty('self contact')
mdb.models['Model-1'].interactionProperties['self contact'].NormalBehavior(
    pressureOverclosure=TABULAR, table=((0.0, -0.4), (15000, -0.3), (20000, 0.0)), 
    constraintEnforcementMethod=DEFAULT)
#-
mdb.models['Model-1'].interactionProperties['self contact'].ThermalConductance(
    clearanceDepTable=((1.0, 0.0), (0.0, 0.21)))

#contact interaction
a4 = mdb.models['Model-1'].rootAssembly
region1=a4.surfaces['bottomWeldSurface']
a4 = mdb.models['Model-1'].rootAssembly
region2=a4.surfaces['topWeldSurface']
#+-
mdb.models['Model-1'].SurfaceToSurfaceContactStd(name='weld contact 1',
    createStepName='Step-1', master=region1, slave=region2,
    sliding=FINITE,
    enforcement=SURFACE_TO_SURFACE,
    interactionProperty='weld contact', adjustMethod=TOLERANCE, 
    adjustTolerance=0.1, surfaceSmoothing=AUTOMATIC, 
    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
mdb.models['Model-1'].interactions['weld contact 1'].deactivate(stepName='Step-3')
#+
a5 = mdb.models['Model-1'].rootAssembly
region=a5.surfaces['bottomWeldSurface']
mdb.models['Model-1'].SelfContactStd(name='Bottom self contact', createStepName='Initial',
    enforcement=NODE_TO_SURFACE,
    surface=region, interactionProperty='self contact', smooth=0.2)
#+
region=a5.surfaces['topWeldSurface']
mdb.models['Model-1'].SelfContactStd(name='Top self contact', createStepName='Initial',
    enforcement=NODE_TO_SURFACE,
    surface=region, interactionProperty='self contact', smooth=0.2)

#constraints
#+
mdb.models['Model-1'].Equation(name='topFlywheelAttachment', terms=((1.0,
    'topAttachment', 5), (-1.0, 'topFlywheelAttachment', 5)))
mdb.models['Model-1'].Equation(name='topFlywheelAttachment2', terms=((1.0,
    'topAttachment', 2), (-1.0, 'topFlywheelAttachment', 2)))
mdb.models['Model-1'].Equation(name='bottomFlywheelAttachment5', terms=((1.0,
    'bottomAttachment', 5), (-1.0, 'bottomFlywheelAttachment', 5)))
mdb.models['Model-1'].Equation(name='bottomFlywheelAttachment2', terms=((1.0,
    'bottomAttachment', 2), (-1.0, 'bottomFlywheelAttachment', 2)))

#-	
#film condition
#input
convectionCoeff=0.001
conductionCoeff=1.0e-4

highestSurface('Upset_weld-1','topPipeHighestSurface')
lowestSurface('Glovepipe_weld-1','bottomPipeLowestSurface')
mostRightSurface('Glovepipe_weld-1','bottomPipeMostRightSurface')

a5 = mdb.models['Model-1'].rootAssembly
region=a5.surfaces['bottomPipeMostRightSurface']
mdb.models['Model-1'].FilmCondition(name='Bottom conduction', 
    createStepName='Weld step', surface=region, 
    definition=EMBEDDED_COEFF, sinkTemperature=initialTemperature,
    filmCoeff=conductionCoeff)
mdb.models['Model-1'].interactions['Bottom conduction'].deactivate(stepName='Step-3')
region=a5.surfaces['topPipeHighestSurface']
mdb.models['Model-1'].FilmCondition(name='Top conduction', 
    createStepName='Weld step', surface=region, 
    definition=EMBEDDED_COEFF, sinkTemperature=initialTemperature,
    filmCoeff=conductionCoeff)
mdb.models['Model-1'].interactions['Top conduction'].deactivate(stepName='Step-3')



#-------------------------BOUNDARY CONDITIONS
#input
appliedPressure = 360.0
flywheelStartVelocity = 52.36
#-
#amplitude
mdb.models['Model-1'].UserAmplitude(name='DISP_AMP', numVariables=4)
mdb.models['Model-1'].UserAmplitude(name='ROT_AMP', numVariables=4)
mdb.models['Model-1'].UserAmplitude(name='FORCE_AMP', numVariables=4)
#-
#BCs
a6 = mdb.models['Model-1'].rootAssembly
region = a6.sets['topFlywheelAttachment']
mdb.models['Model-1'].DisplacementBC(name='NoSpeedUpset', createStepName='Initial',
    region=region, u2=0, ur3=0)
#mdb.models['Model-1'].boundaryConditions['NoSpeedUpset'].deactivate('Weld step')

a6 = mdb.models['Model-1'].rootAssembly
region = a6.sets['bottomFlywheelAttachment']
mdb.models['Model-1'].DisplacementBC(name='NoSpeedGlove', createStepName='Initial',
    region=region, ur2=0)

a6 = mdb.models['Model-1'].rootAssembly
region = a6.sets['bottomFullFace']
mdb.models['Model-1'].VelocityBC(name='SpeeedUpGlove', createStepName='Step-1',
    region=region, v1=0., v2=5.05e09, v3=0., vr1=0., vr2=0., vr3=0.)
mdb.models['Model-1'].boundaryConditions['SpeeedUpGlove'].deactivate('Weld step')

a6 = mdb.models['Model-1'].rootAssembly
region = a6.sets['topFullFace']
mdb.models['Model-1'].VelocityBC(name='StopUpset', createStepName='Step-1',
    region=region, v1=0., v2=0, v3=0., vr1=0., vr2=0., vr3=0.)
mdb.models['Model-1'].boundaryConditions['StopUpset'].deactivate('Weld step')

a6 = mdb.models['Model-1'].rootAssembly
region = a6.sets['topFlywheelAttachment']
mdb.models['Model-1'].VelocityBC(name='VelAngUpset', createStepName='Weld step',
    region=region, vr2=-1., amplitude='ROT_AMP')
mdb.models['Model-1'].boundaryConditions['VelAngUpset'].deactivate('Step-3')

a6 = mdb.models['Model-1'].rootAssembly
region = a6.sets['rightAttachment']
mdb.models['Model-1'].DisplacementBC(name='NoMovRightEdge', createStepName='Weld step',
    region=region, u1=0)
mdb.models['Model-1'].boundaryConditions['NoMovRightEdge'].deactivate('Step-3')

a6 = mdb.models['Model-1'].rootAssembly
region = a6.sets['topFullFace']
mdb.models['Model-1'].VelocityBC(name='NoMovUpset', createStepName='Step-3',
    region=region, v1=0., v2=0., v3=0., vr1=0., vr2=0., vr3=0., amplitude='ROT_AMP')

a6 = mdb.models['Model-1'].rootAssembly
region = a6.sets['bottomFullFace']
mdb.models['Model-1'].VelocityBC(name='SpeeedDownGlove', createStepName='Step-3',
    region=region, v1=0., v2=-100.0e09, v3=0., vr1=0., vr2=0., vr3=0.)

#Load Parameters
dispChange=1.0

a6 = mdb.models['Model-1'].rootAssembly
region = a6.sets['bottomFlywheelAttachment']
mdb.models['Model-1'].ConcentratedForce(name='ForcUpUpset', createStepName='Weld step',
    region=region, distributionType=UNIFORM, field='', cf2= 1.0,
    amplitude='FORCE_AMP')
mdb.models['Model-1'].loads['ForcUpUpset'].deactivate('Step-3')
mdb.models['Model-1'].loads['ForcUpUpset'].suppress()

a6 = mdb.models['Model-1'].rootAssembly
region = a6.sets['bottomFlywheelAttachment']
mdb.models['Model-1'].VelocityBC(name='Goupglove', createStepName='Weld step',
    region=region, v2=1.0, amplitude='DISP_AMP')
mdb.models['Model-1'].boundaryConditions['Goupglove'].deactivate('Step-3')
#mdb.models['Model-1'].boundaryConditions['Goupglove'].suppress()



#predefined fields
f1 = a6.instances['Glovepipe_weld-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
f2 = a6.instances['Upset_weld-1'].faces
faces2 = f2.getSequenceFromMask(mask=('[#1 ]', ), )
region = regionToolset.Region(faces=faces1+faces2)
mdb.models['Model-1'].Temperature(name='Predefined Field-1',
    createStepName='Initial', region=region, distributionType=UNIFORM,
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, magnitudes=(initialTemperature, ))

#----------------------MESH
#input

meshSizeTop = 3.0
meshSizeBot = 3.0
nearWeldZone = 15.0
rightCutPosition =65
nearWeldMeshSize = 0.75

#mesh controls
a6 = mdb.models['Model-1'].rootAssembly
partInstanceTop =(a6.instances['Upset_weld-1'], )
partInstanceBot =(a6.instances['Glovepipe_weld-1'], )
a6.seedPartInstance(regions=partInstanceTop, size=meshSizeTop, deviationFactor=0.1)
a6.seedPartInstance(regions=partInstanceBot, size=meshSizeBot, deviationFactor=0.1)
#+
elemType1 = mesh.ElemType(elemCode=CGAX4HT, elemLibrary=STANDARD)
elemType2 = mesh.ElemType(elemCode=CGAX3T, elemLibrary=STANDARD)
a6 = mdb.models['Model-1'].rootAssembly
f1 = a6.instances['Upset_weld-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
f2 = a6.instances['Glovepipe_weld-1'].faces
faces2 = f2.getSequenceFromMask(mask=('[#1 ]', ), )
pickedRegions =((faces1+faces2), )
a6.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
a6 = mdb.models['Model-1'].rootAssembly
partInstances =(a6.instances['Glovepipe_weld-1'],
    a6.instances['Upset_weld-1'], )
a6 = mdb.models['Model-1'].rootAssembly
a1 = mdb.models['Model-1'].rootAssembly
f1 = a1.instances['Upset_weld-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
f2 = a1.instances['Glovepipe_weld-1'].faces
faces2 = f2.getSequenceFromMask(mask=('[#1 ]', ), )
pickedRegions = faces1+faces2
#-
a1.setMeshControls(elemShape=QUAD_DOMINATED, regions=pickedRegions, technique=FREE, allowMapped=False)
a6 = mdb.models['Model-1'].rootAssembly

#partitions
# Find the lowest point on the top pipe
e = a.instances['Upset_weld-1'].edges
upperCutPosition = 0
lowestLocation = 99999
for k in range(len(e)):
    ((x,y,z),) = e[k].pointOn
    if y < lowestLocation:
	lowestLocation = y
upperCutPosition = nearWeldZone+lowestLocation
upperCutPosition = sliceTopInstance('Upset_weld-1',upperCutPosition,nearWeldMeshSize)
surfaceNearBottom('Upset_weld-1','topWeldSurface',upperCutPosition - 0.001)


#-
sliceVerticalInstance('Glovepipe_weld-1',rightCutPosition)

#mesh seeds
removeEdgeSeeds('Upset_weld-1')
removeEdgeSeeds('Glovepipe_weld-1')
#+-
seedNearZeroTop('Upset_weld-1',nearWeldMeshSize,upperCutPosition +0.001)
seedNearZeroLeftTo('Glovepipe_weld-1',nearWeldMeshSize,rightCutPosition+0.001)

#generate mesh
partInstances =(a6.instances['Glovepipe_weld-1'],
    a6.instances['Upset_weld-1'], )
a6.generateMesh(regions=partInstances)
session.viewports['Viewport: 1'].view.fitView()



#----------------------JOB
#input

primaryJobName = 'Upset_weld'
userSubFileName = 'Upsetweld_sub.for'

mdb.saveAs(primaryJobName)
lastForce = 0
lastUpset = 0
lastSpinR = 52.36

import job
#-
#keyword
mdb.models['Model-1'].keywordBlock.synchVersions(storeNodesAndElements=False)
mdb.models['Model-1'].keywordBlock.setValues(edited = 0)
mdb.models['Model-1'].keywordBlock.synchVersions(storeNodesAndElements=False)

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
mdb.models['Model-1'].keywordBlock.insert(historyBlock, """*controls,analysis=discontinuous""")




#+
mdb.Job(name=primaryJobName, model='Model-1', type=ANALYSIS, explicitPrecision=SINGLE,
        nodalOutputPrecision=SINGLE, description='',
        parallelizationMethodExplicit=DOMAIN, multiprocessingMode=DEFAULT,
        numDomains=12, userSubroutine=userSubFileName, numCpus=12, scratch='',
        echoPrint=OFF, modelPrint=OFF, contactPrint=OFF, historyPrint=OFF)

mdb.models['Model-1'].setValues(noPartsInputFile=OFF)
mdb.jobs[primaryJobName].writeInput(consistencyChecking=OFF)
mdb.save()


#-
mdb.models['Model-1'].setValues(noPartsInputFile=OFF)
mdb.jobs[primaryJobName].writeInput(consistencyChecking=OFF)

#JOB RUN
#input
numberCpus=8
numberGpus=12

logFile = openLogFile(primaryJobName)
writeHeading (logFile)


# Run the original analysis
from analysis import AnalysisApplication
#+
cmd = []
cmd.append('-job')
cmd.append('%s' % primaryJobName )
cmd.append('-input')
cmd.append('%s' % primaryJobName )
cmd.append('-user')
cmd.append('%s' % userSubFileName )
cmd.append('-cpus')
cmd.append('%s' % numberCpus )
cmd.append('-interactive')
sys.stdout = sys.__stdout__
job = AnalysisApplication(cmd)
try:
   job.run()
except:
   print "Oops..."

writeModelInfo(logFile,primaryJobName,timeRemaining,0)

totalTime = totalTime + elapsedTime(primaryJobName)
timeRemaining = simulationTime - totalTime
try:
    whyEnd = searchMsgFileStr(primaryJobName,'***ERROR:',11,70)
except:
    whyEnd = 'NO ERROR?'
writeAnalysisInfo(logFile,primaryJobName,totalTime,timeRemaining,whyEnd)
#+
# add U to odb for 2D plot---- aqui prob
add_unew_odb(primaryJobName)

#Remesh if necessary
remeshStart = 0
timeRemaining0 = timeRemaining
#-
timeCount = 0
nRemesh=1
#input
maxRemeshings = 250
#
#+


if timeRemaining >= 1.e-6:
    for remeshIndex in range(remeshStart,maxRemeshings):
	remeshNumber = nRemesh
#+
	
	remeshJobName = newJobName(primaryJobName,remeshNumber)
	ancestorJobName = priorJobName(primaryJobName,remeshNumber)
	
	execfile('Upsetweld_remesh.py')
	writeModelInfo(logFile,remeshJobName,timeRemaining,remeshNumber)
        cmd = []
        cmd.append('-job')
        cmd.append('%s' % remeshJobName )
        cmd.append('-input')
        cmd.append('%s' % remeshJobName )
        cmd.append('-oldjob')
        cmd.append('%s' % ancestorJobName )
        cmd.append('-user')
        cmd.append('%s' % userSubFileName )
        cmd.append('-cpus')
        cmd.append('%s' % numberCpus )
        cmd.append('-interactive')
        sys.stdout = sys.__stdout__
        remeshJob = AnalysisApplication(cmd)
        try:
            remeshJob.run()
        except:
            print "Ooops..."
#-
        if elapsedTime(remeshJobName) >= weldStepTime:
            totalTime = totalTime + elapsedTime(remeshJobName)
            timeCount = timeCount + 1
            nRemesh=nRemesh+1
            add_unew_odb(remeshJobName)
        if elapsedTime(remeshJobName) < weldStepTime:
            totalTime = totalTime - elapsedTime(ancestorJobName)
            weldStepTime = round(weldStepTime/4,4)
           
            outputFrequency = round(weldStepTime/5,4)
            nRemesh=nRemesh-1
            timeCount = 0
       
        timeRemaining = simulationTime - totalTime
        writeAnalysisInfo(logFile,remeshJobName,totalTime,timeRemaining,whyEnd)
        if timeCount >= 5:
            weldStepTime = round(weldStepTime*2,4)
            if weldStepTime >= weldStepTimeA:
               weldStepTime = weldStepTimeA
            timeCount = 0
#+
	if timeRemaining < 1.e-6:
	    break
# cleanup the last few files before exit	
writeEnding(logFile)
print "Job completed successfully!"