from cosmos.Workflow.models import Workflow
from cosmos.contrib.ezflow.dag import DAG, Split, Add, Map
from tools import ECHO, CAT, WC

####################
# Workflow
####################

dag = ( DAG().
    add([ ECHO(tags={'word':'hello'}), ECHO(tags={'word':'world'}) ]).
    split([('i',[1,2])],CAT).
    map(WC)

)
dag.create_dag_img('/tmp/ex.svg')

#################
# Run Workflow
#################

WF = Workflow.start('Example 1')
dag.add_to_workflow(WF)
WF.run()