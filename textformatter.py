import pandas as pd
import lxml.etree
import pandas_read_xml as pdx
import os
import xml.etree.ElementTree as ET
pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 1)

xml = """

"""

#df_out = pd.read_xml(xml, parser="lxml")

#print(df_out)

#df_parsed = pd.read_xml(
#    xml,
#    xpath="//timetable/s/* ",
#    parser="lxml",
#)
#df_address_stack = pd.read_xml(xml,xpath='//employee_name/email/id[contains(@name,"stack")]//address')
#columns = ["id", "eva", "m", "ar", "test", "cp", "l"]
#df_out = pd.DataFrame(
#    data=df_parsed.values.reshape(-1, len(columns)),
#    columns=columns,
    
#)
#df_out = df_out.drop(columns=["m", "ar", "test"])

##Fetches date and time for proper file naming.
#    current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
#
#    #converts datetime object to string and defines Filepath
#    str_current_datetime = str(current_datetime)
#    file_name = str_current_datetime+".xml"
#    timetableChangesFilePath = "rawdata/timetableChanges/"+ file_name

data1 = ET.tostring(ET.parse('rawdata/timetableChanges/8000028.xml').getroot()).decode("utf-8")
data2 = ET.tostring(ET.parse('rawdata/timetableChanges/8000105.xml').getroot()).decode("utf-8")
f = open("preprocessedData/timetableChanges/Output.xml", "a+")
f.write("<new_root>")
f.write(data1)
f.write(data2)
f.write("</new_root>")
f.close()

df = pdx.read_xml("preprocessedData/timetableChanges/Output.xml", [ 'new_root','timetable'], root_is_rows=False)
df = pdx.fully_flatten(df)
print(df)
df.to_excel('output4.xlsx', index=False)