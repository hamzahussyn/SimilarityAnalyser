import ast  
import astor 
import math
import json
import re
from difflib import SequenceMatcher
from difflib import unified_diff


JsonObject = {  
    "lines" : '', 
    "length" : '', 
    "disSimilarity" : '', 
    "probableSimilarity" : '', 
    "modify" : '', 
    "ratio" : '', 
    "index" : '', 
    "tree" : '', 
    "i" : 0
}

JsonObjectTwo = {
    "similarExpressions" : 0.0,
    "similarAssignments" : 0.0,
    "similarIterators" : 0.0,
    "similarFunctions" : 0.0,
    "similarIdentifiers" : 0.0
}

expr = []
expr_2 = []
expr_helper = []
collect_if_helper = []
collect_assign_1 = []
collect_assign_2 = []
collect_assign_helper = []
collect_call_1 = []
collect_call_2 = []
collect_call_helper = []
collect_for_1 = []
collect_for_2 = []
collect_for_helper = []
targetsOne = []
targetsTwo = []
targets = []


'''
Helper functions are defined here
'''


def nearestTen(a, b):
    greater = max(a, b)
    rounded = round(greater/10)*10
    return rounded


def compareNodes(array_one, array_two):
    ratio = 0
    if len(array_one) > len(array_two):
        start_1 = len(array_one)
        start_2 = len(array_two)
        assign_1_bigger = True
    else:
        start_1 = len(array_two)
        start_2 = len(array_one)
        assign_1_bigger = False

    for i in range(start_1):
        for j in range(start_2):
            if assign_1_bigger:
                if array_one[i] == array_two[j]:
                    ratio = ratio + 1
            else:
                if array_two[i] == array_one[j]:
                    ratio = ratio + 1
    if start_1 != 0:
        return round((ratio/start_1) * 100, 2)
    else:
        return 0

def compareIdentifiers(array_one, array_two):
    ratio = 0
    if len(array_one) > len(array_two):
        start_1 = len(array_one)
        start_2 = len(array_two)
        assign_1_bigger = True
    else:
        start_1 = len(array_two)
        start_2 = len(array_one)
        assign_1_bigger = False

    for i in range(start_1):
        for j in range(start_2):
            if assign_1_bigger:
                if array_one[i] == array_two[j]:
                    ratio = ratio + 1
                    break
            else:
                if array_two[i] == array_one[j]:
                    ratio = ratio + 1
                    break
    if start_1 != 0:
        return round((ratio/(start_1)) * 100, 2)
    else:
        return 0                

def compareExpr():
    ratio = 0
    if len(expr) > len(expr_2):
        start_1 = len(expr)
        start_2 = len(expr_2)
        expr_bigger = True
        expr_2_bigger = False
    else:
        start_1 = len(expr_2)
        start_2 = len(expr)
        expr_bigger = False
        expr_2_bigger = True

    match = 0

    for i in range(start_1):
        for j in range(start_2):
            for k in range(3):
                if expr_bigger:
                    if expr_2[j][k] == expr[i][k]:
                        match = match + 1
                else:
                    if expr_2[i][k] == expr[j][k]:
                        match = match + 1
            if match >= 2:
                print("\n\n")
                print(expr_2[i])
                print(" ==== ")
                print(expr[j])
                print("\n\n")
                ratio = ratio + 1
            match = 0
    if start_1 != 0:
        return (ratio / start_1) * 100
    else:
        return 0    

'''
Node Transformer Class
AST's own class NodeTransformer is used to normalize the AST
Get rid of unimportant information
and information specific to the nodes.

Node Visitor Class
Below this is the NodeVisitor class, to traverse the tree
and extract useful details to compare later.
'''


