from collections import Counter
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster

def getBigCluster(clusters: np.ndarray, numMostCommonGroupToDisplay: int) -> dict:
    """
    Identify and return the largest clusters from a list of clusters.

    Args:
        clusters (np.ndarray): List of cluster assignments for data points.
        numMostCommonGroupToDisplay (int): Number of most common clusters to display.

    Returns:
        dict: Dictionary containing the largest clusters and their member indices.
    """
    
    if not isinstance(clusters, np.ndarray):
        raise TypeError("clusters must be a np.ndarray.")
    if not isinstance(numMostCommonGroupToDisplay, int):
        raise TypeError("numMostCommonGroupToDisplay must be a int.")
    clusterMembers = {}  # Create a dictionary to store cluster memberships

    # Assign data points to clusters
    for idx, clusterId in enumerate(clusters):
        if clusterId in clusterMembers:
            clusterMembers[clusterId].append(idx)
        else:
            clusterMembers[clusterId] = [idx]

    clusterSizes = Counter(clusters)  # Count the size of each cluster
    largestClusters = clusterSizes.most_common(numMostCommonGroupToDisplay)  # Find the largest clusters

    bigCluster = {}
    for cluster, size in largestClusters:
        bigCluster[len(bigCluster)] = clusterMembers[cluster]

    return bigCluster

def formClusterOfTrajectory(distanceMap: np.ndarray, distanceThreshold: float) -> np.ndarray:
    """
    Perform hierarchical clustering on a distance map with ski-learn.

    Args:
        distanceMap (numpy.ndarray): Distance map for entities.
        distanceThreshold (float): Threshold for flat clustering.

    Returns:
        numpy.ndarray: Cluster assignments.
    """
    if not isinstance(distanceMap, np.ndarray):
        raise TypeError("distanceMap must be a np.ndarray.")
    if not isinstance(distanceThreshold, float):
        raise TypeError("distanceThreshold must be a float.")
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
    if not isinstance(parsedTrajectoryList, list):
        raise TypeError("parsedTrajectoryList must be a list.")
    if not isinstance(windowSize, int):
        raise TypeError("windowSize must be a int.")
    print(f'There are {len(parsedTrajectoryList)} trajectories in the dataset')

    distanceMap = np.zeros((len(parsedTrajectoryList), len(parsedTrajectoryList)))

    # Calculate the similarity-based distance map
    for i, entity in enumerate(parsedTrajectoryList):
        disArray = []  # Initialize an array to store distances from the current entity

        if i % 10 == 0:
            print(f'{i} of {len(parsedTrajectoryList)} trajectories has been processed')

        # Calculate similarity with all other trajectories
        for j, entity2 in enumerate(parsedTrajectoryList):
            if i > j:
                continue
            distance = 1 - entity.similarity(entity2, windowSize)  # Calculate the similarity
            distanceMap[i][j] = distance
            distanceMap[j][i] = distance

    print(f'All trajectories have been processed')

    return distanceMap

def generateDistanceMapForLargeData(parsedTrajectoryList: list, windowSize: int) -> np.ndarray:
    """
    Generate a similarity-based distance map for a list of trajectories using the concept of Dilation in image processing.
    The distance is calculated based on how many coordinates of both trajectories are near each other.
    The execution time will be shorter when dataset has more than 3000 trajectories.

    Args:
        parsedTrajectoryList (list): A list of Trajectory instances.
        windowSize (int): The size of the window for similarity calculation.

    Returns:
        numpy.ndarray: A NumPy array containing the similarity-based distance map.
    """
    if not isinstance(parsedTrajectoryList, list):
        raise TypeError("parsedTrajectoryList must be a list.")
    if not isinstance(windowSize, int):
        raise TypeError("windowSize must be a int.")
    print(f'There are {len(parsedTrajectoryList)} trajectories in the dataset')

    distanceMap = np.zeros((len(parsedTrajectoryList), len(parsedTrajectoryList)))

    xMaxList = []
    yMaxList = []

    # Calculate the maximum x and y coordinates 
    for i, entity in enumerate(parsedTrajectoryList):
        x_coords, y_coords = entity.trajExport()
        xMaxList.append(max(x_coords))
        yMaxList.append(max(y_coords))

    xMax = max(xMaxList)
    yMax = max(yMaxList)

    trajAreaList = []

    # Calculate the area occupied by each trajectory in the space
    for i, entity in enumerate(parsedTrajectoryList):

        areaMap = np.zeros((int(xMax + windowSize/2) + 1, int(yMax + windowSize/2) + 1))
        x_coords, y_coords = entity.trajExport()

        for x, y in zip(x_coords, y_coords):
            areaMap[int(x - windowSize/2):int(x + windowSize/2), int(y - windowSize/2):int(y + windowSize/2)] = 1

        trajAreaList.append(areaMap)

    for i, entity in enumerate(parsedTrajectoryList):
        disArray = []  # Initialize an array to store distances from the current entity

        if i % 10 == 0:
            print(f'{i} of {len(parsedTrajectoryList)} trajectories has been processed')

        # Calculate similarity with all other trajectories
        for j, entity2 in enumerate(parsedTrajectoryList):
            if i > j:
                continue
            
            # Calculate the difference in areas and the similarity distance
            diff = np.absolute(trajAreaList[i] - trajAreaList[j])
            distance = np.sum(diff) / (np.sum(trajAreaList[i]) + np.sum(trajAreaList[j]))

            # Assign the calculated distance to the distance map
            distanceMap[i][j] = distance
            distanceMap[j][i] = distance

    print(f'All trajectories have been processed')

    return distanceMap