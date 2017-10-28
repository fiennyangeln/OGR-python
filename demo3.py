import osgeo.ogr as ogr
import osgeo.osr as osr
import os

# Get the input Layer
inShapefile = "BUILDINGS.shp"
inDriver = ogr.GetDriverByName("ESRI Shapefile")
inDataSource = inDriver.Open(inShapefile, 0)
inLayer = inDataSource.GetLayer()

# Create the output Layer
outShapefile = "Buildingcentroid1.shp"
outDriver = ogr.GetDriverByName("ESRI Shapefile")

# Remove output shapefile if it already exists
if os.path.exists(outShapefile):
    outDriver.DeleteDataSource(outShapefile)

# create the spatial reference, WGS84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)


# Create the output shapefile
outDataSource = outDriver.CreateDataSource(outShapefile)
outLayer = outDataSource.CreateLayer("BUILDINGS_centroids", srs, ogr.wkbPoint)


inLayerDefn = inLayer.GetLayerDefn()
for i in range(inLayerDefn.GetFieldCount()):
    fieldDefn = inLayerDefn.GetFieldDefn(i)
    outLayer.CreateField(fieldDefn)

# Get the output Layer's Feature Definition
outLayerDefn = outLayer.GetLayerDefn()

# Add features to the output Layer
for i in range(0, inLayer.GetFeatureCount()):
    # Get the input Feature
    inFeature = inLayer.GetFeature(i)
    # Create output Feature
    outFeature = ogr.Feature(outLayerDefn)
    # Add field values from input Layer
    for i in range(0, outLayerDefn.GetFieldCount()):
        outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetName(), inFeature.GetField(i))
    # Set geometry as centroid
    geom = inFeature.GetGeometryRef()
    centr=ogr.CreateGeometryFromWkt(str(geom)).Centroid()
    inFeature = None
    point=ogr.CreateGeometryFromWkt(str(centr))
    outFeature.SetGeometry(point)
    # Add new feature to output Layer
    outLayer.CreateFeature(outFeature)
    outFeature = None

# Save and close DataSources
inDataSource = None
outDataSource = None
