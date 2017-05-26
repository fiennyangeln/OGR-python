#import modules that are needed

import osgeo.ogr as ogr
import osgeo.osr as osr
import csv
from pyproj import Proj

#set up the proj to convert xy to latlong
p = Proj(proj='utm',zone=10,ellps='WGS84')

# use a dictionary reader so we can access by field name
reader = open("linkbinary.txt","r")

# set up the shapefile driver
driver = ogr.GetDriverByName("ESRI Shapefile")

# create the data source
data_source = driver.CreateDataSource("links.shp")

# create the spatial reference, WGS84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

# create the layer
try:
    layer = data_source.CreateLayer("links", srs, ogr.wkbLineString)
except:
    print("file existed.")
    raise

# Add the fields we're interested in
layer.CreateField(ogr.FieldDefn("id", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("name", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("FRC", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("PJ", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("SLIPRD", ogr.OFTInteger))
field_type = ogr.FieldDefn("ONEWAY", ogr.OFTString)
field_type.SetWidth(3)
layer.CreateField(field_type)
layer.CreateField(ogr.FieldDefn("elevation1", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("elevation2", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("KPH", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("MINUTES", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("numofcoords", ogr.OFTInteger))
reader.readline()
reader.readline()
for line in reader:    
    array=line.split('^')
    count=int(array[1])
    if(count==0) :break
    # create the feature
    feature = ogr.Feature(layer.GetLayerDefn())
    
    # Set the attributes using the values from the delimited text file
    feature.SetField("id", int(array[2]))
    feature.SetField("name", int(array[0]))
    feature.SetField("FRC", int(array[4]))
    if array[12]=="17":
        feature.SetField("PJ", 1)
    else:
        feature.SetField("PJ", 0)
    feature.SetField("SLIPRD", 0)
    feature.SetField("ONEWAY","U")
    feature.SetField("elevation1", int(array[8]))
    feature.SetField("elevation2", int(array[7]))
    feature.SetField("KPH", int(array[6]))
    feature.SetField("MINUTES", 0)
    feature.SetField("numofcoords",int(array[1]))
    line = ogr.Geometry(ogr.wkbLineString)
    for i in range((count+1)//2):
        coord=reader.readline().split("^")
        for i in range(2):
            x,y=float(coord[i*2]),float(coord[i*2+1])
            long,lat=p(x,y,inverse=True)
            if (x!=0 and y!=0): line.AddPoint(long, lat)
        
    link = ogr.CreateGeometryFromWkt(line.ExportToWkt())
    feature.SetGeometry(link)
    layer.CreateFeature(feature)
    feature=None

data_source=None
"""
line = ogr.Geometry(ogr.wkbLineString)
line.AddPoint(1116651.439379124, 637392.6969887456)
line.AddPoint(1188804.0108498496, 652655.7409537067)
line.AddPoint(1226730.3625203592, 634155.0816022386)
line.AddPoint(1281307.30760719, 636467.6640211721)

links=line.ExportToWkt()
"""
