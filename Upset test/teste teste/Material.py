#MATERIAL

from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()

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