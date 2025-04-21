
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
        self.directory=directory
        self.call_graph = CallGraph(directory=directory,fileName=fileName)
        self.call_graph.add_node(__name__)
        self.callCnt=0
        self.uniqeCalls=uniqueCalls

        self.stk=[__name__]

    

    def track_calls(self,func):
        def wrapped_func(*args, **kwargs):
            caller = self.stk[-1]
            inputID,funcID,resID = self.call_graph.get_func_IDs(func,(args,kwargs))
            callee = funcID
            self.callCnt+=1

            # Add nodes and edges to graph
            self.stk.append(callee)
            res= func(*args,**kwargs)
            self.call_graph.add_fuction_scheme(func,(args,kwargs),res)
            self.call_graph.add_vertice(caller,callee)
            self.stk.pop()
            return res
        return wrapped_func
    
 
    def render(self,*args,**kwargs):
        self.call_graph.render(*args,**kwargs)  
        

    def clear(self):
        GTracker.call_graph = Digraph(comment='Function Call Graph')

        GTracker.stk=["__main__"]




class CallGraph():

    #Styles
    inupNoteStyle=""
    functionNodeStyle=""
    DPNodeStyle=""
    outputNodeStyle=""


    def __init__(self,directory=None,fileName=None):

        self.nodes={} # (f,input),(f,output) -> label
        self.nodeStyles={}
        self.vertices={}
        self.groups={}
        self.fileName=fileName
        self.directory=directory
        self.subGraphs:dict[str,CallGraph]={}
        pass


    def add_node(self,node,label=None,**attrs):
        if label is None:
            label = node
        attrs["label"]=label
        self.nodes[node]=attrs

    def add_vertice(self,u,v, **attrs):
        self.vertices[(u,v)]=attrs
        

    def add_note_to_group(self,node,group):
        if group in self.groups:
            g=self.groups[group]
            g[1].add(node)
        else:
            self.groups[group]=[{},{node}]
        pass

    def add_subraph(self,ID,other):
        self.subGraphs[ID]=other
        

   # def overide_node():
   #     pass


    def get_func_IDs(self,func,inputs):

        in_ID_suff=repr(inputs)

        func_ID=(func.__name__,in_ID_suff)
        inputs_ID=(f"inputs {func.__name__}", in_ID_suff)
        output_ID=(f"outputs {func.__name__}",in_ID_suff)

        return inputs_ID, func_ID,output_ID

    def add_fuction_scheme(self,func, inputs, ouputs, tabulate_outputs=False):
        funcName=func.__name__
        args,kwargs=inputs
        input_table=tabulate(*args,**kwargs)
        res=repr(ouputs)
        input_tableID, funcNodeID, resID = self.get_func_IDs(func=func,inputs=inputs)


        other =CallGraph()

        other.add_node(input_tableID, input_table)
        other.add_node(funcNodeID,funcName)
        other.add_node(resID,res)
        
        other.add_vertice(input_tableID,funcNodeID)
        other.add_vertice(funcNodeID,resID)

        clusterID=("cluster",funcNodeID)
        self.add_subraph(clusterID,other)
        pass

    def add_DP(self,):
        pass

    def add_Base_Case(self,inputs,outputs):
        pass

    

    def render(self,clear=True,ftype="pdf",view=False):
        G = Digraph()
        G.attr(newrank='true')

        NodeDict={}

        vertCnt=0
        edgeCnt=0

        for graph in self.subGraphs.values():
            for vert in graph.nodes:
                if vert in NodeDict:
                    continue
                NodeDict[vert]=f'v{vertCnt}'
                vertCnt+=1

        for vert in self.nodes:
            if vert in NodeDict:
                continue
            NodeDict[vert]=f'v{vertCnt}'
            vertCnt+=1

          
        for clusterID, subgraph in self.subGraphs.items():
            clusterName= 'cluster_'+str(hash(clusterID))
            with G.subgraph(name=clusterName) as sg:
                sg.graph_attr['rank']='same'
                sg.attr(style='filled', color='lightgrey' )
                

                for (u,v), attrs in subgraph.vertices.items():
                    sg.edge(NodeDict[u],NodeDict[v],**attrs)
            with G.subgraph() as g:
                for node,attrs in subgraph.nodes.items():
                    g.attr(rank='same')
                    g.node(NodeDict[node],**attrs)


        for node,attrs in self.nodes.items():
            G.node(NodeDict[node],**attrs)

        for edge,attrs in self.vertices.items():
            u,v = edge
            G.edge(NodeDict[u],NodeDict[v],**attrs)
            
            

        now = datetime.now()
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")  # Format: YYYY-MM-DD HH:MM:SS
        fileName=f"callGraph-{current_datetime}.dot"
        if self.fileName:
            fileName=f"{self.fileName}.dot"

        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)
        G.render(filename=fileName,directory=self.directory,format=ftype,view=view)
        if clear:
            self.clear()

    def clear(self):
        pass