def ec2PAmiDetails(ec2, data):
    reservations = ec2.describe_instances()['Reservations']

    if not reservations:
        print("No instances found in the selected region.")
        exit(0)


    for instances in reservations:
        infoAmi = amiInfo(ec2, instances['Instances'][0]['ImageId'])
        if infoAmi is None:
            location = "not present"
            name = 'not present'
            amiPlatDet = 'not present'
        else:
            location = infoAmi['ImageLocation']
            name = infoAmi['Name']
            amiPlatDet = infoAmi['PlatformDetails']

        if instances['Instances'][0].get('Platform'):
            notWin = instances['Instances'][0]['Platform']
        else:
            notWin = 'not windows'
        instances_data = {
            "ID": instances['Instances'][0]['InstanceId'],
            "AMI": instances['Instances'][0]['ImageId'],
            "AMIEc2Plat": notWin,
            "AMIlocation": location,
            "AMIName": name,
            "AMIPlatDetails": amiPlatDet
        }
        data['Instances'].append(instances_data)
    return data


def amiInfo(ec2, location):
    images = ec2.describe_images(
        Filters=[
            {
                'Name': 'image-id',
                'Values': [
                    location
                ]
            }
        ]
    )['Images']
    for ami in images:
        return ami

