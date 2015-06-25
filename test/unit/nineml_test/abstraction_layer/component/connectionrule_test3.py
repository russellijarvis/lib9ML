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
def inf_check(l1, l2, desc):
    check_list_contain_same_items(l1, l2, desc1='Declared',
                                  desc2='Inferred', ignore=['t'], desc=desc)

#The self argument implies that this method is inside a class.


import nineml.abstraction as al
import os
import nineml

c5 = nineml.read("/home/russell/git/lib9ml/test/xml/neurons/HodgkinHuxleyClass.xml")
c5.items()
#c5.to_xml()
#c5.from_xml()
#c = nineml.read("/home/russell/git/CerebellarCortex/9ml/simple.xml")
#c.items()
#:    <StateVariable name="n" dimension="dimensionless"/>
c1 = nineml.read("/home/russell/git/lib9ml/test/xml/connectionrules/ExplicitConnectionList.xml")#:    <Parameter name="sourceIndices" dimension="dimensionless"/>
c2 = nineml.read("/home/russell/git/lib9ml/test/xml/connectionrules/RandomFanOut.xml")#:    <Parameter name="probability" dimension="dimensionless"/>
c3 = nineml.read("/home/russell/git/lib9ml/test/xml/connectionrules/ProbabilisticConnectivity.xml")#:    <Parameter name="probability" dimension="dimensionless"/>
c4 = nineml.read("/home/russell/git/lib9ml/test/xml/connectionrules/RandomFanIn.xml")#:    <Parameter name="probability" dimension="dimensionless"/>
print c5
print c1
print c2
print c3 
print c4


# Un comment the following file to debug XML syntax errors.
#plan seperate the above file into different files. Then debug parts of them individually.
#c.items()
#



uniform_cls='''
<!-- Element -->
<xs:element name="NormalDistribution" substitutionGroup="un:AbstractDistribution">
  <xs:complexType>
    <xs:complexContent>
      <xs:extension base="un:NormalDistributionType"/>
    </xs:complexContent>
  </xs:complexType>
</xs:element>

<!-- Complex type -->
<xs:complexType name="NormalDistributionType">
  <xs:complexContent>
    <xs:extension base="un:AbstractDistributionType">
      <xs:sequence>
        <xs:element name="mean" type="un:ContinuousValuesType"/>
        <xs:element name="variance" type="un:PositiveRealValuesType"/>
      </xs:sequence>
    </xs:extension>
  </xs:complexContent>
</xs:complexType>
'''                

unifrom_instance='''
<!-- Single value -->
<un:NormalDistribution xmlns:un="http://www.uncertml.org/2.0">
  <un:mean>3.14</un:mean>
  <un:variance>3.14</un:variance>
</un:NormalDistribution>

<!-- Multiple values -->
<un:NormalDistribution xmlns:un="http://www.uncertml.org/2.0">
  <un:mean>3.14 6.28 9.42</un:mean>
  <un:variance>3.14 6.28 9.42</un:variance>
</un:NormalDistribution>
'''                

def get_component():
    aliases = [
        "q10 := 3.0**((celsius - 6.3)/10.0)",  # temperature correction factor
        "alpha_m := -0.1*(V+40.0)/(exp(-(V+40.0)/10.0) - 1.0)",  # m
        "beta_m := 4.0*exp(-(V+65.0)/18.0)",
        "mtau := 1/(q10*(alpha_m + beta_m))",
        "minf := alpha_m/(alpha_m + beta_m)",
        "alpha_h := 0.07*exp(-(V+65.0)/20.0)",               # h
        "beta_h := 1.0/(exp(-(V+35)/10.0) + 1.0)",
        "htau := 1.0/(q10*(alpha_h + beta_h))",
        "hinf := alpha_h/(alpha_h + beta_h)",
        "alpha_n := -0.01*(V+55.0)/(exp(-(V+55.0)/10.0) - 1.0)", # n
        "beta_n := 0.125*exp(-(V+65.0)/80.0)",
        "ntau := 1.0/(q10*(alpha_n + beta_n))",
        "ninf := alpha_n/(alpha_n + beta_n)",
        "gna := gnabar*m*m*m*h",                       # 
        "gk := gkbar*n*n*n*n",
        "ina := gna*(ena - V)",                 # currents
        "ik := gk*(ek - V)",
        "il := gl*(el - V )"]

    hh_regime = al.Regime(
        "dn/dt = (ninf-n)/ntau",
        "dm/dt = (minf-m)/mtau",
        "dh/dt = (hinf-h)/htau",
        "dV/dt = (ina + ik + il + Isyn)/C",
        transitions=al.On("V > theta",do=al.SpikeOutputEvent() )
    )

# the rest are not "parameters" but aliases, assigned vars, state vars, indep vars, analog_analog_ports, etc.
    parameters = ['el', 'C', 'ek', 'ena', 'gkbar', 'gnabar', 'theta', 'gl','celsius', ]
    #c1 = al.ComponentClass("HodgkinHuxley", 
    #                      parameters=parameters,
    #                      regimes=(hh_regime,),
    #                      aliases=aliases)


    #from nineml.abstraction.writers import XMLWriter
    #writers.XMLWriter.write(c1, '/tmp/nineml_toxml1.xml')
   
    #return c1
    return

