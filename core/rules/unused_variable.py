from _ast import Assign, Call, FunctionDef
from typing import Any
from ..rule import *


class UnusedVariableVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.variables = {}

    def visit_Assign(self, node):
        if isinstance(node.targets[0], Name):
            variable_name = node.targets[0].id
            if variable_name not in self.variables.keys():
                self.variables[variable_name] = node.lineno
            if isinstance(node.value, BinOp): ##pensar si es necesario mas casos!!
                if isinstance(node.value.left, Name):
                    if node.value.left.id in self.variables.keys():
                        del self.variables[node.value.left.id]
                if isinstance(node.value.right, Name):
                    if node.value.right.id in self.variables.keys():
                        del self.variables[node.value.right.id]


        
    def visit_Call(self, node: Call):
        if isinstance(node.func, Attribute):
            if isinstance(node.func.value, Name):
                if isinstance(node.args[0], Name):
                    del self.variables[node.args[0].id]    
    

    def visit_FunctionDef(self, node: FunctionDef):
        if node.name.startswith('test'):
            NodeVisitor.generic_visit(self, node)
            print(f' Printduicc {self.variables.keys()}')
            for variable in list(self.variables.keys()):
                print(f' Print3 {self.variables[variable]}')
                self.addWarning('UnusedVariable', self.variables[variable],'variable ' + variable + ' has not been used')
            self.variables = {}
    

class UnusedVariableTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = UnusedVariableVisitor()
        visitor.visit(node)
        return visitor.warningsList()
        
    @classmethod
    def name(cls):
        return 'not-used-variable'
