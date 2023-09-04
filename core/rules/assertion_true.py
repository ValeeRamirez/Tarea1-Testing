from ..rule import *

class AssertionTrueVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        self.definiciones = []
        
    def visit_Assign(self, node):
        if isinstance(node.value, Constant) and node.value.value == True:
            self.definiciones.append(node.targets[0].id) ##agregamos todos los que definan una variable = True
        self.generic_visit(node)

    def visit_Call(self, node: Call):
        if isinstance(node.func, Name) and node.func.id == 'assertTrue':
            if isinstance(node.args[0], Constant) and node.args[0].value == True:
                self.addWarning('AssertTrueWarning', node.lineno, 'useless assrt true detected')
            if isinstance(node.args[0], Name) and node.args[0].id in self.definiciones:
                self.addWarning('AssertTrueWarning', node.lineno, 'useless assrt true detected')
        self.generic_visit(node)
    

class AssertionTrueTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = AssertionTrueVisitor()
        visitor.visit(node)
        return visitor.warnings
        
    # @classmethod
    # def name(cls):
    #     return 'assertion-true'
    
