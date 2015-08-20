from rootpy.tree import Tree, TreeModel, TreeChain
from rootpy.io import root_open
from random import gauss
from rootpy import asrootpy


# This is to copy a file and modify its eventweight by a normalization factor:

nf = 218.243/65.802

chain = TreeChain(name="MVATree", files="ggH125mixca05.root")
f_copy = root_open("ggH125mixca05_copy.root",'recreate')
tree_copy = Tree("MVATree")

tree_copy.set_buffer(chain._buffer, create_branches=True)

for entry in chain:
    entry.EventWeight = entry.EventWeight*nf
    tree_copy.Fill()


tree_copy.Write()
f_copy.Close()

