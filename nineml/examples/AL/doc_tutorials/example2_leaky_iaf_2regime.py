import nineml.abstraction_layer as al
r1 = al.Regime(
    name="sub_threshold_regime",
    time_derivatives=["dV/dt = (-gL*(V-vL) + I)/C", ],
    transitions=[al.On("V>Vth",
                       do=["tspike = t",
                           "V = V_reset",
                           al.OutputEvent('spike')],
                 to="refractory_regime"), ],
)

r2 = al.Regime(name="refractory_regime",
               transitions=[al.On("t >= tspike + trefractory",
                                  to="sub_threshold_regime"), ],
               )

leaky_iaf = al.ComponentClass(
                "LeakyIAF",
                dynamics=al.Dynamics(
                    regimes=[r1, r2],
                    state_variables=['V', 'tspike'],
                    ),
                analog_ports=[al.AnalogPort("I", mode='recv')],
                parameters=['C', 'V_reset', 'Vth', 'gL', 'trefractory', 'vL'],
                )


leaky_iaf.write("leaky_iaf.xml")
