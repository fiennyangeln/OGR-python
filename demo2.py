from osgeo import ogr
import osgeo.osr as osr

# set up the shapefile driver
driver = ogr.GetDriverByName("ESRI Shapefile")

# create the data source
data_source = driver.CreateDataSource("demo.shp")

# create the spatial reference, WGS84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

# create the layer
layer = data_source.CreateLayer("demo", srs, ogr.wkbLineString)
layer.CreateField(ogr.FieldDefn("ID", ogr.OFTInteger))
"""
# create feature directly
feature = ogr.Feature(layer.GetLayerDefn())
feature.SetField("ID",1000)
point = ogr.Geometry(ogr.wkbPoint) #or wkbLineString
point.AddPoint(103.852722, 1.296964)
feature.SetGeometry(point)
layer.CreateFeature(feature)
feature=None
"""
# create feature using WKT
feature = ogr.Feature(layer.GetLayerDefn())
feature.SetField("ID",1000)
line_wkt="LINESTRING (103.850530 1.294531,103.850727 1.294793,103.851114 1.295246,103.851850 1.295996)"
line=ogr.CreateGeometryFromWkt(line_wkt)
feature.SetGeometry(line)
layer.CreateFeature(feature)
feature = None

data_source =None

