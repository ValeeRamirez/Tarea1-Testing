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
                    valor = valor + arg.id
            if isinstance(node.args[0], Constant):
                valor = node.args[0].value
            tupla_call = (atributo, valor)
        self.lista.append(tupla_call)

    def visit_FunctionDef(self, node: FunctionDef):
        if node.name.startswith('test'):
            NodeVisitor.generic_visit(self, node)
            self.diccionario[node.name] = self.lista
            self.lista = []

    def visit_ClassDef(self, node: ClassDef):
        NodeVisitor.generic_visit(self, node)
        print(self.diccionario)
        for key in self.diccionario.keys():
            test1 = key
        # del self.diccionario[test1]
        ## necesito poder recorrer la wea sin que se compare con si mismo 
        igual = False
        for i in range(0,len(self.diccionario[test1])-1):
            for key in self.diccionario.keys():
                if self.diccionario[test1][i] == self.diccionario[key][i]:
                    print('entro igual')
                    print(self.diccionario[test1][i], self.diccionario[key][i])
                    igual = True
                else:
                    igual = False
                if igual:
                    self.contador +=1
                i += 1
        self.contador = self.contador // len(self.diccionario.keys())
        # print('resultado', self.contador)
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
