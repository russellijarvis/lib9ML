"""
Definitions for the DynamicsClass. DynamicsClass derives from 2 other mixin
classes, which provide functionality for hierachical components and for local
components definitions of interface and dynamics

:copyright: Copyright 2010-2013 by the Python lib9ML team, see AUTHORS.
:license: BSD-3, see LICENSE for details.
"""
import itertools
from ...exceptions import NineMLRuntimeError
from ..base import NamespaceAddress

from ...utility import normalise_parameter_as_list, filter_discrete_types
from itertools import chain
from ..expressions import Alias
from ..base import ComponentClass, Parameter
from .regimes import StateVariable
from ..ports import (AnalogReceivePort, AnalogSendPort,
                     AnalogReducePort, EventReceivePort,
                     EventSendPort)
from nineml.utility import (check_list_contain_same_items,
                            ensure_valid_identifier, invert_dictionary,
                            assert_no_duplicates)
from ..expressions.util import get_reserved_and_builtin_symbols
from ..base.utils.cloner import ExpandAliasDefinition, ClonerVisitor
from .. import BaseALObject
from ..base.utils.visitors import ActionVisitor
from ..base.utils.queryer import Queryer


class _FlatMixin(object):

    """Mixin Class that provides the infrastructure for *local* component
    definitions - i.e. the dynamics
    """

    def __init__(self, analog_ports=[],
                 event_ports=[], dynamics=None):
        """Constructor - For parameter descriptions, see the
        DynamicsClass.__init__() method
        """
        self._analog_send_ports = dict((port.name, port)
                                       for port in analog_ports
                                       if isinstance(port, AnalogSendPort))
        self._analog_receive_ports = dict((port.name, port)
                                          for port in analog_ports
                                          if isinstance(port,
                                                        AnalogReceivePort))
        self._analog_reduce_ports = dict((port.name, port)
                                         for port in analog_ports
                                         if isinstance(port, AnalogReducePort))
        self._event_send_ports = dict((port.name, port)
                                      for port in event_ports
                                      if isinstance(port, EventSendPort))
        self._event_receive_ports = dict((port.name, port)
                                         for port in event_ports
                                         if isinstance(port, EventReceivePort))
        self._dynamics = dynamics
        ensure_valid_identifier(self.name)

    @property
    def ports(self):
        return chain(self.analog_send_ports, self.analog_receive_ports,
                     self.analog_reduce_ports, self.event_send_ports,
                     self.event_receive_ports)

    @property
    def analog_send_ports(self):
        """Returns an iterator over the local |AnalogSendPort| objects"""
        return self._analog_send_ports.itervalues()

    @property
    def analog_receive_ports(self):
        """Returns an iterator over the local |AnalogReceivePort| objects"""
        return self._analog_receive_ports.itervalues()

    @property
    def analog_reduce_ports(self):
        """Returns an iterator over the local |AnalogReducePort| objects"""
        return self._analog_reduce_ports.itervalues()

    @property
    def analog_ports(self):
        """Returns an iterator over the local analog port objects"""
        return chain(self.analog_send_ports, self.analog_receive_ports,
                     self.analog_reduce_ports)

    @property
    def event_send_ports(self):
        """Returns an iterator over the local |EventSendPort| objects"""
        return self._event_send_ports.itervalues()

    @property
    def event_receive_ports(self):
        """Returns an iterator over the local |EventReceivePort| objects"""
        return self._event_receive_ports.itervalues()

    @property
    def event_ports(self):
        return chain(self.event_send_ports, self.event_receive_ports)

    @property
    def dynamics(self):
        """Returns the local |Dynamics| object"""
        return self._dynamics
    # -------------------------- #

    def __repr__(self):
        return "<dynamics.DynamicsClass %s>" % self.name

    # Forwarding functions to the dynamics #

    @property
    def aliases(self):
        """Forwarding function to self.dynamics.aliases"""
        return self._dynamics.aliases

    @property
    def regimes(self):
        """Forwarding function to self.dynamics.regimes"""
        return self._dynamics.regimes

    @property
    def regimes_map(self):
        """Forwarding function to self.dynamics.regimes_map"""
        return self._dynamics.regimes_map

    @property
    def transitions(self):
        """Forwarding function to self.dynamics.transitions"""
        return self._dynamics.transitions

    @property
    def state_variables(self):
        """Forwarding function to self.dynamics.state_variables"""
        return self._dynamics.state_variables

    @property
    def analog_send_ports_map(self):
        """
        Returns the underlying dictionary containing the AnalogSendPort
        objects
        """
        return self._analog_send_ports

    @property
    def analog_receive_ports_map(self):
        """
        Returns the underlying dictionary containing the AnalogReceivePort
        objects
        """
        return self._analog_receive_ports

    @property
    def analog_reduce_ports_map(self):
        """
        Returns the underlying dictionary containing the AnalogReducePort
        objects
        """
        return self._analog_reduce_ports

    @property
    def event_send_ports_map(self):
        """
        Returns the underlying dictionary containing the EventSendPort
        objects
        """
        return self._event_send_ports

    @property
    def event_receive_ports_map(self):
        """
        Returns the underlying dictionary containing the EventReceivePort
        objects
        """
        return self._event_receive_ports

    @property
    def aliases_map(self):
        """Forwarding function to self.dynamics.alias_map"""
        return self._dynamics.aliases_map

    @property
    def state_variables_map(self):
        """Forwarding function to self.dynamics.state_variables_map"""
        return self._dynamics.state_variables_map

    @property
    def _attributes_with_dimension(self):
        return chain(self.analog_ports, self.parameters, self.state_variables)

    # -------------------------- #

    def backsub_all(self):
        """Expand all alias definitions in local equations.

        This function finds |Aliases|, |TimeDerivatives|, *send* |AnalogPorts|,
        |StateAssignments| and |Conditions| which are defined in terms of other
        |Aliases|, and expands them, such that each only has |Parameters|,
        |StateVariables| and recv/reduce |AnalogPorts| on the RHS.

        """

        for alias in self.aliases:
            alias_expander = ExpandAliasDefinition(originalname=alias.lhs,
                                                   targetname=("(%s)" %
                                                               alias.rhs))
            alias_expander.visit(self)

    def write(self, file, flatten=True):  # @ReservedAssignment
        """Export this model to an XML file.

        :params file: A filename or fileobject
        :params flatten: Boolean specifying whether the component should be
            flattened before saving

        """
        from nineml.abstraction_layer.dynamics.utils.xml import XMLWriter
        return XMLWriter.write(component=self, file=file, flatten=flatten)


