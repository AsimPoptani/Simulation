from cmath import inf
import imp


import unittest
import Scheduler

# Test the scheduler
class TestScheduler(unittest.TestCase):
    def test_distance(self):
        # Define scheduler
        scheduler = Scheduler.Scheduler(0,0,0,0)
        # Test the distance function (x,y)
        self.assertEqual(scheduler.work_distance((0,0),(0,0)),0)
        self.assertEqual(scheduler.work_distance((0,0),(1,0)),1)
        self.assertEqual(scheduler.work_distance((0,0),(0,1)),1)
        self.assertEqual(scheduler.work_distance((0,0),(1,1)),1.4142135623730951)
    
    def test_time(self):
        # This tests the time to get to a point
        # Define scheduler
        scheduler = Scheduler.Scheduler(0,0,0,0)
        # Test the time function meters,meters per second
        self.assertEqual(scheduler.time_to_point(0,0),0)
        self.assertEqual(scheduler.time_to_point(1,0),inf)
        self.assertEqual(scheduler.time_to_point(0,1),0)
        self.assertEqual(scheduler.time_to_point(1,1),1)
        self.assertEqual(scheduler.time_to_point(10,1),10)
        self.assertEqual(scheduler.time_to_point(1,10),1/10)

