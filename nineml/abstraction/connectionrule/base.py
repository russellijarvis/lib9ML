#!/usr/bin/env python
"""
docstring goes here

.. module:: connection_generator.py
   :platform: Unix, Windows
   :synopsis:

.. moduleauthor:: Mikael Djurfeldt <mikael.djurfeldt@incf.org>
.. moduleauthor:: Dragan Nikolic <dnikolic@incf.org>

:copyright: Copyright 2010-2013 by the Python lib9ML team, see AUTHORS.
:license: BSD-3, see LICENSE for details.
"""
from ..componentclass import ComponentClass
from nineml.annotations import annotate_xml, read_annotations
from nineml.abstraction.ports import PropertyReceivePort


class ConnectionRule(ComponentClass):

    element_name = 'ConnectionRule'
    defining_attributes = ('name', '_parameters', '_select', '_constants',
                           '_aliases', '_property_receive_ports', '_property_receive_port')
   
    #class_to_member_dict = {PropertyReceivePorts: '_property_receive_ports'}
    #class_to_member_dict = {PropertyReceivePort: '_property_receive_port'}

    def __init__(self, name, select, parameters=None, constants=None,
                 aliases=None):
        super(ConnectionRule, self).__init__(
            name=name, parameters=parameters, aliases=aliases,
            constants=constants)
        self._select = select

    @property
    def select(self):
        return self._select

    @property
    def property_receive_ports(self):
        return self._property_receive_ports.itervalues()

    @property
    def property_receive_port_names(self):
        return self._property_receive_ports.iterkeys()

    #This method is actually more correct than one below.
    #maybe the attribute does not exist because _property_recieve_ports never exists.
    @property
    def property_receive_port(self, name):
        return self._property_receive_ports[name]


    #@property
    #def property_receive_port(self):#, name):
    #    return self._property_receive_port.itervalues()

    @property
    def selects(self):
        """
        Iterate through nested select statements
        """
        select = self._select
        yield select
        if select.select is not None:
            select = self._select
            yield select
        else:
            raise StopIteration

    def accept_visitor(self, visitor, **kwargs):
        """ |VISITATION| """
        return visitor.visit_componentclass(self, **kwargs)

    def __copy__(self, memo=None):  # @UnusedVariable
        return ConnectionRuleCloner().visit(self)

    def rename_symbol(self, old_symbol, new_symbol):
        ConnectionRuleRenameSymbol(self, old_symbol, new_symbol)

    def assign_indices(self):
        ConnectionRuleAssignIndices(self)

    def required_for(self, expressions):
        return ConnectionRuleRequiredDefinitions(self, expressions)

    def _find_element(self, element):
        return ConnectionRuleElementFinder(element).found_in(self)

    def validate(self):
        ConnectionRuleValidator.validate_componentclass(self)

    @property
    def all_expressions(self):
        extractor = ConnectionRuleExpressionExtractor()
        extractor.visit(self)
        return extractor.expressions

    @annotate_xml
    def to_xml(self):
        self.standardize_unit_dimensions()
        self.validate()
        return ConnectionRuleXMLWriter().visit(self)

    @classmethod
    @read_annotations
    def from_xml(cls, element, document):
        return ConnectionRuleXMLLoader(document).load_connectionruleclass(
            element)


    # Parenting:
    def set_parent_model(self, parentmodel):
        """Sets the parent component for this component"""
        assert not self._parentmodel
        self._parentmodel = parentmodel

    def get_parent_model(self):
        """Gets the parent component for this component"""
        return self._parentmodel

    #def validate(self):
    #    """ Over-ridden in mix'ed class"""
    #    raise NotImplementedError()
    
    
    def validate(self):
        pass
        #self._resolve_transition_regimes()
        #DynamicsValidator.validate_componentclass(self)

    def get_node_addr(self):
        """Get the namespace address of this component"""
        parent = self.get_parent_model()
        if not parent:
            return NamespaceAddress.create_root()
        else:
            contained_namespace = invert_dictionary(parent.subnodes)[self]
            return parent.get_node_addr().get_subns_addr(contained_namespace)




from .visitors.cloner import ConnectionRuleCloner
from .visitors.modifiers import (
    ConnectionRuleRenameSymbol, ConnectionRuleAssignIndices)
from .visitors.queriers import (
    ConnectionRuleRequiredDefinitions, ConnectionRuleElementFinder,
    ConnectionRuleExpressionExtractor)
from .visitors.validators import ConnectionRuleValidator
from .visitors.xml import (
    ConnectionRuleXMLLoader, ConnectionRuleXMLWriter)
