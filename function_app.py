import azure.functions as func
import logging
import os
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobSasPermissions, generate_blob_sas
from datetime import datetime, timezone, timedelta

app = func.FunctionApp()
@app.function_name(name="sendEmailTo")
@app.blob_trigger(arg_name="myblob",
                  path="uploadeddocuments",
                  connection="documentvaultbtcloud_STORAGE") 

def gatherFileInfo(myblob: func.InputStream, context: func.Context):
    executionID = context.invocation_id  # Obtain the ID of the uploaded document. 
    fileName = myblob.name  # Obtain the name of the uploaded document.
    metadata = myblob.metadata  # Obtain the metadata of the uploaded document.
    currentTimeUTC = datetime.now(timezone.utc)  # Obtain the current time in UTC.  
    accountKey = os.environ["documentvaultbtcloud_STORAGE"]  # Obtain the account key from the environment variable.\
    expiryTime = currentTimeUTC + timedelta(days=1)


    sendToEmail = metadata.get('SendToEmail', None)
    if sendToEmail:
        logging.info(f"We're sending this to {sendToEmail}")


    sasToken = generate_blob_sas(
            account_name="documentvaultbtcloud",
            container_name="",
            blob_name=myblob.name,
            account_key=os.environ["documentvaultbtcloud_STORAGE_KEY"],
            permission=BlobSasPermissions(read=True),
            start=currentTimeUTC,
            expiry=expiryTime,
            protocol="https"
        )
    
    logging.info(f"Blob URL: {myblob.uri}")
    logging.info(f"SAS Token: {sasToken}")
    logging.info(f"SAS and Blob URL: {myblob.uri}?{sasToken}")








