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