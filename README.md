<h2>Python</h2>
<p>This is my mini project which mainly implements OGR library to create various shapefiles and convert various shapefiles type into .mp files, .img file, .typ file in order to help with analysis.

How to create .img file to be loaded into Mapsource:

If what you have is shapefile:
  1.Convert the shapefile into .mp file by using shp2mp code on the internet / GPS MapEdit / my python code that I shall provide here soon
  2.Convert the .mp file into .img file, I'm using MapTk for this purpose
  3.Resulted files from MapTk doesn't provide .typ files, so I handcoded it by using the .mp files as an input to produce the .typ files (have a look at my source code <b>mp2typ.py</b>, if you want to use it directly change your .mp file name into "inputfile.mp", place it in the same folder as my sourcecode after you installed python. It shall works and produce "resultedfile.typ"
  4.Use the mapsettoolkit (i'm using version 1.77) to input the .img files as well as .typ files, fill the form, then check the "Install in MapSource" and click start
  5.Close your existing MapSource and open it again. There you'll find your mapset 
</p>

