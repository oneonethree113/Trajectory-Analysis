import json
from src.trajectory  import Trajectory
from src.visualization import drawClusterOnAllPraj
from src.trajectory_processor import generateDistanceMap,formClusterOfTrajectory,getBigCluster
def main ():
    # Define hyper-parameters
    windowSize = 200  # The window size for trajectory comparison
    distanceThreshold = 0.5  # The threshold for merge cluster 
    sampleSize = 1000  # The number of trajectories to process
    numMostCommonGroupToDisplay=3   # The number of trajectories cluster shown on the full picture

    # Read and parse trajectory data from the JSON file
    with open(r'data/trajectories.json') as dataFile:
        fileContents = dataFile.read()

    parsedJson = json.loads(fileContents)

    # Create a list of Trajectory instances from the parsed JSON data
    parsedTrajectoryList = [Trajectory(entity) for entity in parsedJson[:sampleSize]]

    # Generate the distance map
    distanceMap = generateDistanceMap(parsedTrajectoryList, windowSize)
    clusters = formClusterOfTrajectory(distanceMap,distanceThreshold)
    bigCluster=getBigCluster(clusters,numMostCommonGroupToDisplay)
    
        
        
    for clusterId, members in bigCluster.items():
        drawClusterOnAllPraj(parsedTrajectoryList,bigCluster,clusterId,title=f'Cluster {clusterId}') 
        
    numPrajInBigCluster=sum([len(cluster) for _,cluster in bigCluster.items()])
    drawClusterOnAllPraj(parsedTrajectoryList,bigCluster,title=f'Most common {numMostCommonGroupToDisplay} routes ({numPrajInBigCluster} of {len(parsedTrajectoryList)} trajectories)')

if __name__ == '__main__':
    main()