class _NamespaceMixin(object):

    """ A mixin class that provides the hierarchical structure for
    (sub) components.
    """

    def __init__(self, subnodes=None, portconnections=None):
        """Constructor - For parameter descriptions, see the
        DynamicsClass.__init__() method
        """

        # Prevent dangers with default arguments.
        subnodes = subnodes or {}
        portconnections = portconnections or []

        # Initialise class variables:
        self._parentmodel = None
        self.subnodes = {}
        self._portconnections = []

        # Add the parameters using class methods:
        for namespace, subnode in subnodes.iteritems():
            self.insert_subnode(subnode=subnode, namespace=namespace)

        for src, sink in portconnections:
            self.connect_ports(src, sink)

    # Parenting:
    def set_parent_model(self, parentmodel):
        """Sets the parent component for this component"""
        assert not self._parentmodel
        self._parentmodel = parentmodel

    def get_parent_model(self):
        """Gets the parent component for this component"""
        return self._parentmodel

    def _validate_self(self):
        """ Over-ridden in mix'ed class"""
        raise NotImplementedError()

    def get_node_addr(self):
        """Get the namespace address of this component"""
        parent = self.get_parent_model()
        if not parent:
            return NamespaceAddress.create_root()
        else:
            contained_namespace = invert_dictionary(parent.subnodes)[self]
            return parent.get_node_addr().get_subns_addr(contained_namespace)

    def get_subnode(self, addr):
        """Gets a subnode from this component recursively."""
        namespace_addr = NamespaceAddress(addr)

        # Look up the first name in the namespace
        if len(namespace_addr.loctuple) == 0:
            return self

        local_namespace_ref = namespace_addr.loctuple[0]
        if local_namespace_ref not in self.subnodes:
            err = "Attempted to lookup node: %s\n" % local_namespace_ref
            err += "Doesn't exist in this namespace: %s" % self.subnodes.keys()
            raise NineMLRuntimeError(err)

        subnode = self.subnodes[local_namespace_ref]
        addr_in_subnode = NamespaceAddress(namespace_addr.loctuple[1:])
        return subnode.get_subnode(addr=addr_in_subnode)

    def insert_subnode(self, namespace, subnode):
        """Insert a subnode into this component

        :param subnode: An object of type ``DynamicsClass``.
        :param namespace: A `string` specifying the name of the component in
            this components namespace.

        :raises: ``NineMLRuntimeException`` if there is already a subcomponent
                  at the same namespace location

        .. note::

            This method will clone the subnode.

        """
        if not isinstance(namespace, basestring):
            err = 'Invalid namespace: %s' % type(subnode)
            raise NineMLRuntimeError(err)

        if not isinstance(subnode, DynamicsClass):
            err = 'Attempting to insert invalid '
            err += 'object as subcomponent: %s' % type(subnode)
            raise NineMLRuntimeError(err)

        if namespace in self.subnodes:
            err = 'Key already exists in namespace: %s' % namespace
            raise NineMLRuntimeError(err)
        self.subnodes[namespace] = ClonerVisitor().visit(subnode)
        self.subnodes[namespace].set_parent_model(self)

        self._validate_self()

    def connect_ports(self, src, sink):
        """Connects the ports of 2 subcomponents.

        The ports can be specified as ``string`` s or |NamespaceAddresses|.


        :param src: The source port of one sub-component; this should either an
            |EventPort| or |AnalogPort|, but it *must* be a send port.

        :param sink: The sink port of one sub-component; this should either an
            |EventPort| or |AnalogPort|, but it *must* be either a 'recv' or a
            'reduce' port.

        """

        connection = (NamespaceAddress(src), NamespaceAddress(sink))
        self._portconnections.append(connection)

        self._validate_self()

    @property
    def portconnections(self):
        return self._portconnections


