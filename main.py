import json
from src.trajectory import Trajectory
from src.visualization import drawClusterOnAllPraj
from src.trajectory_processor import generateDistanceMap, formClusterOfTrajectory, getBigCluster

def main():
    """
    Main function for clustering and visualizing trajectories.

    Reads trajectory data from a JSON file, performs clustering, and visualizes clusters.

    Args:
        None

    Returns:
        None
    """
    # Define hyper-parameters
    windowSize = 200  # The window size for trajectory comparison
    distanceThreshold = 0.5  # The threshold for merge clusters
    sampleSize = 1000  # The number of trajectories to process
    numMostCommonGroupToDisplay = 30  # The number of trajectories clusters shown on the full picture

    # Read and parse trajectory data from the JSON file
    with open(r'data/trajectories.json') as dataFile:
        fileContents = dataFile.read()

    parsedJson = json.loads(fileContents)

    # Create a list of Trajectory instances from the parsed JSON data
    parsedTrajectoryList = [Trajectory(entity) for entity in parsedJson[:sampleSize]]

    # Generate the distance map
    distanceMap = generateDistanceMap(parsedTrajectoryList, windowSize)
    
    # Form clusters of trajectories based on distance map and threshold
    clusters = formClusterOfTrajectory(distanceMap, distanceThreshold)
    
    # Get the biggest clusters for visualization
    bigCluster = getBigCluster(clusters, numMostCommonGroupToDisplay)

    # Visualize each big cluster
    for clusterId, members in bigCluster.items():
        drawClusterOnAllPraj(parsedTrajectoryList, bigCluster, clusterId, title=f'Cluster {clusterId}') 

    numPrajInBigCluster = sum([len(cluster) for _, cluster in bigCluster.items()])
    # Visualize all big clusters and other trajectories in one image
    drawClusterOnAllPraj(parsedTrajectoryList, bigCluster,
                         title=f'Most common {numMostCommonGroupToDisplay} clusters ({numPrajInBigCluster} of {len(parsedTrajectoryList)} trajectories)')

if __name__ == '__main__':
    main()