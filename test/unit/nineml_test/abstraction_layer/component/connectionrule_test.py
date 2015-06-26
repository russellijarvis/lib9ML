import nineml.abstraction as al
from IPython.utils._tokenize_py2 import Number
from nineml.abstraction.connectionrule import *
from nineml.abstraction import connectionrule
#from nineml.annotations import annotate_xml, read_annotations
#Not an actual XML document yet.
from nineml.xmlns import NINEML, E
import unittest

from nineml.abstraction import connectionrule as cr
from copy import copy, deepcopy
from nineml.abstraction.expressions import (
    Expression, Alias, ExpressionSymbol)


from nineml import annotations 
from nineml import utils
from nineml.annotations import read_annotations

from itertools import chain
from collections import Counter
from nineml.abstraction.dynamics import TimeDerivative, Regime, StateVariable
from sympy import symbols
import sympy

from nineml.document import Document
#def inf_check(l1, l2, desc):
#    check_list_contain_same_items(l1, l2, desc1='Declared',
#                                  desc2='Inferred', ignore=['t'], desc=desc)


import nineml.abstraction as al
import os
import nineml


#First import a whole bunch of examples and show that that the XML documents are able to be converted into lxml Documents
#And from xml documents they are successfuly get converted to a collection of python component class instance objects contained 
#inside objects objects.


c1 = nineml.read("/home/russell/git/lib9ml/test/xml/connectionrules/ExplicitConnectionList.xml")
c2 = nineml.read("/home/russell/git/lib9ml/test/xml/connectionrules/RandomFanOut.xml")
c3 = nineml.read("/home/russell/git/lib9ml/test/xml/connectionrules/ProbabilisticConnectivity.xml")
c4 = nineml.read("/home/russell/git/lib9ml/test/xml/connectionrules/RandomFanIn.xml")
c5 = nineml.read("/home/russell/git/lib9ml/test/xml/neurons/HodgkinHuxleyClass.xml")
c5.items()

# No-where are the Python objects c[1-5] required by the code below, they are here only for an educational purpose.



#Bypass XML documents and create instances of the ConnectionRule class by creating the required attributes, and component classes
#directly within python.

def get_component():

    cr.ConnectionRuleXMLLoader    
    cr.ConnectionRuleXMLWriter   
    # No-where are the Python objects cr.ConnectionRuleXMLLoader/Writer required by the code below, they are here only for an educational purpose.

    pms = ['k']
    pms = ['k', 'mu1', 'mu2', 'sigma1', 'sigma2', 'gkbar', 'gnabar', 'theta', 'gl','celsius', ]
    mask=cr.select.Mask.rhs="(GLdistance < dendradius) && (numMFconn == 0) && (ProbMFGoC > rand)"    
    return nineml.abstraction.ConnectionRule(name='ringnetwork',select=mask,parameters=pms,constants=None, aliases=None)

pc=get_component() #pc=python made component object.
b=pc.to_xml()

for b in enumerate(b.items()): print b
print pc.select
#cr2 = connection rule 2.
cr2=cr.ConnectionRuleXMLLoader(pc)
print cr2


class TestConnectionRule(unittest.TestCase, Document):
    # What annotations, there is no actual XML doc, so don't worry
    # about this function decorator!
    #@read_annotations

    
    def runTest():
        pass
    def test_xml_round_trip(self): 
        blocks = ('name','Parameter','Constant','Alias','Select')


        def setUp(self):
            self.c = Constant(name="faraday", value=96485.3365, units=coulomb)
            self.pms = ['k', 'mu1', 'mu2', 'sigma1', 'sigma2', 'gkbar', 'gnabar', 'theta', 'gl','celsius', ]
            self.mask=cr.select.Mask.rhs="(GLdistance < dendradius) && (numMFconn == 0) && (ProbMFGoC > rand)"    


        def test_xml_roundtrip(self):
            writer = XMLWriter()
            #Above c is a component attribute of this instance object (self), as opposed to class object (cls).
            xml = self.c.accept_visitor(writer)
            #loader = XMLLoader(Document(coulomb))
            #c = loader.load_constant(xml)
            #self.assertEqual(c, self.c, "Constant failed xml roundtrip")


        def load_xml_doc():
            al.ConnectionRuleXMLLoader



        def get_component():
            return nineml.abstraction.ConnectionRule(name='ringnetwork',select=mask,parameters=pms,constants=None, aliases=None)
        
        #@annotate_xml
        def to_xml(self):
            self.standardize_unit_dimensions()
            self.validate()
            return ConnectionRuleXMLWriter().visit(self)

        #@classmethod
        #@read_annotations
        def from_xml(cls, element, document):
            return ConnectionRuleXMLLoader(document).load_connectionruleclass(element)


            

class ConnectionRuletest(unittest.TestCase):

    def setUp(self):
        self.c = nineml.abstraction.ConnectionRule.parameter(name="k")

    def test_accept_visitor(self):
        # Signature: name(self, visitor, **kwargs)
                # |VISITATION|

        class ConstantTestVisitor(TestVisitor):

            def visit_constant(self, component, **kwargs):  # @UnusedVariable @IgnorePep8
                return kwargs

        v = ConstantTestVisitor()
        self.assertEqual(
            v.visit(self.c, kwarg1='Hello', kwarg2='Hello2'),
            {'kwarg1': 'Hello', 'kwarg2': 'Hello2'}
        )

    def test_xml_roundtrip(self):
        writer = XMLWriter()
        xml = self.c.accept_visitor(writer)
        loader = XMLLoader(Document(coulomb))
        c = loader.load_constant(xml)
        self.assertEqual(c, self.c, "Constant failed xml roundtrip")

         


to=TestConnectionRule()
to.test_xml_round_trip()

