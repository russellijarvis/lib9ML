import unittest
import nineml.abstraction_layer as al
from IPython.utils._tokenize_py2 import Number
#from nineml.abstraction_layer.connectionrule.select import Preference
# from docutils.parsers.rst.directives.misc import Replace
#print al.ConnectionRuleXMLLoader
#import al.connectionrule
# I suspect non of the import statements above because the abstraction directory has been refactored to abstraction.
#al.ConnectionRuleXMLWriter


#The self argument implies that this method is inside a class.

to=TestConnectionRule()
to.test_xml_roundtrip()             
to.get_component()


class TestConnectionRule(unittest.TestCase):
    def test_xml_round_trip(self): 
        #write Python objects here.
        #For connection Rules.
        get_component()
    
        al.ConnectionRuleXMLWriter
    
        ConnectionRule(
            name=element.get('MF2GC'),
            propertyrecieveport=blocks[""],
            parameters=blocks["Parameter"],
            constant=blocks["Constant"],
            alias=blocks["Alias"],
            select=blocks["Select"]
        )
        
        Select(  
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

        def get_component():
         
            parameters = ['k', 'mu1', 'sigma1', 'mu2', 'sigma2']
            crc = al.ConnectionRuleClass("",ConnectCondition=["abs(i-j)<= k"] )  #A list of strings.              
            return crc
        
            #                              SelectConnections=[]
            #                              
            #                              #Number
            #                              #Preference
            #                              #Replace
            #  
            '''
            al.Regime(
                name="subthresholdregime",
                time_derivatives=[
                    "-g_L*(V-E_L)/C_m + g_L*Delta*exp((V-V_T)/Delta-w/S)/C_m+ Isyn/C_m",
                    "dw/dt = (a*(V-E_L)-w)/tau_w", ],
                transitions=al.On("V > V_T",
                    do=["V = E_L",
                        "w = w + b",
                        al.OutputEvent('spikeoutput')],
                        to="refractoryregime"),
                                 ),
         
                al.Regime(
                    name="refractoryregime",
                    transitions=al.On("t>=tspike+trefractory",
                    to="subthresholdregime"),
                )],
            analog_ports=[al.AnalogReducePort("Isyn", operator="+")]
            )
         
            return crc
            '''
             
         
