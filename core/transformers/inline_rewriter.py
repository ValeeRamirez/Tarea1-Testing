from ast import *
from core.rewriter import RewriterCommand
import ast


class NodeInlineVisitor(NodeVisitor):
    def __init__(self):
        super().__init__()
        self.variables = dict()

    def visit_FunctionDef(self, node: FunctionDef):
        NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node: Assign):
        self.variables[node.targets[0].id] = {"valor": node.value, "usos": 0}
        NodeVisitor.generic_visit(self, node)
    
    def visit_Name (self, node: Name):
        NodeVisitor.generic_visit(self, node)
        if node.id in self.variables:
            self.variables[node.id]["usos"] += 1
        
    
class InlineTransformer(NodeTransformer):
    def __init__(self, diccionario):
        super().__init__()
        self.variables = diccionario
                                      

    def visit_Assign(self, node: Assign):
        if node.targets[0].id in self.variables:
            if self.variables[node.targets[0].id]["usos"] == 2:
                NodeTransformer.generic_visit(self, node)
                return None
            else:
                NodeTransformer.generic_visit(self, node)
                return node
        else:
            NodeTransformer.generic_visit(self, node)
            return node

    def visit_Name (self, node: Name):
        NodeTransformer.generic_visit(self, node)
        if node.id in self.variables:
            if self.variables[node.id]["usos"] == 2:
                return self.variables[node.id]["valor"]
            else:
                return node
        else:
            return node
            

class InlineCommand(RewriterCommand):
    def apply(self, ast):
        visitor = NodeInlineVisitor()
        visitor.visit(ast)    
        print(visitor.variables)
        new_tree = fix_missing_locations(InlineTransformer(visitor.variables).visit(ast))
        return new_tree

    @classmethod
    def name(self):
        return 'eval'

# tree = parse( """def test(self):
#                             x = complex_method()
#                             y = x + 2
#                             z = x + y
#                             self.assertEquals(z,2)""")
# command = InlineCommand()
# tree = command.apply(tree)
# print(unparse(tree))

