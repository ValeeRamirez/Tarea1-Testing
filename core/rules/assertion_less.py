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

    def visit_Call(self, node: Call):
        if isinstance(node.func, Attribute):
            if 'assert' in node.func.attr:
                self.has_assert = True  # Se encontró una llamada a assert..

    def visit_FunctionDef(self, node: FunctionDef):
        NodeVisitor.generic_visit(self, node)
        # Revisar cuales no tenian assert
        if not self.has_assert:
            self.addWarning('AssertionLessWarning', node.lineno, 'it is an assertion less test')
        # Restablecer la variable de seguimiento antes de visitar la siguiente función
        self.has_assert = False

class AssertionLessTestRule(Rule):
    def analyze(self, node):
        visitor = AssertionLessVisitor()
        visitor.visit(node)
        return visitor.warningsList()
        
    @classmethod
    def name(cls):
        return 'assertion-less'
