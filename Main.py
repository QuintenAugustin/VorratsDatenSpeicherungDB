import subprocess
#Orchestrator. This process starts all other processes for data getting and data modification for Python
#If I have excess time I should figure out how to have timeTablePlanned run only hourly
program_list = ["timeTableChanges.py", "timeTablePlanned.py", "textformatter.py"]

for program in program_list: 
    subprocess.call(["python", program])
    print("Finished " + program)