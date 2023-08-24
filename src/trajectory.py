
from src.coordinates  import Coordinates
class Trajectory:
    """
    Represents a trajectory with a unique ID, type, and a list of coordinates.

    Args:
        entity (dict): A dictionary representing the trajectory entity.

    Attributes:
        id (str): The unique identifier of the trajectory.
        type (str): The type of the trajectory.
        traj (list): A list of Coordinates objects representing the trajectory path.
    """
    def __init__(self, entity: dict):
        self.id = entity['object_id']
        self.type = entity['object_type']
        self.traj = [Coordinates(cor.split(',')) for cor in entity['coordinates'].split()]

    def similarity(self, targetTraj: 'Trajectory', windowSize: int) -> float:
        """
        Calculates the similarity score of the two trajectories's direction between based on their coordinates.

        Args:
            targetTraj (Trajectory): The target trajectory to compare with.
            windowSize (float): The size of the window for coordinate comparison.

        Returns:

            float: The similarity score between the two trajectories. The score is within the range of 0 to 1,
                   where 0 indicates no similarity and 1 indicates maximum similarity.
        """
        
        
        if not isinstance(targetTraj, Trajectory):
            raise TypeError("tar_cor must be an instance of Coordinates.")
        
        if not isinstance(windowSize, int):
            raise TypeError("windowSize must be a int.")
            
        score = 0
        for cor in self.traj:
            for tar in targetTraj.traj:
                if cor.withinFilter(tar, windowSize):
                    score += 1
                    break
        for cor in targetTraj.traj:
            for tar in self.traj:
                if cor.withinFilter(tar, windowSize):
                    score += 1
                    break
        return score / (len(self.traj) + len(targetTraj.traj))
    def trajExport(self) -> tuple:
        """
        Extracts x and y coordinates from the trajectory.

        Returns:
            tuple: A tuple containing two lists. The first list contains x-coordinates and the second list contains y-coordinates.
        """
        x_coords = [cor.x for cor in self.traj]
        y_coords = [cor.y for cor in self.traj]
        return x_coords, y_coords