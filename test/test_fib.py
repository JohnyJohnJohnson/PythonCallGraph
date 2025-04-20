
from ..callGraph.callGraph import GTracker
import sys

#sys.path.insert(0,"..")

def test_fib():

    tracker=GTracker(directory="test_result/fib_result",fileName="grouped calls")
    

    @tracker.track_calls
    def fib(n):
        if n<=2:
            return 1
        return fib(n-1)+fib(n-1)
    

    fib(6)
    tracker.render()

    tracker=GTracker(directory="test_result/fib_result",uniqueCalls=True,fileName="unique calls")        
    @tracker.track_calls
    def fib(n):
        if n<=2:
            return 1
        return fib(n-1)+fib(n-1)
    

    fib(6)
    tracker.render()
