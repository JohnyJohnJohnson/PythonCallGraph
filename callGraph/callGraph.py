
from graphviz import Digraph
import os
from datetime import datetime


def tabulate(*args,**kwargs):
    cont=[]
    for i,arg in enumerate(args):
        line=f"<TR><TD>{i}</TD><TD>{arg}</TD></TR>"
        cont.append(line)

    for key,value in kwargs.items():
        line=f"<TR><TD>{key}</TD><TD>{value}</TD></TR>"
        cont.append(line)

    res=f"<<TABLE> {'\n'.join(cont)}</TABLE>>"
    return res


def get_node_id(*args,**kwargs):
    return str(hash(repr(args)+repr(kwargs)))

    
    pass



class GTracker():


    def __init__(self,directory="call-graphs",fileName=None,uniqueCalls=False):
        self.fileName=fileName
        self.directory=directory
        self.call_graph = Digraph(comment='Function Call Graph')
        self.callCnt=0
        self.uniqeCalls=uniqueCalls

        self.stk=["__main__"]

    

    def track_calls(self,func):
        def wrapped_func(*args, **kwargs):
            caller = self.stk[-1]
            callee_label = f"{tabulate(func.__name__ ,*args,**kwargs)}"
            callee=get_node_id(callee_label)
            self.callCnt+=1
            if self.uniqeCalls:
                callee=f"No.{self.callCnt}\n{callee}"
            self.stk.append(callee,)

            # Add nodes and edges to graph
            self.call_graph.node(caller)
            self.call_graph.node(callee,label=callee_label)
            self.call_graph.edge(caller, callee)
            res= func(*args,**kwargs)
            self.stk.pop()
            return res
        return wrapped_func
    
 
    def render(self,clear=True,ftype="pdf",view=True):
        now = datetime.now()
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")  # Format: YYYY-MM-DD HH:MM:SS
        fileName=f"callGraph-{current_datetime}.dot"
        if self.fileName:
            fileName=f"{self.fileName}.dot"

        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)
        self.call_graph.render(filename=fileName,directory=self.directory,format=ftype,view=view)
        if clear:
            self.clear()

    def clear(self):
        GTracker.call_graph = Digraph(comment='Function Call Graph')

        GTracker.stk=["__main__"]




class CallGraph():

    #Styles
    inupNoteStyle=""
    functionNodeStyle=""
    DPNodeStyle=""
    outputNodeStyle=""


    def __init__(self):

        self.e={} # (f,input),(f,output)
        self.v={}
        self.groups={}
        pass


    def add_node():
        pass

    def add_note_to_group():
        pass

    def overide_node():
        pass

    def add_fuction_scheme():
        pass

    def add_DP():
        pass

    def render():
        pass

