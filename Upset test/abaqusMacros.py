# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def Macro1():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    pass


def Macro2():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
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


