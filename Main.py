import subprocess
#Orchestrator. This process starts all other processes for data getting and data modification for Python
program_list = ["timeTableChanges.py", "timeTablePlanned.py", "textformatter9.py"]

for program in program_list: 
    subprocess.call(["python", program])
    print("Finished " + program)