class nodeTransformer(ast.NodeTransformer):
    def visit_Name(self, node):
        if hasattr(node, 'id'):
            del node.id
        self.generic_visit(node)
        return node

    def visit_Assign(self, node):
        # if hasattr(node, 'ctx'):
        # del node.ctx
        if hasattr(node, 'type_comment'):
            del node.type_comment
        for target in node.targets:
            if isinstance(target, ast.Name):
                del target.id
        del node.targets
        self.generic_visit(node)
        return node

    def visit_Attribute(self, node):
        del node.attr
        del node.ctx
        self.generic_visit(node)
        return node

    def visit_For(self, node):
        node.target
        self.generic_visit(node)
        return node

    def visit_Import(self, node):
        pass

    def visit_ImportFrom(self, node):
        pass

    def visit_Call(self, node):
        if hasattr(node, 'args'):
            if len(node.args) == 0:
                del node.args
        del node.keywords
        self.generic_visit(node)
        return(node)


class nodeVisitor(ast.NodeVisitor):

    def visit_Name(self, node):
        targets.append(node.id)

    def visit_Assign(self, node):
        this_assignment = []
        for target in node.targets:
            if isinstance(target, ast.Name):
                if hasattr(target, 'id'):
                    this_assignment.append(target.id)
        if hasattr(node, 'value'):
            if hasattr(node.value, 'value'):
                this_assignment.append(node.value.value)
        collect_assign_helper.append(this_assignment)

    def visit_BinOp(self, node):
        this_expr = []
        # this_expr.append(astor.dump_tree(node))
        this_expr.append(astor.dump_tree(node.left))
        this_expr.append(astor.dump_tree(node.op))
        this_expr.append(astor.dump_tree(node.right))
        expr_helper.append(this_expr)
        self.generic_visit(node)


    def visit_Compare(self, node):
        this_comparer = []
        if hasattr(node.left, 'id'):
            this_comparer.append(node.left.id)
        elif hasattr(node.left, 'value'):
            this_comparer.append(node.left.value)     
        this_comparer.append(astor.dump_tree(node.ops))
        for c in node.comparators:
            if hasattr(c, 'id'):
                this_comparer.append(node.left.id)
            elif hasattr(c, 'value'):
                this_comparer.append(c.value)
        collect_if_helper.append(this_comparer)

    def visit_For(self, node):
        this_for = []
        if hasattr(node.target, 'id'):
            this_for.append(node.target.id)
        this_for.append(astor.dump_tree(node.iter))
        # print(node.iter.id)
        collect_for_helper.append(this_for)

    def visit_Call(self, node):
        this_call = []
        # print(astor.dump_tree(node.func))
        if hasattr(node.func, 'id'):
            this_call.append(node.func.id)
        for arg in node.args:
            if hasattr(arg, 'value'):
                this_call.append(arg.value)
            elif hasattr(arg, 'id'):
                this_call.append(arg.id)
            else:
                this_call.append(astor.dump_tree(arg))
        collect_call_helper.append(this_call)
        self.generic_visit(node)    


'''
Unified Diff Algorithm

use of unified_diff from the difflib library, 
mainly to identify disimilarity and average out the similarity of 
longest common sequence and the probable similarity in the code.
'''

def Unified_Diff_Algorithm(treeOne, treeTwo):
    treeline = astor.dump_tree(treeOne).split('\n')
    treeline2 = astor.dump_tree(treeTwo).split('\n')
    # Splitted both the trees into lists on each new line.

    n = astor.dump_tree(treeOne)

    percentage = 0
    percentageTwo = 0

    #count1 = -1
    #count2 = -1

    for line in unified_diff(treeline, treeline2, n=0):
        if line[0] == '-':
            if percentage == 0:
                percentage = (len(line)/len(n))*100
            else:
                percentage = percentage + (len(line))
        if line[0] == '+':
            if percentageTwo == 0:
                percentageTwo = (len(line)/len(n))*100
            else:
                percentageTwo = percentageTwo + (len(line))
   
    Dissimilarity = round((percentage / len(n)) * 100, 2)
    Similarity = round(100 - (percentage / len(n)) * 100, 2)
    codeToAdd = round((percentageTwo / len(n)) * 100, 2)
    matchedSequences = round(SequenceMatcher(None, ast.dump(treeOne), ast.dump(treeTwo)).ratio() * 100, 2)
    amplify = Similarity + matchedSequences
    amplify = amplify/math.ceil(amplify/100.0) * nearestTen(Similarity, matchedSequences)
    result = round(amplify / 100, 2)

    JsonObject['lines'] = f"Total lines in AST = {len(treeline)}"
    JsonObject['length'] = f"Character length of candidate file = {len(n)}"
    JsonObject['disSimilarity'] = f"Dissimilarity = {Dissimilarity} % "
    JsonObject['probableSimilarity'] = f"Probable Similarity = {Similarity} %"
    JsonObject['modify'] = f"Code to add from reference to candidate will amount to {codeToAdd} %"
    JsonObject['ratio'] = f"Ratio of Matching sequences found = {matchedSequences} %"
    JsonObject['index'] = f"Similarity Index: {result} %"
    JsonObject['i'] = result
    JsonObject['tree'] = n

