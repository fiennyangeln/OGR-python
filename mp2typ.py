#initialization
reader=open("inputfile.mp","r")
creator=open("resultfile.typ","w")
starter=True
choice=0
header=["#","[_polygon]\n","[_point]\n","[_line]\n"]
polyorder=[]
for line in reader:
    if starter:
        if "[IMG ID]" in line: creator.write("[_id]\nProductCode=1\nFID=1000\n")
        elif "CodePage" in line: creator.write("".join([line,"\n"]))
        elif "END-IMG" in line:
            creator.write("[End]\n\n")
            starter=False
    elif not choice:
        if "[POLYGON]" in line:
            choice=1
        elif "[POI]" in line:
            choice=2
        elif "[POLYLINE]" in line:
            choice=3
    elif "Type" in line:
        if choice==1 and line not in polyorder:
            polyorder.append(line)
        creator.write("%s%s\n[End]\n" %(header[choice],str(line)))
        choice=0



creator.write("[_drawOrder]\n")
for item in polyorder:
    creator.write(",".join([item,"1\n"]))

creator.write("[End]\n")
creator.close()
reader.close()
