from _ast import Assign, FunctionDef
from typing import Any
from ..rule import *
import re


class AssertionLessVisitor(WarningNodeVisitor):
    # Implementar Clase
    def __init__(self):
        super().__init__()
        self.definiciones = []
        self.has_assert = False  # Para verificar cuales no tienen assert
        self.assert_pattern = re.compile(r'assert[A-Z]\w*')

    def visit_Call(self, node: Call):
        if isinstance(node.func, Attribute):
            if self.assert_pattern.match(node.func.attr):
                print(f' Print3 {node.func.attr}')
                # if isinstance(node.func.value, Name) and node.func.value.id == 'self':
                #     print(f' Print1 {node.args[0].value}')
                self.has_assert = True  # Se encontró una llamada a self.assert..
                ##siento que aca estoy agregando una linea nomas, pero hay que agregar la llamada de funcion o no?
        NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node: FunctionDef):
        # Revisar cuales no tenian assert
        if not self.has_assert:
            print(f' Print2 {node.name}')
            self.addWarning('AssertionLessWarning', node.lineno, 'it is an assertion less test')
        # Restablecer la variable de seguimiento antes de visitar la siguiente función
        self.has_assert = False
        NodeVisitor.generic_visit(self, node)

class AssertionLessTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = AssertionLessVisitor()
        visitor.visit(node)
        return visitor.warningsList()

        
    @classmethod
    def name(cls):
        return 'assertion-less'
