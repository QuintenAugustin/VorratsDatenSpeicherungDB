import os
import xml.etree.ElementTree as ET

#The goal is to add all xml files into a single batch that can then be added to a pandas dataframe.
#This is pretty roundabout. Adding everything initially into one massive file may doable. 
#This should be tested. Deletion after being added to dataframe happens anyways.
#YOU SHOULD TEST FOR CORRECTNESS!
#dataFrameList = os.getcwd("rawdata/timetableChanges/")

#data = []

#for r, d, f in os.walk(dataFrameList):
 #   for file in f:
  #      if ".xml" in file:
   #         data.append(file)

#preProcessedChangeData = "preprocessedData/timetableChanges/output.xml"

#Writes timetable changes to file
#with open(preProcessedChangeData, 'w') as f:
#    f.write(data)
#    f.close()


    