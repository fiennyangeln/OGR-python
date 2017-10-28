#import modules that are needed

import osgeo.ogr as ogr
import osgeo.osr as osr
import csv

# use a dictionary reader so we can access by field name
reader = csv.DictReader(open(R"INCIDENTS.CSV"),
    delimiter=',',
    quoting=csv.QUOTE_NONE)

# set up the shapefile driver
driver = ogr.GetDriverByName("ESRI Shapefile")

# create the data source
data_source = driver.CreateDataSource("incidents.shp")

# create the spatial reference, WGS84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

# create the layer
layer = data_source.CreateLayer("incidents", srs, ogr.wkbPoint)

# Add the fields we're interested in
field_type = ogr.FieldDefn("ID", ogr.OFTString)
field_type.SetWidth(40)
layer.CreateField(field_type)
field_region = ogr.FieldDefn("Region", ogr.OFTString)
field_region.SetWidth(24)
layer.CreateField(field_region)
layer.CreateField(ogr.FieldDefn("Latitude", ogr.OFTReal))
layer.CreateField(ogr.FieldDefn("Longitude", ogr.OFTReal))

# Process the text file and add the attributes and features to the shapefile
for row in reader:
    # create the feature
    feature = ogr.Feature(layer.GetLayerDefn())
    # Set the attributes using the values from the delimited text file
    feature.SetField("ID", str(row['id']))
    feature.SetField("Region", str(row['location']))
    feature.SetField("Latitude", row['lat'])
    feature.SetField("Longitude", row['long'])

    # create the WKT for the feature using Python string formatting
    wkt = "POINT(%f %f)" %  (float(row['long']) , float(row['lat']))

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
