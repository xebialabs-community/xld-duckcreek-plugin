import json, glob

# build up variable with glob path
path1 = str(deployed.file.path)
path = glob.glob(path1 + "/*.json")

# Locate and store manifest.json information
for f_name in path:
    with open(f_name, 'r') as data_file:
        data = json.load(data_file)

# Generate deployment for each appserver item
for appFile in data["appServerFiles"]:
    if appFile.get('file'):
        context.addStep(steps.powershell(
            description="Deploying Duck Creek app source: %s " % appFile["source"] ,
            script="duckcreek/deploy.ps1",
            order=60,
            powershell_context={'deployedApplication': deployedApplication, 'source': appFile["source"], 'target': appFile["target"], 'copytype': appFile["copytype"], 'file':appFile["file"]}))
    else:
        context.addStep(steps.powershell(
            description="Deploying Duck Creek app source: %s " % appFile["source"] ,
            script="duckcreek/deploy.ps1",
            order=60,
            powershell_context={'deployedApplication': deployedApplication, 'source': appFile["source"], 'target': appFile["target"], 'copytype': appFile["copytype"]}))

# Generate deployment for each webserver item
for webFile in data["webServerFiles"]:
    if webFile.get('file'):
        context.addStep(steps.powershell(
            description="Deploying Duck Creek app source: %s " % webFile["source"] ,
            script="duckcreek/deploy.ps1",
            order=60,
            powershell_context={'deployedApplication': deployedApplication, 'source': webFile["source"], 'target': webFile["target"], 'copytype': webFile["copytype"], 'file':webFile["file"]}))
    else:
        context.addStep(steps.powershell(
            description="Deploying Duck Creek app source: %s " % webFile["source"] ,
            script="duckcreek/deploy.ps1",
            order=60,
            powershell_context={'deployedApplication': deployedApplication, 'source': webFile["source"], 'target': webFile["target"], 'copytype': webFile["copytype"]}))

# Generate IIS restart on successful deployment
if data["restartIIS"] == "True":
    context.addStep(steps.powershell(
        description="Issue IIS restart command",
        script="duckcreek/iis_restart.ps1",
        order=80,
        powershell_context={'deployedApplication': deployedApplication}))

# Generate IIS restart on successful deployment
if data["updateDBserver"] == "True":
    context.addStep(steps.powershell(
        description="Issue database restart command",
        script="duckcreek/db_restart.ps1",
        order=90,
        powershell_context={'deployedApplication': deployedApplication}))
