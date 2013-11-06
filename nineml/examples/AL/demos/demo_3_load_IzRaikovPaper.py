import nineml 

iz_comp = nineml.abstraction_layer.readers.XMLReader.read_component('../../../../../../catalog/sample_xml_files/IzhikevichFS_AL.xml')
print iz_comp
nineml.al.writers.DotWriter.write(iz_comp, 'TestOut_Iz.dot')
nineml.al.writers.DotWriter.build('TestOut_Iz.dot')






