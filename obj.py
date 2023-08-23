class Coordinates:
    """
    Represents a point with x and y coordinates.

    Args:
        coordinateList (list): A list containing x and y coordinates.

    Attributes:
        x (float): The x-coordinate.
        y (float): The y-coordinate.
    """
    def __init__(self, coordinateList: list):
        self.x = float(coordinateList[0])
        self.y = float(coordinateList[1])

    def withinFilter(self, tar_cor: 'Coordinates', window_size: int) -> bool:
        """
        Checks if the current coordinate is within a given window around the target coordinate.

        Args:
            tar_cor (Coordinates): The target coordinate to compare with.
            window_size (float): The size of the window.

        Returns:
            bool: True if the current coordinate is within the window around the target coordinate, False otherwise.
        """
        
        if not isinstance(tar_cor, Coordinates):
            raise TypeError("tar_cor must be an instance of Coordinates.")
        
        if not isinstance(window_size, int):
            raise TypeError("window_size must be a int.")
            
        return (tar_cor.x <= self.x + window_size/2) and \
               (tar_cor.x >= self.x - window_size/2) and \
               (tar_cor.y <= self.y + window_size/2) and \
               (tar_cor.y >= self.y - window_size/2)

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

    def similarity(self, target_traj: 'Trajectory', window_size: int) -> float:
        """
        Calculates the similarity score of the two trajectories's direction between based on their coordinates.

        Args:
            target_traj (Trajectory): The target trajectory to compare with.
            window_size (float): The size of the window for coordinate comparison.

        Returns:

            float: The similarity score between the two trajectories. The score is within the range of 0 to 1,
                   where 0 indicates no similarity and 1 indicates maximum similarity.
        """
        
        
        if not isinstance(target_traj, Trajectory):
            raise TypeError("tar_cor must be an instance of Coordinates.")
        
        if not isinstance(window_size, int):
            raise TypeError("window_size must be a int.")
            
        score = 0
        for cor in self.traj:
            for tar in target_traj.traj:
                if cor.withinFilter(tar, window_size):
                    score += 1
                    break
        for cor in target_traj.traj:
            for tar in self.traj:
                if cor.withinFilter(tar, window_size):
                    score += 1
                    break
        return score / (len(self.traj) + len(target_traj.traj))
    def trajExport(self):
        """
        Extracts x and y coordinates from the trajectory.

        Returns:
            tuple: A tuple containing two lists. The first list contains x-coordinates and the second list contains y-coordinates.
        """
        x_coords = [cor.x for cor in self.traj]
        y_coords = [cor.y for cor in self.traj]
        return x_coords, y_coords