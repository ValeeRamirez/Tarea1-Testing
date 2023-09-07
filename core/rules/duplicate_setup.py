from _ast import Assign, ClassDef, FunctionDef
import ast
from typing import Any
from ..rule import *


class DuplicatedSetupVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.diccionario = {}
        self.lista = []
        self.contador = 0

    def visit_Assign(self, node: Assign):
        tupla_assign = (node.targets[0].id, node.value.value)
        self.lista.append(tupla_assign)

    def visit_Call(self, node: Call):
        if isinstance(node.func, Attribute):
            atributo = node.func.attr
            if isinstance(node.args[0], Name):
                valor = ''
                for arg in node.args:
                    if isinstance(arg, Name):
                        valor = valor + arg.id
                    elif isinstance(arg, Constant):
                        valor = valor + str(arg.value)
            if isinstance(node.args[0], Constant):
                valor = node.args[0].value
            if isinstance(node.args[0], BinOp):
                valor = ''
                valor = valor + node.args[0].left.id
                valor = valor + node.args[0].right.id
                valor = valor + str(node.args[1].value)
            tupla_call = (atributo, valor)
        self.lista.append(tupla_call)

    def visit_FunctionDef(self, node: FunctionDef):
        if node.name.startswith('test'):
            NodeVisitor.generic_visit(self, node)
            self.diccionario[node.name] = self.lista
            self.lista = []

    def visit_ClassDef(self, node: ClassDef):
        NodeVisitor.generic_visit(self, node)
        for key in self.diccionario.keys():
            test1 = key
        # igual = True
        for i in range(0,len(self.diccionario[test1])):
            igual = True
            for key in self.diccionario.keys():
                if test1 != key:
                    if self.diccionario[test1][i] != self.diccionario[key][i]:
                        igual = False
                        break
            if igual:
                self.contador +=1
            else:
                break
        if self.contador > 0:
            self.addWarning('DuplicatedSetup', self.contador, 'there are ' + str(self.contador) + ' duplicated setup statements') 

class DuplicatedSetupRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = DuplicatedSetupVisitor()
        visitor.visit(node)
        return visitor.warningsList()

    @classmethod
    def name(cls):
        return 'duplicate-setup'
