# initialise modules..
import oci
import io
import os
import json
import uuid
import calendar
import time
from fdk import response
import logging
logging.basicConfig(level=logging.INFO)

# use oracle resource principal provider to extract credentials from rpst token..
def handler(ctx, data: io.BytesIO=None):
   signer = oci.auth.signers.get_resource_principals_signer()
   resp = do(signer)
   return response.Response(ctx,
      response_data=json.dumps(resp),
      headers={"Content-Type": "application/json"})

def do(signer):
   # return data..
   file_list = None
   file_list = []
   
   # configurations of function
   application_id = os.environ['application_id']
   workspace_id = os.environ['workspace_id']
   task_key = os.environ['task_key']

   # initialize client..
   config = {}
   config['log_requests'] = True
   data_integration = oci.data_integration.DataIntegrationClient(config,signer=signer)

   # application_key
   application_key = str
   application_list = data_integration.list_applications(workspace_id).data.items
   for i in application_list:
      if i.identifier == application_id:
         application_key = i.key 
         logging.info("Application identifier: " + i.identifier + " Application key is " + application_key)

   # task run details
   app_name = data_integration.get_application(workspace_id, application_key).data.name
   taskrun_name = app_name + "_func"
   genkey = str(calendar.timegm(time.gmtime()))
   md = oci.data_integration.models.RegistryMetadata(aggregator_key = task_key)
   create_task_run_details = oci.data_integration.models.CreateTaskRunDetails(
      name = taskrun_name,
      key = genkey,
      registry_metadata=md
   )
   
   # create a task run from application
   logging.info("Creating the Data Integration Task Run")
   logging.info("workspace ID: " + workspace_id + " Application Key: " + application_key + " Task Run key: " + create_task_run_details.key )
   taskrun = data_integration.create_task_run(workspace_id, application_key, create_task_run_details)
     
     