#in {(len(treeline)-count1) if(len(treeline)-count1)>0 else 0} lines of AST
#in {count1} lines of AST
#of candidate and {count2} lines of AST

'''
Functions to export
'''
def analyseSimilarity(codeOne, codeTwo):

    docStringRegEx = r'"""[\s\S]*?"""'
    codeOne = re.sub(docStringRegEx, '', codeOne)
    codeTwo = re.sub(docStringRegEx, '', codeTwo)
    
    docStringRegExTwo = r'\'\'\'[\s\S]*?\'\'\''
    codeOne = re.sub(docStringRegExTwo, '', codeOne)
    codeTwo = re.sub(docStringRegExTwo, '', codeTwo)

    treeOne = ast.parse(codeOne)
    treeTwo = ast.parse(codeTwo)

    # TRANSFORMING THE TREE HERE
    TreeOneTransformed = nodeTransformer().visit(treeOne)
    TreeTwoTransformed = nodeTransformer().visit(treeTwo)

    global JsonObject

    Unified_Diff_Algorithm(TreeOneTransformed, TreeTwoTransformed)

    return json.dumps(JsonObject)


def analyseNodes(codeOne, codeTwo):

    treeOne = ast.parse(codeOne)
    treeTwo = ast.parse(codeTwo)

    global expr
    global expr_2 
    global expr_helper  
    global collect_assign_1 
    global collect_assign_2 
    global collect_assign_helper
    global collect_call_1 
    global collect_call_2 
    global collect_call_helper 
    global collect_for_1 
    global collect_for_2 
    global collect_for_helper
    global targetsOne
    global targetsTwo
    global targets 
    global JsonObjectTwo

    # VISITING NODES HERE

    nodeVisitor().visit(treeOne)
    # helpers go here
    collect_for_1 = collect_for_helper
    collect_for_helper = []

    collect_call_1 = collect_call_helper
    collect_call_helper = []

    expr = expr_helper
    expr_helper = []

    collect_assign_1 = collect_assign_helper
    collect_assign_helper = []

    targetsOne = targets
    targets = []

    nodeVisitor().visit(treeTwo)
    # helpers go here
    collect_for_2 = collect_for_helper
    collect_for_helper = []

    collect_call_2 = collect_call_helper
    collect_call_helper = []

    expr_2 = expr_helper
    expr_helper = []

    collect_assign_2 = collect_assign_helper
    collect_assign_helper = []

    targetsTwo = targets
    targets = []

    r = compareExpr()
    JsonObjectTwo["similarExpressions"] = r
    
    r = compareNodes(collect_assign_1, collect_assign_2)
    JsonObjectTwo["similarAssignments"] = r
    
    r = compareNodes(collect_for_1, collect_for_2)
    JsonObjectTwo["similarIterators"] = r

    r = compareNodes(collect_call_1, collect_call_2)
    JsonObjectTwo["similarFunctions"] = r

    r = compareIdentifiers(targetsOne, targetsTwo)
    JsonObjectTwo["similarIdentifiers"] = r

    return json.dumps(JsonObjectTwo)       