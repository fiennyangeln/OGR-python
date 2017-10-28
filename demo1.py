from osgeo import ogr
point = ogr.Geometry(ogr.wkbPoint) #or wkbLineString
point.AddPoint(1198054.34, 648493.09)
print (point.ExportToWkt())
