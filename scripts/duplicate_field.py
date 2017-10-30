from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from PyQt4.QtCore import QVariant


##Duplicate Fied=name
##input_layer=vector
##field_to_duplicate=field input_layer
##fieldname_list=string 


layer = processing.getObject(input_layer)

pr = layer.dataProvider()

caps = pr.capabilities()

def refreshLayer():
    layer.setCacheImage( None )
    layer.dataProvider().forceReload()
    layer.triggerRepaint()
    iface.mapCanvas().refreshAllLayers()

fields = layer.pendingFields()


QVariantDict = {
	4 : QVariant.Int,
	1 : QVariant.Double,
	10 : QVariant.String,
	14 : QVariant.Date,
}

listFieldName = str(fieldname_list).split(';')

newFieldIndex = len(fields)
FieldIdx=0

for field in fields:
	if field.name() == field_to_duplicate:
		FieldIdx = fields.indexFromName(field.name()) 
		field_type = QVariantDict[field.type()]
		field_precision = field.precision()
		field_length = field.length()
		field_widget = layer.editorWidgetV2(FieldIdx)
		field_widgetConfig = layer.editorWidgetV2Config(FieldIdx)
		progress.setText("{},{},{},{}".format(str(field.name()),str(FieldIdx), str(field_widget), str(field_widgetConfig)))
	else:
		pass

for f in listFieldName:
	if f in fields:
		pass
	else :
		if caps & QgsVectorDataProvider.AddAttributes:
			modelProperties= QgsField(f, field_type, str(field_length), int(field_precision), QVariant.String )				
			res = pr.addAttributes([modelProperties])
			layer.updateFields()			
			layer.setEditorWidgetV2(newFieldIndex , field_widget)
			layer.setEditorWidgetV2Config(newFieldIndex , field_widgetConfig)
			newField_widget = layer.editorWidgetV2(newFieldIndex)
			newField_widgetConfig = layer.editorWidgetV2Config(newFieldIndex)
			progress.setText("{},{},{},{}".format(str(f),str(newFieldIndex), str(newField_widget), str(newField_widgetConfig)))
			newFieldIndex += 1


refreshLayer()