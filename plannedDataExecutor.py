import subprocess
#Orchestrator. This process starts all other processes for data getting and data modification for Python
#If I have excess time I should figure out how to have timeTablePlanned run only hourly
program_list = ["timeTablePlanned.py", "sqldatabaseConnectorPlannedData.py"]
print('Bootup sequence initiated, launching data collection probes.')
for program in program_list: 
    subprocess.call(["python", program])
    print("Finished " + program)
print('All programs successfully exectued. Astonishing work as always sir.')