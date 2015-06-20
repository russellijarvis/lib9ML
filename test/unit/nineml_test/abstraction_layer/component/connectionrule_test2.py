#import unittest
import nineml.abstraction_layer as al
from IPython.utils._tokenize_py2 import Number
from nineml.abstraction_layer.connectionrule import *
from nineml.abstraction_layer import connectionrule
#from nineml.base import BaseULObject, resolve_reference, write_reference
#from ..base import NINEML, E
#from .utility import check_tag
#from .components import BaseComponent
#from ..utility import expect_single
from nineml.base import annotate_xml, read_annotations
from nineml.xmlns import NINEML, E

#from nineml..test.unit.nineml_test.abstraction_layer import component
#from al.connectionrule.select import Preference
# from docutils.parsers.rst.directives.misc import Replace
#print al.ConnectionRuleXMLLoader
#import al.connectionrule
# I suspect non of the import statements above because the abstraction directory has been refactored to abstraction.
#al.ConnectionRuleXMLWriter


#from nineml.abstraction_layer import connectionrule
# For some reason ConnectionRuleXMLLoader is not available in XMLLoader
#print ConnectionRuleXMLLoader

#from nineml.abstraction.connectionrule.visitors.xml import ConnectionRuleXMLLoader, ConnectionRuleXMLWriter

from nineml.abstraction_layer import connectionrule as cr
'''
class KineticDynamicsClassXMLLoader(DynamicsClassXMLLoader):
    @read_annotations
    def load_componentclass(self, element):
        #blocks is defined as a list of tuples.x
        blocks = ('Parameter', 'AnalogSendPort', 
        		  'AnalogReceivePort','EventSendPort',
        		  'EventReceivePort', 'AnalogReducePort',
        		  'KineticDynamics')
        
        subnodes = self._load_blocks(element, blocks=blocks)
        kineticsblock 
        = expect_single(subnodes["KineticDynamics"])

        return KineticsDynamicsClass(
            name=element.get('name'),
            parameters=subnodes["Parameter"],
            analog_ports=chain(subnodes["AnalogSendPort"],
                               subnodes["AnalogReceivePort"],
                               subnodes["AnalogReducePort"]),
            event_ports=chain(subnodes["EventSendPort"],
                              subnodes["EventReceivePort"]),
            kineticsblock=kineticsblock)
'''
#The self argument implies that this method is inside a class.

class TestConnectionRule():#unittest.TestCase):
    @read_annotations

    def test_xml_round_trip(self): 
        #write Python objects here.
        #For connection Rules.
        #get_component()
        blocks = ('name','Parameter','Constant','Alias','Select')
        cr.ConnectionRuleClassXMLLoader    
        cr.ConnectionRuleClassXMLWriter(
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


to=TestConnectionRule()
#to.get_component()
to.test_xml_round_trip()

