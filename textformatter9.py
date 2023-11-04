import pandas as pd
import lxml.etree
import pandas_read_xml as pdx
import os
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
#data = []

#dataFrameList = os.listdir("rawdata/timetableChanges/")

#for r, d, f in os.walk(dataFrameList):
#    for file in f:
#        if ".xml" in file:
#            data.append(file)

df = pdx.read_xml(xml)
df = pdx.fully_flatten(df)
print(df)
df.to_excel('output3.xlsx', index=False)
#print(df_parsed)