class InterfaceInferer(ActionVisitor):

    """ Used to infer output |EventPorts|, |StateVariables| & |Parameters|."""

    def __init__(self, dynamics, incoming_port_names):
        ActionVisitor.__init__(self, require_explicit_overrides=True)

        # State Variables:
        self.state_variable_names = set()
        for regime in dynamics.regimes:
            for time_deriv in regime.time_derivatives:
                self.state_variable_names.add(time_deriv.dependent_variable)
            for transition in regime.transitions:
                for state_assignment in transition.state_assignments:
                    self.state_variable_names.add(state_assignment.lhs)

        # Which symbols can we account for:
        self.accounted_for_symbols = set(itertools.chain(
            self.state_variable_names,
            dynamics.aliases_map.keys(),
            # dynamics.constants_map.keys(),  # TODO: Need to add this
            # dynamics.random_variables_map.keys(),
            incoming_port_names,
            get_reserved_and_builtin_symbols()
        ))

        # Parameters:
        # Use visitation to collect all atoms that are not aliases and not
        # state variables

        self.free_atoms = set()
        self.input_event_port_names = set()
        self.output_event_port_names = set()

        self.visit(dynamics)

        self.free_atoms -= self.input_event_port_names
        self.free_atoms -= self.output_event_port_names
        self.parameter_names = self.free_atoms

    def action_dynamics(self, dynamics, **kwargs):
        pass

    def action_regime(self, regime, **kwargs):
        pass

    def action_statevariable(self, state_variable, **kwargs):
        pass

    def _notify_atom(self, atom):
        if atom not in self.accounted_for_symbols:
            self.free_atoms.add(atom)

    # Events:
    def action_eventout(self, output_event, **kwargs):  # @UnusedVariable
        self.output_event_port_names.add(output_event.port_name)

    def action_onevent(self, on_event, **kwargs):  # @UnusedVariable
        self.input_event_port_names.add(on_event.src_port_name)

    # Atoms (possible parameters):
    def action_assignment(self, assignment, **kwargs):  # @UnusedVariable
        for atom in assignment.rhs_atoms:
            self._notify_atom(atom)

    def action_alias(self, alias, **kwargs):  # @UnusedVariable
        for atom in alias.rhs_atoms:
            self._notify_atom(atom)

    def action_timederivative(self, time_derivative, **kwargs):  # @UnusedVariable @IgnorePep8
        for atom in time_derivative.rhs_atoms:
            self._notify_atom(atom)

    def action_condition(self, condition, **kwargs):  # @UnusedVariable
        for atom in condition.rhs_atoms:
            self._notify_atom(atom)

    def action_oncondition(self, on_condition, **kwargs):
        pass


