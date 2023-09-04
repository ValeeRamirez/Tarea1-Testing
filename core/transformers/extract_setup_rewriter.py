from ast import *
import ast
from core.rewriter import RewriterCommand

class NodeSetupVisitor(NodeVisitor):
    def __init__(self):
        super().__init__()
        self.funciones = {}
        self.erased = []

    def visit_Module(self, node: Module):
        NodeVisitor.generic_visit(self, node)
        for funcion, values in self.funciones.items(): # este codigo revisa si las variables definidas en las funciones son iguales, solo para CLASES y constantes.
            sameValue = True
            for i in range(len(values)-1):
                if isinstance(values[i], Call):
                    if isinstance(values[i+1], Call):
                        if values[i].func.id != values[i+1].func.id:
                            sameValue = False
                            break
                        else:
                            for j in range(len(values[i].args)):
                                if values[i].args[j].value != values[i+1].args[j].value:
                                    sameValue = False
                                    break
                    else:
                        sameValue = False
                        break
                elif isinstance(values[i], Constant):
                    if isinstance(values[i+1], Constant):
                        if values[i].value != values[i+1].value:
                            sameValue = False
                            break
                    else:
                        sameValue = False
                        break
            if not sameValue or len(values) == 1:
                self.erased.append(funcion)
        for funcion in self.erased:
            del self.funciones[funcion]
        print(self.funciones)

    def visit_FunctionDef(self, node: FunctionDef):
        NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node: Assign):
        if node.targets[0].id not in self.funciones.keys():
            self.funciones[node.targets[0].id] = [node.value]
        else:
            self.funciones[node.targets[0].id].append(node.value)
        NodeVisitor.generic_visit(self, node)

class ExtractSetupTransformer(NodeTransformer):
    def __init__(self, funciones):
        super().__init__()
        self.funciones = funciones
    
    def visit_ClassDef(self, node: ClassDef):
        NodeTransformer.generic_visit(self, node)
        newBody = []
        newFunctionDef = []
        for funcion, values in self.funciones.items():
            newBody.append(Assign(targets=[Attribute(value=Name(id='self', 
                                                                ctx=Load()),
                                                    attr=funcion,
                                                    ctx=Store())],
                                value=values[0]))
        if self.funciones != {}:
            newFunctionDef.append(FunctionDef(name='setUp',
                                        args=arguments(posonlyargs=[],
                                                        args=[arg(arg='self')],
                                                        kwonlyargs=[],
                                                        kw_defaults=[],
                                                        defaults=[]),
                                        body = newBody,
                                        decorator_list=[]))
        return ClassDef(name=node.name, 
                        bases=node.bases, 
                        keywords=node.keywords, 
                        body=newFunctionDef + node.body, 
                        decorator_list=node.decorator_list)
    
    def visit_Assign(self, node: Assign):
        if node.targets[0].id in self.funciones.keys():
            NodeTransformer.generic_visit(self, node)
            return None
        else:
            NodeTransformer.generic_visit(self, node)
            return node
    
    def visit_Name (self, node: Name):
        NodeTransformer.generic_visit(self, node)
        if node.id in self.funciones.keys():
            return Attribute(value=Name(id='self', ctx=Load()),attr=node.id,ctx=Load())
        else:
            return node



class ExtractSetupCommand(RewriterCommand):
    # Implementar comando, recuerde que puede necesitar implementar además clases NodeTransformer y/o NodeVisitor.
    def apply(self, ast):
        visitor = NodeSetupVisitor()
        visitor.visit(ast)
        new_tree = fix_missing_locations(ExtractSetupTransformer(visitor.funciones).visit(ast))
        return new_tree

    @classmethod
    def name(cls):
        return 'extract-setup'


# tree = parse( """class TestX(TestCase):
#     def test_x(self):
#         p = Person("Juan", "?")
#         x = 4
#         self.assertEquals(p.age(),3)
#     def test_k(self):
#         p = Person("Juan", "?")
#         x = 4
#         self.assertEquals(p.age(),3)
#     def test_y(self):
#         p = Person("Juan", "?")
#         self.assertEquals(p.name(),"Juan")""")




# visitor = NodeSetupVisitor()
# visitor.visit(tree)    

