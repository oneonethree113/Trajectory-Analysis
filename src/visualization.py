import matplotlib.cm as cm

from src.trajectory  import Trajectory
from src.coordinates  import Coordinates

import matplotlib.pyplot as plt
def generate_distinct_colors(num_colors: int) ->list:
    if not isinstance(num_colors, int):
        raise TypeError("num_colors must be a int.")
    # Get a colormap with the desired number of colors
    colormap = cm.get_cmap('tab20', num_colors)
    
    # Generate a list of distinct colors
    distinct_colors = [colormap(i) for i in range(num_colors)]
    
    return distinct_colors
def drawClusterOnAllPraj(allTrajectory: list,clusterSet: dict,clusterIdx=None,title='')->None:
    if not isinstance(allTrajectory, list):
        raise TypeError("allTrajectory must be a list.")
    if not isinstance(clusterSet, dict):
        raise TypeError("clusterSet must be a dict.")
    if not isinstance(title, str):
        raise TypeError("title must be a str.")
    
    #colors for visualization
    cluster_colors=generate_distinct_colors(len(clusterSet))
    clusterPrajList=[]
    if clusterIdx==None:
        for cluster_idx,cluster in clusterSet.items():
            for mem in cluster:
                clusterPrajList.append(mem)
        for idx,traj in enumerate(allTrajectory):
            if idx in clusterPrajList:
                continue
            x_coords, y_coords = traj.trajExport()
            plt.plot(x_coords, y_coords, color='black')
        for cluster_idx,cluster in clusterSet.items():
            for mem in cluster:
                traj=allTrajectory[mem]
                x_coords, y_coords = traj.trajExport()
                plt.plot(x_coords, y_coords, color=cluster_colors[cluster_idx])
        # Add labels and title
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title(title)
        plt.savefig(f'images/Cluster.png')
        plt.clf()
    else:
        for mem in clusterSet[clusterIdx]:
            clusterPrajList.append(mem)
        
        for idx,traj in enumerate(allTrajectory):
            if idx in clusterPrajList:
                continue
            x_coords, y_coords = traj.trajExport()
            plt.plot(x_coords, y_coords, color='black')
            
        for mem in clusterSet[clusterIdx]:
            traj=allTrajectory[mem]
            x_coords, y_coords = traj.trajExport()
            plt.plot(x_coords, y_coords, color=cluster_colors[clusterIdx])
        
        
        # Add labels and title
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title(title)
        plt.savefig(f'images/Cluster{clusterIdx}.png')
        plt.clf()