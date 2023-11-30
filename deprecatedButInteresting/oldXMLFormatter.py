#This is one of my first promising ones, back when I was naive and thought this might be easy HAHAHAHAHA
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