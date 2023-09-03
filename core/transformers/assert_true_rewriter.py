from ast import *
import ast
from core.rewriter import RewriterCommand

# class RewriterCommand:
#     def apply(self, ast):
#         # Por defecto retorna el mismo AST sin ninguna modificacion
#         return ast

class AssertTrueTransformer(NodeTransformer):
    def visit_Call(self, node: Call):
        newNode = NodeTransformer.generic_visit(self, node)
        match newNode:
            case Call(func=Attribute(value=Name(id='self', ctx=Load()),attr='assertEquals',ctx=Load()),
                      args=[Name(id= _ , ctx=Load()), Constant(value=True)], 
                      keywords= _):
                return Call(func=Attribute(value=Name(id='self', ctx=Load()),attr='assertTrue',ctx=Load()),
                            args = [node.args[0]],
                            keywords = node.keywords)
            case _:
                return newNode


    
class AssertTrueCommand(RewriterCommand):
    # Implementar comando, recuerde que puede necesitar implementar además clases NodeTransformer y/o NodeVisitor.
    def apply(self, ast):
        new_tree = fix_missing_locations(AssertTrueTransformer().visit(ast))
        return new_tree

    @classmethod
    def name(self):
        return 'eval'

# tree = parse("self.assertEquals(x, True)")
# command = AssertTrueCommand()
# tree = command.apply(tree)
# print(unparse(tree))