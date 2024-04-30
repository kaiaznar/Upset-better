# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 6.12-1 replay file
# Internal Version: 2012_03_13-20.23.18 119612
# Run by Kai on Wed May 15 15:04:23 2019
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=189.676559448242, 
    height=212.425003051758)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
Mdb()
#: A new model database has been created.
#: The model "Model-1" has been created.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
o1 = session.openOdb(
    name='D:/kai/02. Simulacao/Upset test - CVC 3/Upset_weld_remesh_106.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: D:/kai/02. Simulacao/Upset test - CVC 3/Upset_weld_remesh_106.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     2
#: Number of Meshes:             2
#: Number of Element Sets:       6
#: Number of Node Sets:          9
#: Number of Steps:              3
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=2, frame=0 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=2, frame=0 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=1, frame=21 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=1, frame=0 )
session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
session.viewports['Viewport: 1'].view.setValues(nearPlane=335.457, 
    farPlane=495.765, width=75.6589, height=34.7305, viewOffsetX=19.6424, 
    viewOffsetY=3.90946)
session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
session.viewports['Viewport: 1'].view.setValues(nearPlane=339.621, 
    farPlane=491.601, width=28.8747, height=13.2547, viewOffsetX=17.6766, 
    viewOffsetY=0.552273)
session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
session.viewports['Viewport: 1'].view.setValues(nearPlane=338.256, 
    farPlane=492.965, width=44.3363, height=20.3522, viewOffsetX=16.3219, 
    viewOffsetY=45.3798)
session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
session.viewports['Viewport: 1'].view.setValues(nearPlane=337.907, 
    farPlane=493.315, width=48.2805, height=22.1627, viewOffsetX=17.4958, 
    viewOffsetY=-0.824239)
Mdb()
#: A new model database has been created.
#: The model "Model-1" has been created.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
