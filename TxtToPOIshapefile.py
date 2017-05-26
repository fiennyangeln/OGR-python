#import modules that are needed

import osgeo.ogr as ogr
import osgeo.osr as osr
import csv
from pyproj import Proj

#set up the proj to convert xy to latlong
p = Proj(proj='utm',zone=10,ellps='WGS84')

# use a dictionary reader so we can access by field name
reader = open("poiTable.txt","r")

# set up the shapefile driver
driver = ogr.GetDriverByName("ESRI Shapefile")

# create the data source
data_source = driver.CreateDataSource("poi.shp")

# create the spatial reference, WGS84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

# create the layer
try:
    layer = data_source.CreateLayer("poi", srs, ogr.wkbPoint)
except:
    print("file existed.")
    raise
    
# Add the fields we're interested in
layer.CreateField(ogr.FieldDefn("id", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("name_id", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("category", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("type", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("brand", ogr.OFTInteger))
field_type = ogr.FieldDefn("address", ogr.OFTString)
field_type.SetWidth(40)
layer.CreateField(field_type)
field_region = ogr.FieldDefn("tel", ogr.OFTString)
field_region.SetWidth(24)
layer.CreateField(field_region)
layer.CreateField(ogr.FieldDefn("country", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("state", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("city", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("Latitude", ogr.OFTReal))
layer.CreateField(ogr.FieldDefn("Longitude", ogr.OFTReal))

# Process the text file and add the attributes and features to the shapefile
for line in reader:
    array=line.split('^')

    # create the feature
    feature = ogr.Feature(layer.GetLayerDefn())
    
    # Set the attributes using the values from the delimited text file
    feature.SetField("id", int(array[0]))
    feature.SetField("name_id", int(array[1]))
    feature.SetField("category", int(array[2]))
    feature.SetField("type", int(array[3]))
    feature.SetField("brand", int(array[4]))
    feature.SetField("address",(array[5]))
    feature.SetField("tel", array[6])
    feature.SetField("country", int(array[7]))
    feature.SetField("state", int(array[8]))
    feature.SetField("city", int(array[9]))
    x,y=float(array[10]),float(array[11])
    long,lat=p(x,y,inverse=True)
    feature.SetField("Latitude", lat)
    feature.SetField("Longitude", long)

    
    # create the WKT for the feature using Python string formatting
    wkt = "POINT(%f %f)" %  (long , lat)

    # Create the point from the Well Known Txt
    point = ogr.CreateGeometryFromWkt(wkt)

    # Set the feature geometry using the point
    feature.SetGeometry(point)
    
    # Create the feature in the layer (shapefile)
    layer.CreateFeature(feature)

    # Dereference the feature
    feature = None

# Save and close the data source
data_source = None
