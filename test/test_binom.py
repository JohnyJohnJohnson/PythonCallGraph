
from ..callGraph.callGraph import GTracker
import sys

#sys.path.insert(0,"..")

def test_bin():

    tracker=GTracker(directory="test_result/bin_result",fileName="grouped calls")
    

    @tracker.track_calls
    def bin(n,k):
        if k<=1:
            return 1
        if k>=n:
            return 1
        return bin(n-1,k)+bin(n-1,k-1)
    

    bin(7,4)
    tracker.render()

    tracker=GTracker(directory="test_result/bin_result",uniqueCalls=True,fileName="unique calls") 
    @tracker.track_calls
    def bin(n,k):
        if k<=1:
            return 1
        if k>=n:
            return 1
        return bin(n-1,k)+bin(n-1,k-1)
    

    bin(7,4)
    tracker.render()
