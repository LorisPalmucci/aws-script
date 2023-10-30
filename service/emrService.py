def cluster(emr, data):
    clusters = emr.list_clusters()

    if not clusters:
        print("No clusters found in the selected region.")
        exit(0)

    clusterInfo(clusters['Clusters'], emr, data)

    if clusters.get('Marker'):
        while clusters.get('Marker'):
            clusters = emr.list_clusters(
                Marker=clusters['Marker']
            )
            clusterInfo(clusters['Clusters'], emr, data)
    return data


def clusterInfo(clusters, emr, d):
    for clus in clusters:
        clusterID = clus['Id']
        appVersion = clusterDetails(clusterID, emr)
        emr_data = {
            "IdCluster": clus['Id'],
            "App Version": appVersion
        }
        d["Clusters"].append(emr_data)


def clusterDetails(ID, emr):
    clusterInf = emr.describe_cluster(ClusterId=ID)

    return clusterInf['Cluster']['ReleaseLabel']
