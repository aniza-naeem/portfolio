from fileinput import filename
import requests
import datetime
import json
from datetime import date
from datetime import timedelta
import pandas as pd
import csv
from azure.storage.blob import BlobServiceClient
from pathlib import Path 
import os

#import config
import settings

# current local date
today = date.today()
yesterday = today - timedelta(days = 1)

# GLOBLAL VARIABLES

#################################################################
apikey = settings.apikey
endate = yesterday.strftime("%Y-%m-%d")
date=[]
productname=[]
servicename=[]
familyname=[]
familysize=[]
cost=[]
nextpage = 0
product_core_cost = {"date":[],"productname":[],"cost":[]};  
####################################################################

def UploadToBlobStorage(filename):

    print ("uploading csv to blob storage")
    blobname = "product"+Path(filename).name
    connection = BlobServiceClient.from_connection_string(settings.connectionString)
    blob_client = connection.get_blob_client(container=settings.containerName, blob=blobname)

    # Upload the created file
    with open(filename, "rb") as data:
        blob_client.upload_blob(data,overwrite=True)  
    
    print ("uploading completed")

   
########################################################################
def getcostdata(startdate,enddate,costdimension):

    global nextpage
    apiurl= settings.apiurl + '?start_date={start_date}&end_date={end_date}&dimensions={dimensions},category3,instance_size&metrics=total_amortized_cost,resource_identifier_count&sort=category3ASC&filters=enhanced_service_name%3D%3DAzure%20Compute&filters=usage_family%3D%3DInstance%20Usage&filters=instance_family!%3D(not set)&filters=instance_family!%3Dnot set&token={nextpagetoken}'.format(start_date=startdate,end_date=enddate,dimensions=costdimension,nextpagetoken=nextpage)

    response = requests.get(apiurl,auth=(apikey,''))
   
    if(response.status_code==200):
        jsondata = response.json() 
        costresults= jsondata["results"]
        print (len(costresults))
        for item in costresults:
            temp_size= item["instance_size"]
            instance_count= item["resource_identifier_count"]
            total_core= int(temp_size)*int(instance_count)

            temp_cost=  item['total_amortized_cost']
            core_cost= float(temp_cost)/int(total_core)

            product_core_cost["date"].append(item["date"])
            product_core_cost["productname"].append(item["category3"])
            product_core_cost["cost"].append(core_cost)

    pagination= jsondata["pagination"]
    if "next" in pagination:
        nextpage = pagination["next"] # get the next page
    else:
        nextpage=0


#####################################################################################

def GetProductCPUcost(startdate,enddate,costdimension):
    global nextpage

    apiurl= settings.apiurl + '?start_date={start_date}&end_date={end_date}&dimensions={dimensions},category3,instance_size&metrics=total_amortized_cost,resource_identifier_count&sort=category3ASC&filters=enhanced_service_name%3D%3DAzure%20Compute&filters=usage_family%3D%3DInstance%20Usage&filters=instance_family!%3D(not set)&filters=instance_family!%3Dnot set&token={nextpagetoken}'.format(start_date=startdate,end_date=enddate,dimensions=costdimension,nextpagetoken=nextpage)
    
    response = requests.get(apiurl,auth=(apikey,''))

    if(response.status_code==200):
        jsondata = response.json() 
        costresults= jsondata["results"]
        print (len(costresults))
        for item in costresults:
            temp_size= item["instance_size"]
            instance_count= item["resource_identifier_count"]
            total_core= int(temp_size)*int(instance_count)

            temp_cost=  item['total_amortized_cost']
            core_cost= float(temp_cost)/int(total_core)

            product_core_cost["date"].append(item["date"])
            product_core_cost["productname"].append(item["category3"])
            product_core_cost["cost"].append(core_cost)

        pagination= jsondata["pagination"]
        if "next" in pagination:
            nextpage = pagination["next"] # get the next page
            while nextpage!=0:
                getcostdata(startdate,enddate,costdimension)  

        print(len(product_core_cost["productname"]))
        dataframe= pd.DataFrame(product_core_cost)
        results = dataframe.groupby(["date","productname"]).mean() 
        csv_columns = ['date','productname','cost']
        #filename =  settings.folderpath+startdate+'_'+enddate+'_'+costdimension+'.csv'
        filename =  settings.folderpath+startdate+'_'+costdimension+'.csv'

        
        if (os.path.exists(filename)):
            os.remove(filename)
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=csv_columns)
                writer.writeheader()
                for index, row in results.iterrows():
                    writer.writerow({'date':index[0],'productname':index[1], 'cost': row[0]})
         
            UploadToBlobStorage(filename)
        else:
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=csv_columns)
                writer.writeheader()
                for index, row in results.iterrows():
                    writer.writerow({'date':index[0],'productname':index[1], 'cost': row[0]})
         
            UploadToBlobStorage(filename)

#Get per day cost data
GetProductCPUcost('2022-10-21',endate,'date')
# Get month wise cost data
#GetProductCPUcost('2022-10-15',endate,'year_month')
#GetProductCPUcost('2022-04-01','2022-06-30','year_month')

