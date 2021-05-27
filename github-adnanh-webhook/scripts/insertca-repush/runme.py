import subprocess
import argparse
resource_url=""

def checkkill(code):
   if code>0:
      exit(1)
   


parser = argparse.ArgumentParser()
parser.add_argument('jsonstr', type=str,
                    help='json string from harbor')
args = parser.parse_args()
import json
try:
   notification = json.loads(str(args.jsonstr))
   event_data=notification['event_data']
   print("eventdata of type {} with data {}".format(type(event_data),event_data))
   resources=event_data['resources']
   print("resources of type {} with data {}".format(type(resources),resources))
   resource_url=resources[0]['resource_url']
   print("Resource_url is ",resource_url)
except Exception as err:
   print("Error is: \n",err)

try:
   print("Processing {}".format(resource_url))
   import random
   random_no = random.randint(1000000,9999999)
   dockerpull = subprocess.run(["docker","pull",resource_url], stdout=subprocess.DEVNULL)
   print("The exit code for docker pull was: %d" % dockerpull.returncode)
   checkkill(dockerpull.returncode)

   dockercheckcert=subprocess.run(["docker","run","--rm",resource_url,"/bin/bash","-c","ls /usr/share/ca-certificates/extra/ca.dsta.ai.crt"], stdout=subprocess.DEVNULL)
   dockercheckpath=subprocess.run(["docker","run","--rm",resource_url,"/bin/bash","-c","ls /usr/share/ca-certificates/extra"], stdout=subprocess.DEVNULL)
   if dockercheckcert.returncode>0: 
      dockercreate = subprocess.run(["docker","run", "--rm", "-d","--name",str(random_no),str(resource_url)], stdout=subprocess.DEVNULL)
      print("The exit code for docker create was: %d" % dockercreate.returncode)
      checkkill(dockercreate.returncode)

      if dockercheckpath.returncode>0:
          dockercreatepath = subprocess.run(["docker","exec",str(random_no),"mkdir","-p", "/usr/share/ca-certificates/extra"], stdout=subprocess.DEVNULL)
          print("The exit code for docker create path was %d" % dockercreatepath.returncode)
          checkkill(dockercreatepath.returncode)

      dockercp = subprocess.run(["docker","cp","ca.dsta.ai.crt",str(random_no)+":/usr/share/ca-certificates/extra/ca.dsta.ai.crt"], stdout=subprocess.DEVNULL)
      print("The exit code for docker copy was: %d" % dockercp.returncode)
      checkkill(dockercp.returncode)

      dockercommit = subprocess.run(["docker","commit",str(random_no),resource_url],stdout=subprocess.DEVNULL)
      print("The exit code for docker commit was: %d" % dockercommit.returncode)
      checkkill(dockercommit.returncode)

      dockerpush = subprocess.run(["docker","push",resource_url],stdout=subprocess.DEVNULL)
      print("The exit code for docker push was: %d" % dockerpush.returncode)
      checkkill(dockerpush.returncode)

      dockerrm = subprocess.run(["docker","rm","-f",str(random_no)],stdout=subprocess.DEVNULL)
      print("The exit code for docker rm was %d" % dockerrm.returncode)
   else:
      print("Image already has ca certificate, skip")
except Exception as err:
   print("Error is:\n",err)
