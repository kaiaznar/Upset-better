from abaqus import *
from abaqusConstants import *
import odbAccess
import annotationToolset
from odbAccess import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()

def takePictures(baseJob):
	remeshNumber = 0
	cont = True
	while cont:
		endereco = os.getcwd()
		if remeshNumber == 0:
			arqName = baseJob + '.odb'
			
			print arqName
		else:
			arqName =  baseJob + '_remesh_' + '%i' % (remeshNumber) + '.odb'
		try:
			
			odb = session.openOdb(name = endereco + '/' + arqName)
			vw = session.viewports['Viewport: 1']
			vw.setValues(displayedObject=odb)
			vw.odbDisplay.display.setValues(plotState=(
				CONTOURS_ON_DEF, ))
			vw.odbDisplay.setFrame(step=1, frame=0 )
			vw.view.setValues(session.views['Front'])
			vw.view.setValues(nearPlane=336.241, 
        farPlane=494.981, width=96.6194, height=38.085, viewOffsetX=20.3436, 
        viewOffsetY=-4.72025)
			picFile = endereco + '/' + 'Frame_' + '%i' % (remeshNumber)
			session.printToFile(
				fileName = picFile ,
				format=TIFF,canvasObjects=(vw, ))
			remeshNumber += 1
			endereco += '/' + arqName
			session.odbs[endereco].close()
		except:
			print 'nao deu'
			cont = False
	#session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        #DEFORMED, ))
    #session.viewports['Viewport: 1'].odbDisplay.setDeformedVariable(
        #variableLabel='UNEW', )
    #session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        #CONTOURS_ON_DEF, ))
		
takePictures('Upset_weld')