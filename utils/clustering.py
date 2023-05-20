from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans


def perform_clustering(data, config):

    if config["cluster_method"] == "AgglomerativeClustering":
        aggl = AgglomerativeClustering(n_clusters=config['n_clusters'])
        cluster_labels = aggl.fit_predict(data)
        return cluster_labels
    elif config["cluster_method"] == "DBSCAN":
        dbscan = DBSCAN(eps=config["eps"],
                        min_samples=config["min_samples"])
        cluster_labels = dbscan.fit_predict(data)
        return cluster_labels
    elif config["cluster_method"] == "kmeans":
        kmeans = KMeans(n_clusters=config['n_clusters'])
        kmeans.fit(data)
        cluster_labels = kmeans.fit_predict(data)
        return cluster_labels
    else:
        print("Unknow cluster method")
        exit(1)
