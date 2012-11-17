from cosmos.Cosmos.helpers import groupby
import itertools as it
import networkx as nx
import pygraphviz as pgv
import decorator

class WorkflowDAG(object):
    
    def __init__(self):
        self.G = nx.DiGraph()
        
    def create_dag_img(self):
        print 'hello'
        AG = pgv.AGraph(strict=False,directed=True,fontname="Courier",fontsize=11)
        AG.node_attr['fontname']="Courier-Bold"
        AG.node_attr['fontsize']=12
            
        for task,data in self.G.nodes(data=True):
            AG.add_node(task,label=task.label)
        AG.add_edges_from(self.G.edges())
        AG.layout(prog="dot")
        AG.draw('/tmp/graph.svg',format='svg')
        print 'wrote to /tmp/graph.svg'
        
    def describe(self,generator):
        return list(generator)
        
    def set_parameters(self,params):
        """
        Sets the parameters of every task in the dag
        """
        for task in self.G.node:
            task.parameters = params.get(task.stage_name,{})
            
    def add_to_workflow(self,WF):
        for stage_name, nodes in groupby(self.G.node,lambda t: t.stage_name):
            pass
            #print stage_name
            #print list(nodes)
        #print self.G.in_degree().items()
        #degree_0_tasks = map(lambda x:x[0],filter(lambda x: x[1] == 0,self.G.in_degree().items()))
        #print degree_0_tasks


class DagError(Exception):pass


def merge_dicts(*args):
    """
    Merges dictionaries in *args.  On duplicate keys, right most dict take precedence
    """
    def md(x,y):
        x = x.copy()
        for k,v in y.items(): x[k]=v
        return x
    return reduce(md,args)

class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)
    
WF = None

def infix(func,*args,**kwargs):
    """
    If the second argument is a tuple, submit it as *args
    """
    def wrapped(*args,**kwargs):
        LHS = args[0]
        RHS = args[1] if type(args[1]) == tuple else (args[1],)
        try:
            return func(LHS,*RHS)
        except TypeError:
            raise DagError('Func {0} called with arguments {1} and *{2}'.format(func,LHS,RHS))
    return wrapped

@infix
def _apply(input_tasks,tool_class,stage_name=None):
    if not stage_name: stage_name = tool_class.__name__
    #TODO validate that tool_class.stage_name is unique
    for input_task in input_tasks:
        DAG = input_task.DAG
        new_task = tool_class(stage_name=stage_name,DAG=DAG,tags=input_task.tags)
        DAG.G.add_edge(input_task,new_task)
        yield new_task
        
Apply = Infix(_apply) #map

@infix
def _reduce(input_tasks,keywords,tool_class,stage_name=None):
    if not stage_name: stage_name = tool_class.__name__
    try:
        if type(keywords) != list:
            raise DagError('Invalid Right Hand Side of reduce')
    except Exception:
        raise DagError('Invalid Right Hand Side of reduce')
    for tags, input_task_group in groupby(input_tasks,lambda t: dict([(k,t.tags[k]) for k in keywords])):
        input_task_group = list(input_task_group)
        DAG = input_task_group[0].DAG
        new_task = tool_class(stage_name=stage_name,DAG=DAG,tags=tags)
        for input_task in input_task_group:
            DAG.G.add_edge(input_task,new_task)
        yield new_task
Reduce = Infix(_reduce)

@infix
def _split(input_tasks,split_by,tool_class,stage_name=None):
    if not stage_name: stage_name = tool_class.__name__
    splits = [ list(it.product([split[0]],split[1])) for split in split_by ] #splits = [[(key1,val1),(key1,val2),(key1,val3)],[(key2,val1),(key2,val2),(key2,val3)],[...]]
    for input_task in input_tasks:
        DAG = input_task.DAG
        for new_tags in it.product(*splits):
            tags = tags=merge_dicts(dict(input_task.tags),dict(new_tags))
            new_task = tool_class(stage_name=stage_name,DAG=DAG,tags=tags) 
            DAG.G.add_edge(input_task,new_task)
            yield new_task
Split = Infix(_split)

@infix
def _reduce_and_split(input_tasks,keywords,split_by,tool_class,stage_name=None):
    if not stage_name: stage_name = tool_class.__name__
    splits = [ list(it.product([split[0]],split[1])) for split in split_by ] #splits = [[(key1,val1),(key1,val2),(key1,val3)],[(key2,val1),(key2,val2),(key2,val3)],[...]]
    
    for group_tags,input_task_group in groupby(input_tasks,lambda t: dict([(k,t.tags[k]) for k in keywords])):
        input_task_group = list(input_task_group)
        DAG = input_task_group[0].DAG
        for new_tags in it.product(*splits):
            new_task = tool_class(stage_name=stage_name,DAG=DAG,tags=merge_dicts(group_tags,dict(new_tags)))
            for input_task in input_task_group:
                DAG.G.add_edge(input_task,new_task)
            yield new_task
ReduceSplit = Infix(_reduce_and_split)


    