class DynamicsClass(ComponentClass, _FlatMixin, _NamespaceMixin):

    """A DynamicsClass object represents a *component* in NineML.

      .. todo::

         For more information, see

    """
    defining_attributes = ('name', '_parameters', '_analog_send_ports',
                           '_analog_receive_ports', '_analog_reduce_ports',
                           '_event_send_ports', '_event_receive_ports',
                           'dynamics')

    writer_name = 'dynamics'

    def __init__(self, name, parameters=None, analog_ports=[],
                 event_ports=[],
                 dynamics=None, subnodes=None,
                 portconnections=None, regimes=None,
                 aliases=None, state_variables=None):
        """Constructs a DynamicsClass

        :param name: The name of the component.
        :param parameters: A list containing either |Parameter| objects
            or strings representing the parameter names. If ``None``, then the
            parameters are automatically inferred from the |Dynamics| block.
        :param analog_ports: A list of |AnalogPorts|, which will be the
            local |AnalogPorts| for this object.
        :param event_ports: A list of |EventPorts| objects, which will be the
            local event-ports for this object. If this is ``None``, then they
            will be automatically inferred from the dynamics block.
        :param dynamics: A |Dynamics| object, defining the local dynamics of
                         the component.
        :param subnodes: A dictionary mapping namespace-names to sub-component.
            [Type: ``{string:|DynamicsClass|, string:|DynamicsClass|,
            string:|DynamicsClass|}`` ] describing the namespace of
            subcomponents for this component.
        :param portconnections: A list of pairs, specifying the connections
            between the ports of the subcomponents in this component. These can
            be `(|NamespaceAddress|, |NamespaceAddress|)' or ``(string,
            string)``.
        :param interface: A shorthand way of specifying the **interface** for
            this component; |Parameters|, |AnalogPorts| and |EventPorts|.
            ``interface`` takes a list of these objects, and automatically
            resolves them by type into the correct types.

        Examples:

        >>> a = DynamicsClass(name='MyComponent1')

        .. todo::

            Point this towards and example of constructing ComponentClasses.
            This can't be here, because we also need to know about dynamics.
            For examples

        """
        ComponentClass.__init__(self, name, parameters)
        # We can specify in the componentclass, and they will get forwarded to
        # the dynamics class. We check that we do not specify half-and-half:
        if dynamics is not None:
            if regimes or aliases or state_variables:
                err = "Either specify a 'dynamics' parameter, or "
                err += "state_variables /regimes/aliases, but not both!"
                raise NineMLRuntimeError(err)

        else:
            dynamics = Dynamics(regimes=regimes,
                                    aliases=aliases,
                                    state_variables=state_variables)
        self._query = Queryer(self)

        # Ensure analog_ports is a list not an iterator
        analog_ports = list(analog_ports)
        event_ports = list(event_ports)

        # Check there aren't any duplicates in the port and parameter names
        assert_no_duplicates(p if isinstance(p, basestring) else p.name
                             for p in chain(parameters if parameters else [],
                                            analog_ports,
                                            event_ports))

        analog_receive_ports = [port for port in analog_ports
                                if isinstance(port, AnalogReceivePort)]
        analog_reduce_ports = [port for port in analog_ports
                               if isinstance(port, AnalogReducePort)]
        incoming_port_names = [p.name for p in chain(analog_receive_ports,
                                                     analog_reduce_ports)]
        # EventPort, StateVariable and Parameter Inference:
        inferred_struct = InterfaceInferer(dynamics, incoming_port_names)
        inf_check = lambda l1, l2, desc: check_list_contain_same_items(
            l1, l2, desc1='Declared', desc2='Inferred', ignore=['t'],
            desc=desc)

        # Check any supplied parameters match:
        if parameters is not None:
            inf_check(self._parameters.keys(),
                      inferred_struct.parameter_names,
                      'Parameters')
        else:
            self._parameters = dict((n, Parameter(n))
                                    for n in inferred_struct.parameter_names)

        # Check any supplied state_variables match:
        if dynamics._state_variables:
            state_var_names = [p.name for p in dynamics.state_variables]
            inf_check(state_var_names,
                      inferred_struct.state_variable_names,
                      'StateVariables')
        else:
            state_vars = dict((n, StateVariable(n)) for n in
                              inferred_struct.state_variable_names)
            dynamics._state_variables = state_vars

        # Check Event Receive Ports Match:
        event_receive_ports = [port for port in event_ports
                               if isinstance(port, EventReceivePort)]
        event_send_ports = [port for port in event_ports
                            if isinstance(port, EventSendPort)]
        if event_receive_ports:
            # FIXME: not all OutputEvents are necessarily exposed as Ports,
            # so really we should just check that all declared output event
            # ports are in the list of inferred ports, not that the declared
            # list is identical to the inferred one.
            inf_check([p.name for p in event_receive_ports],
                      inferred_struct.input_event_port_names,
                      'Event Ports In')

        # Check Event Send Ports Match:
        if event_send_ports:
            inf_check([p.name for p in event_send_ports],
                      inferred_struct.output_event_port_names,
                      'Event Ports Out')
        else:
            event_ports = []
            # Event ports not supplied, so lets use the inferred ones.
            for evt_port_name in inferred_struct.input_event_port_names:
                event_ports.append(EventReceivePort(name=evt_port_name))
            for evt_port_name in inferred_struct.output_event_port_names:
                event_ports.append(EventSendPort(name=evt_port_name))

        # Construct super-classes:
        _FlatMixin.__init__(
            self, analog_ports=analog_ports, event_ports=event_ports,
            dynamics=dynamics)
        _NamespaceMixin.__init__(
            self, subnodes=subnodes, portconnections=portconnections)

        # Finalise initiation:
        self._resolve_transition_regime_names()

        # Store flattening Information:
        self._flattener = None

        # Is the finished component valid?:
        self._validate_self()

    @property
    def flattener(self):
        """
        If this component was made by flattening other components, return the
        |ComponentFlattener| object. This is useful for finding initial-regimes
        """
        return self._flattener

    def set_flattener(self, flattener):
        """Specifies the flattening object used to create this component, if
        this component was flattened from a hierarchical component"""
        if not flattener:
            raise NineMLRuntimeError('Setting flattener to None??')
        if self.flattener:
            raise NineMLRuntimeError('Trying to change flattener')
        self._flattener = flattener

    def was_flattened(self):
        """Returns ``True`` if this component was created by flattening another
        component"""
        return self.flattener is not None

    def _validate_self(self):
        ComponentValidator.validate_componentclass(self)

    @property
    def query(self):
        """ Returns the ``ComponentQuery`` object associated with this class"""
        return self._query

    def is_flat(self):
        """Is this component flat or does it have subcomponents?

        Returns a ``Boolean`` specifying whether this component is flat; i.e.
        has no subcomponent
        """

        return len(self.subnodes) == 0

    def accept_visitor(self, visitor, **kwargs):
        """ |VISITATION| """
        return visitor.visit_componentclass(self, **kwargs)

    def _resolve_transition_regime_names(self):
        # Check that the names of the regimes are unique:
        names = [r.name for r in self.regimes]
        assert_no_duplicates(names)

        # Create a map of regime names to regimes:
        regime_map = dict([(r.name, r) for r in self.regimes])

        # We only worry about 'target' regimes, since source regimes are taken
        # care of for us by the Regime objects they are attached to.
        for trans in self.transitions:
            if trans.target_regime_name not in regime_map:
                errmsg = "Can't find regime: %s" % trans.target_regime_name
                raise NineMLRuntimeError(errmsg)
            trans.set_target_regime(regime_map[trans.target_regime_name])

    @property
    def _attributes_with_dimension(self):
        return chain(self.parameters, self.analog_ports, self.state_variables)


