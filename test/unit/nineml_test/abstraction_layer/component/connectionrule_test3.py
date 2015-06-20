import nineml.abstraction_layer as al
from IPython.utils._tokenize_py2 import Number
from nineml.abstraction_layer.connectionrule import *
from nineml.abstraction_layer import connectionrule
#from nineml.annotations import annotate_xml, read_annotations
#Not an actual XML document yet.
from nineml.xmlns import NINEML, E
import unittest

from nineml.abstraction_layer import connectionrule as cr
from nineml.abstraction_layer.dynamics import DynamicsBlock, regimes
from nineml.abstraction_layer import BaseALObject
from copy import copy, deepcopy
from nineml.abstraction_layer.expressions import (
    Expression, Alias, ExpressionSymbol)

from nineml.abstraction_layer.dynamics.utils.xml import DynamicsClassXMLLoader, DynamicsClassXMLWriter

from nineml import annotations 
from nineml import utils
from nineml.annotations import read_annotations
from nineml.abstraction_layer.units import dimensionless
from nineml.utils import ensure_valid_identifier, expect_single
from nineml.exceptions import NineMLRuntimeError
from nineml.utils import normalise_parameter_as_list
from nineml.utils import filter_discrete_types
from nineml.abstraction_layer.dynamics import DynamicsClass 
from nineml.abstraction_layer.componentclass import ComponentClass, Parameter
from nineml.abstraction_layer.dynamics.utils import DynamicsQueryer
from nineml.utils import (check_list_contain_same_items, invert_dictionary,
                            assert_no_duplicates)

from nineml.abstraction_layer.dynamics.utils.cloner import (
    DynamicsExpandAliasDefinition, DynamicsCloner)
from itertools import chain
from nineml.abstraction_layer.dynamics.validators import DynamicsValidator
from nineml.abstraction_layer.dynamics.utils import DynamicsClassInterfaceInferer
from nineml.abstraction_layer.dynamics.base import _NamespaceMixin
from collections import Counter
from nineml.abstraction_layer.dynamics import TimeDerivative, Regime, StateVariable
from sympy import symbols
import sympy


def inf_check(l1, l2, desc):
    check_list_contain_same_items(l1, l2, desc1='Declared',
                                  desc2='Inferred', ignore=['t'], desc=desc)

#The self argument implies that this method is inside a class.


import nineml.abstraction_layer as al
import os

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

    analog_ports = [al.SendPort("V"), al.ReducePort("Isyn",reduce_op="+")]

    c1 = al.ComponentClass("HodgkinHuxley", 
                          parameters=parameters,
                          regimes=(hh_regime,),
                          aliases=aliases, 
                          analog_ports=analog_ports)
    return c1



def get_component_2():

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
    parameters = ['k', 'mu1', 'mu2', 'sigma1', 'sigma2', 'gkbar', 'gnabar', 'theta', 'gl','celsius', ]


    aliases = [
        "q10 := 3.0**((celsius - 6.3)/10.0)",  # temperature correction factor
     ]

    hh_regime = al.Regime(
        "dn/dt = (ninf-n)/ntau",
        "dm/dt = (minf-m)/mtau",
        "dh/dt = (hinf-h)/htau",
        "dV/dt = (ina + ik + il + Isyn)/C",
        transitions=al.On("V > theta",do=al.SpikeOutputEvent() )
    )

    # the rest are not "parameters" but aliases, assigned vars, state vars, indep vars, analog_analog_ports, etc.
    
    al.AnalogReceivePort
    property_recieve_ports = [al.SendPort("V"), al.ReducePort("Isyn",reduce_op="+")]

    c1 = al.ComponentClass("HodgkinHuxley", 
                          parameters=parameters,
                          regimes=(hh_regime,),
                          aliases=aliases, 
                          analog_ports=analog_ports)
    return c1


class TestConnectionRule(unittest.TestCase):
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

        
        parameters = ['k', 'mu1', 'mu2', 'sigma1', 'sigma2', 'gkbar', 'gnabar', 'theta', 'gl','celsius', ]
        cr.ConnectionRuleClassXMLLoader    
        cr.ConnectionRuleClassXMLWriter
        
        cr.ConnectionRuleClassXMLWriter(
            #subnodes = self._load_blocks(element, blocks=blocks)
            #subnodes = self._load_blocks(element, blocks=subblocks)
            
            #name=element.get('MF2GC'),
            name='MF2GC',
            propertyrecieveport=blocks[""],

            parameters=blocks["Parameter"],
            constant=blocks["Constant"],
            alias=blocks["Alias"],
            select=blocks["Select"]
        )

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

        def get_component():
         
            parameters = ['k', 'mu1', 'sigma1', 'mu2', 'sigma2']
            crc = al.ConnectionRuleClass("",ConnectCondition=["abs(i-j)<= k"] )  #A list of strings.              
            return crc
        
         

        #pass

to=TestConnectionRule()
#to.get_component()
to.test_xml_round_trip()

