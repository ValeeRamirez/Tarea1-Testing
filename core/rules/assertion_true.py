from ..rule import *

class AssertionTrueVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.definiciones = []
        
    def visit_Assign(self, node):
        if isinstance(node.targets[0], Name):
            if isinstance(node.value, Constant) and node.value.value == True:
                self.definiciones.append(node.targets[0].id) ##agregamos todos los que definan una variable = True
        NodeVisitor.generic_visit(self, node)

    def visit_Call(self, node: Call):
        if isinstance(node.func, Attribute) and node.func.attr == 'assertTrue':
            if isinstance(node.func.value, Name) and node.func.value.id == 'self':
                # print(f' Print1 {node.args[0].value}')
                if isinstance(node.args[0], Constant) and node.args[0].value == True:
                    print(f' Print1 {node.args[0].value}')
                    self.addWarning('AssertTrueWarning', node.lineno, 'useless assert true detected')
                if isinstance(node.args[0], Name) and node.args[0].id in self.definiciones:
                    print(f' Print3 {node.args[0].id}')
                    self.addWarning('AssertTrueWarning', node.lineno, 'useless assert true detected')
        NodeVisitor.generic_visit(self, node)
    

class AssertionTrueTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = AssertionTrueVisitor()
        visitor.visit(node)
        return visitor.warningsList()
        
    # @classmethod
    # def name(cls):
    #     return 'assertion-true'
    