def get_component2():

    # 
    # Parameter
    # PropertyReceivePort
    # Select
    # Constant
    # Alias 
    #     <Parameter name="k" dimension="dimensionless"/>  
    #     <Parameter name="mu1" dimension="dimensionless" container="source"/>
    #     <Parameter name="sigma1" dimension="dimensionless" container="source"/>
    #     <Parameter name="mu2" dimension="dimensionless" container="source"/>
    #     <Parameter name="sigma2" dimension="dimensionless" container="source"/>

   
    cr.ConnectionRuleXMLLoader    
    cr.ConnectionRuleXMLWriter#.writer
       

    # the rest are not "parameters" but aliases, assigned vars, state vars, indep vars, analog_analog_ports, etc.
    
    al.AnalogReceivePort
    #property_recieve_ports = [al.SendPort("V"), al.ReducePort("Isyn",reduce_op="+")]

    #c1 = al.ComponentClass("RingNetwork", parameters=parameters)
                          #regimes=(hh_regime,),
                          #aliases=aliases, 
                          #analog_ports=analog_ports)

    pms = ['k']
    pms = ['k', 'mu1', 'mu2', 'sigma1', 'sigma2', 'gkbar', 'gnabar', 'theta', 'gl','celsius', ]

    abc=cr.select.Mask.rhs="(GLdistance < dendradius) && (numMFconn == 0) && (ProbMFGoC > rand)"
    #cr.select.RandomVariable
    #|  __init__(self, name, distribution, units)
    #cr.select.RandomVariable(name='uniform', distribution="http://www.uncertml.org/2.0", units="um")
    #cr(name='ringnetwork',select="(GLdistance < dendradius) && (numMFconn == 0) && (ProbMFGoC > rand)",parameters=pms,constants=None, aliases=None )

    cr2=nineml.abstraction.ConnectionRule(name='ringnetwork',select="(GLdistance < dendradius) && (numMFconn == 0) && (ProbMFGoC > rand)",parameters=pms,constants=None, aliases=None)
    cr3=nineml.abstraction.ConnectionRule(name='ringnetwork',select=abc,parameters=pms,constants=None, aliases=None)

    #__init__(self, name, select, parameters=None, constants=None, aliases=None)

    
    return cr2
c1=get_component2()
b=c1.to_xml()
b.items()
b.values()
b.keys()


#AttributeError: 'ConnectionRule' object has no attribute '_property_receive_ports'
#nineml/abstraction/connectionrule/base.py

#Suggesting I need to edit the connection Rule object itself.

class TestConnectionRule(unittest.TestCase, Document):
    # What annotations, there is no actual XML doc, so don't worry
    # about this function decorator!
    #@read_annotations
    
    def runTest():
        pass
    def test_xml_round_trip(self): 
        #write Python objects here.
        #For connection Rules.
        #get_component()
        blocks = ('name','Parameter','Constant','Alias','Select')
        # blocks is of type tuple, but it gets converted to a dictionary
        # as is implied below blocks, when blocks is accesssed by keys.
        
        #There is a special class somewhere that converts blocks to a dictionary.

        #My goal is merely to load components in order to develop and test the XMLWriter class.
        #Do I need to load blocks to do this?

        #cd ~/; grep -r "Andrew" * to find more details of how Andrew writes XML code that loads blocks.

        
       
        #First I need to instantiate the ConnectionRule Component Class.
        #visit_componentclass = annotate_to_xml(self, *args, **kwargs)
        #what are arguments to other writers like?
        
        #cr.ConnectionRuleXMLWriter(
        #    
        #          )

        '''
        cr(
            name=element.get('MF2GC'),
            propertyrecieveport=blocks[""],
            parameters=blocks["Parameter"],
            constant=blocks["Constant"],
            alias=blocks["Alias"],
            select=blocks["Select"]
        )
        '''

        parameters = ['k', 'mu1', 'mu2', 'sigma1', 'sigma2', 'gkbar', 'gnabar', 'theta', 'gl','celsius', ]
        cr=al.ConnectionRule

        #.parameters
        '''
        cr.Select(  
            mask=blocks["mask"],
            number=blocks["number"],#Does the appropriate object get expanded here
            preference=blocks["preference"],
            was_selecteds=blocks["was_selected"], 
            number_selected=blocks["number_selected"],
            random_variables=blocks["random_variables"], 
            select=blocks["select"], 
            repeat_whiles=blocks["repeat_while"]
        )
        return
        '''

        def setUp(self):
            self.c = Constant(name="faraday", value=96485.3365, units=coulomb)


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
         
            parameters = ['k', 'mu1', 'sigma1', 'mu2', 'sigma2']
            crc = al.ConnectionRule("",ConnectCondition=["abs(i-j)<= k"] )  #A list of strings.              
            Document.write(crc, filename)
            return crc
        
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
        #self.c = Constant(name="faraday", value=96485.3365, units=coulomb)
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

         

        #pass

to=TestConnectionRule()
#to.get_component()
to.test_xml_round_trip()

