from collections import Counter
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster

def getBigCluster(clusters: list, numMostCommonGroupToDisplay: int) -> dict:
    """
    Identify and return the largest clusters from a list of clusters.

    Args:
        clusters (list): List of cluster assignments for data points.
        numMostCommonGroupToDisplay (int): Number of most common clusters to display.

    Returns:
        dict: Dictionary containing the largest clusters and their member indices.
    """
    clusterMembers = {}  # Create a dictionary to store cluster memberships

    # Assign data points to clusters
    for idx, clusterId in enumerate(clusters):
        if clusterId in clusterMembers:
            clusterMembers[clusterId].append(idx)
        else:
            clusterMembers[clusterId] = [idx]

    cluster_sizes = Counter(clusters)  # Count the size of each cluster
    largest_clusters = cluster_sizes.most_common(numMostCommonGroupToDisplay)  # Find the largest clusters

    big_cluster = {}
    for cluster, size in largest_clusters:
        big_cluster[len(big_cluster)] = clusterMembers[cluster]

    return big_cluster

def formClusterOfTrajectory(distanceMap: np.ndarray, distanceThreshold: float) -> np.ndarray:
    """
    Perform hierarchical clustering on a distance map.

    Args:
        distanceMap (numpy.ndarray): Distance map for entities.
        distanceThreshold (float): Threshold for flat clustering.

    Returns:
        numpy.ndarray: Cluster assignments.
    """
    hierarchicalClusters = linkage(distanceMap, method='single')  # Calculate hierarchical linkage
    maxDistance = distanceThreshold * 2  # Maximum distance for flat clustering

    return fcluster(hierarchicalClusters, t=maxDistance, criterion='distance')

def generateDistanceMap(parsedTrajectoryList: list, windowSize: int) -> np.ndarray:
    """
    Generate a similarity-based distance map for a list of trajectories  using idea of Dilation in image processing.
    The distance is calculated by how many coordinations of the both trajectories near the next trajectory.

    Args:
        parsedTrajectoryList (list): A list of Trajectory instances.
        windowSize (int): Size of the window for similarity calculation.

    Returns:
        numpy.ndarray: A NumPy array containing the similarity-based distance map.
    """
    print(f'There are {len(parsedTrajectoryList)} trajectories in the dataset')

    distanceMap = np.zeros((len(parsedTrajectoryList), len(parsedTrajectoryList)))

    # Calculate the similarity-based distance map
    for i, entity in enumerate(parsedTrajectoryList):
        disArray = []  # Initialize an array to store distances from the current entity

        if i % (len(parsedTrajectoryList) / 20) == 0:
            print(f'{i} of {len(parsedTrajectoryList)} trajectories has been processed')

        # Calculate similarity with all other entities
        for j, entity2 in enumerate(parsedTrajectoryList):
            if i > j:
                continue
            similarity = 1 - entity.similarity(entity2, windowSize)  # Calculate the similarity
            distanceMap[i][j] = similarity
            distanceMap[j][i] = similarity

    print(f'All trajectories have been processed')

    return distanceMap
