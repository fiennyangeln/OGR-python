from osgeo import ogr
import os

daShapefile = r'buildings.shp'
#ways to check if exist

#1. but can't detect incomplete file
#if not os.path.isfile(R"C:\Users\Angelina\Downloads\PARCELS.shp"):
#    raise IOError('Could not find file ' + str(R"C:\Users\Angelina\Downloads\PARCELS.shp"))

dataSource = ogr.Open(daShapefile)
#2. dataSource will return None if shapefile doesn't exist
if dataSource is None:
    print ('Could not open %s' % (daShapefile))
daLayer = dataSource.GetLayer(0)
layerDefinition = daLayer.GetLayerDefn()

fieldName=[]
print ("Name  -  Type  Width  Precision")
for i in range(layerDefinition.GetFieldCount()):
    fieldName.append(layerDefinition.GetFieldDefn(i).GetName())
    fieldTypeCode = layerDefinition.GetFieldDefn(i).GetType()
    fieldType = layerDefinition.GetFieldDefn(i).GetFieldTypeName(fieldTypeCode)
    fieldWidth = layerDefinition.GetFieldDefn(i).GetWidth()
    GetPrecision = layerDefinition.GetFieldDefn(i).GetPrecision()

    print (fieldName[i] + " - " + fieldType+ " " + str(fieldWidth) + " " + str(GetPrecision))
fieldnumber=i+1
print(fieldnumber)
#get the shapefile feature count
layer = dataSource.GetLayer()
featureCount = layer.GetFeatureCount()
print ("Number of features in %s: %d" % (os.path.basename(daShapefile),featureCount)) #return the shapefile name & number of feature

file_write=open("phonenumber.txt","w")
driver = ogr.GetDriverByName("ESRI Shapefile")
dataSource1 = driver.Open(daShapefile, 0)
layer = dataSource1.GetLayer()

#access specific index of layer
feature=layer[3]
print(feature.GetField(fieldName[4]))

#iterate through all
for feature in layer:
    for j in range(fieldnumber):
        file_write.write( str(feature.GetField(fieldName[j]))+'\t')
    file_write.write('\n')

file_write.close()

#to iterate from the start
layer.ResetReading()