class Dynamics(BaseALObject):

    """
    An object, which encapsulates a component's regimes, transitions,
    and state variables
    """

    defining_attributes = ('_regimes', '_aliases', '_state_variables')

    def __init__(self, regimes=None, aliases=None, state_variables=None):
        """Dynamics object constructor

           :param aliases: A list of aliases, which must be either |Alias|
               objects or ``string``s.
           :param regimes: A list containing at least one |Regime| object.
           :param state_variables: An optional list of the state variables,
                which can either be |StateVariable| objects or `string` s. If
                provided, it must match the inferred state-variables from the
                regimes; if it is not provided it will be inferred
                automatically.
        """

        aliases = normalise_parameter_as_list(aliases)
        regimes = normalise_parameter_as_list(regimes)
        state_variables = normalise_parameter_as_list(state_variables)

        # Load the aliases as objects or strings:
        alias_td = filter_discrete_types(aliases, (basestring, Alias))
        aliases_from_strs = [Alias.from_str(o) for o in alias_td[basestring]]
        aliases = alias_td[Alias] + aliases_from_strs

        # Load the state variables as objects or strings:
        sv_types = (basestring, StateVariable)
        sv_td = filter_discrete_types(state_variables, sv_types)
        sv_from_strings = [StateVariable(o, dimension=None)
                           for o in sv_td[basestring]]
        state_variables = sv_td[StateVariable] + sv_from_strings

        assert_no_duplicates(r.name for r in regimes)
        assert_no_duplicates(a.lhs for a in aliases)
        assert_no_duplicates(s.name for s in state_variables)

        self._regimes = dict((r.name, r) for r in regimes)
        self._aliases = dict((a.lhs, a) for a in aliases)
        self._state_variables = dict((s.name, s) for s in state_variables)

    def accept_visitor(self, visitor, **kwargs):
        """ |VISITATION| """
        return visitor.visit_dynamics(self, **kwargs)

    def __repr__(self):
        return ('Dynamics({} regimes, {} aliases, {} state-variables)'
                .format(len(list(self.regimes)), len(list(self.aliases)),
                        len(list(self.state_variables))))

    @property
    def regimes(self):
        return self._regimes.itervalues()

    @property
    def regimes_map(self):
        return self._regimes

    @property
    def transitions(self):
        return chain(*[r.transitions for r in self.regimes])

    @property
    def aliases(self):
        return self._aliases.itervalues()

    @property
    def aliases_map(self):
        return self._aliases

    @property
    def state_variables(self):
        return self._state_variables.itervalues()

    @property
    def state_variables_map(self):
        return self._state_variables

from .validators import ComponentValidator
