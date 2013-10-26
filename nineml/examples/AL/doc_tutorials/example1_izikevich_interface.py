import nineml.abstraction_layer as al

# (This component will not run, because I & V are undefined:)

# iz = al.ComponentClass(
#    name="IzikevichNeuron",
#    parameters=['a', 'b', 'c', 'd'],
#    event_ports=[al.EventPort('spikeoutput', mode='send')],
#    analog_ports=[al.AnalogPort('I', mode='recv'),
#                  al.AnalogPort('V', mode='send')],
#)
