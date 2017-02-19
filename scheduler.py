import argparse
import json
import os
import re

#
# Global variables
#
project_url = ''
no_days = ''
project = ''

# ----------------------------------
#
# Utility to execute system commands
#
# ----------------------------------

def execute_cmd(cmd):
    print "***** Executing command '"+ cmd + "'"
    response = os.popen(cmd).read()
    return response

# ----------------------------------
#
# Process the git log 
#
# ----------------------------------

def process_commits():
    cmd = "cd " + project + "; git log --all --since=" + str(no_days) + ".day --name-status"
    response = execute_cmd(cmd)

    for line in response.splitlines():
        if line.startswith('commit '):
            print line[7:]
        if line.startswith('Author:'):
            if(re.search('\<(.*?)\>',line)):
                print re.search('\<(.*?)\>',line).group(1)
        if line.startswith('Date:'):
            print line[5:]

#
# Read the program parameters
#
parser = argparse.ArgumentParser(description="Code Review Scheduler Program")
parser.add_argument("-n", nargs="?", type=int, default=1, help="Number of (d)ays to look for log. ")
parser.add_argument("-p", nargs="?", type=str, default="em", help="Project name.")
args = parser.parse_args()

no_days = args.n
project = args.p

#
# Read the scheduler config file
#
with open('config.json') as cfg_file:
    main_config = json.load(cfg_file)

for p in main_config:
    if p['name'] == project:
        project_url = p['git_url']
	break

# Clone the repository if not already exists
print "********* Doing project checkout **********"
if(os.path.isdir("./" + project)):
    execute_cmd("cd " + project + "; git pull")
else:
    execute_cmd("git clone " + project_url + " " + project)
print "*** Done *******"
print " "

print 'Processing the scheduler against project ' + project + '....'
process_commits()
