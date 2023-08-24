
from src.trajectory  import Trajectory
from src.coordinates  import Coordinates
import unittest

class TestCoordinates(unittest.TestCase):
    def test_withinFilter(self):
        # Create Coordinates instances
        coord1 = Coordinates([2.0, 2.0])
        coord2 = Coordinates([2.0, 1.0])
        coord3 = Coordinates([1.0, 0.0])
        
        # Test withinFilter method
        self.assertTrue(coord1.withinFilter(coord2, 2))
        self.assertFalse(coord1.withinFilter(coord3, 2))
        self.assertTrue(coord2.withinFilter(coord3, 2))

class TestTrajectory(unittest.TestCase):
    def test_similarity(self):
        # Create Trajectory instances
        traj1 = Trajectory({'object_id': '1', 'object_type': 'type1', 'coordinates': '1.0,2.0 2.0,3.0'})
        traj2 = Trajectory({'object_id': '2', 'object_type': 'type2', 'coordinates': '1.5,2.5 2.5,3.5'})

        # Test similarity method
        similarity_score = traj1.similarity(traj1, 1)
        self.assertEqual(similarity_score,1.0)
        
        similarity_score = traj1.similarity(traj2, 1)
        self.assertIsInstance(similarity_score, float)
        self.assertGreaterEqual(similarity_score, 0.0)
        self.assertLessEqual(similarity_score, 1.0)
        
        similarity_score_rev = traj2.similarity(traj1, 1)
        self.assertEqual(similarity_score,similarity_score_rev)
        
        traj = traj1.trajExport()
        self.assertIsInstance(traj, tuple)
        self.assertEqual(len(traj[0]),len(traj[1]))
        
        
        

if __name__ == '__main__':
    unittest.main()
