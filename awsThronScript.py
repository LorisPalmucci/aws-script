import sys
import boto3
import json

from service import *


def credentialBootstrap():
    # Get the AWS account name
    account_id = boto3.client('sts').get_caller_identity()['Account']

    # Get the list of AWS account-enabled regions
    session = boto3.session.Session()
    available_regions = session.get_available_regions(serv)

    # Show the user the list of available regions and let them choose one
    print("List of available regions:")
    for i, region in enumerate(available_regions, 1):
        print(f"{i}. {region}")

    region_index = int(input("Select the number corresponding to the desired region: ")) - 1

    if region_index < 0 or region_index >= len(available_regions):
        print("Invalid selection.")
        exit(1)

    selected_region = available_regions[region_index]
    print(f"You have selected the region: {selected_region}")

    # Connect to the selected region
    session = boto3.Session(region_name=selected_region)

    s = session.client(serv)

    # Retrieve and list all detached EBS volumes

    jsonData = {
        "Account": account_id,
        "Region": selected_region,
        getService(f"{serv}"): []
    }
    return s, jsonData, selected_region, account_id


# ec2service.ec2PAmiDetails(session.client('service'))
def createOutput():
    # Write the JSON data to the output file
    output_file_name = f"{accId}_{reg}.json"
    with open(output_file_name, "w") as output_file:
        json.dump(json_data, output_file, indent=4, default=str)

    print(f"Output saved to file: {output_file_name}")

# funzione prinicpale di avvio
if __name__ == '__main__':
    #prende in ingresso il servizio specifico ed avvia il boot delle credenziali
    serv = str(sys.argv[1])
    service, json_data, reg, accId = credentialBootstrap()

    if serv == 'emr':
        cluster(service, json_data)
    elif serv == 'ec2':
        ec2PAmiDetails(service, json_data)
    #stampa l'output in formato json
    createOutput()
