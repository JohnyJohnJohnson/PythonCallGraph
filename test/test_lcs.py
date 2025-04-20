
from ..callGraph.callGraph import GTracker
import sys

#sys.path.insert(0,"..")

def test_lcs():

    tracker=GTracker(directory="test_result/lcs_result",fileName="grouped calls")
    

    @tracker.track_calls
    def lcs(a,b):   
        if not a or not b:
            return ""
        
        if a[-1]==b[-1]:
            return a[-1] + lcs(a[:-1],b[:-1])
        
        return max(lcs(a[:-1],b),lcs(a,b[:-1]))
    

    lcs("carlua","curlau")
    tracker.render()

    tracker=GTracker(directory="test_result/lcs_result",uniqueCalls=True,fileName="unique calls")        
    @tracker.track_calls
    def lcs(a,b):   
        if not a or not b:
            return ""
        
        if a[-1]==b[-1]:
            return a[-1] + lcs(a[:-1],b[:-1])
        
        return max(lcs(a[:-1],b),lcs(a,b[:-1]))
    

    lcs("carl","curl")
    tracker.render()
