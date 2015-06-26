"""
docstring needed

:copyright: Copyright 2010-2013 by the Python lib9ML team, see AUTHORS.
:license: BSD-3, see LICENSE for details.
"""
from nineml.annotations import annotate_xml
from nineml.xmlns import E
from nineml.annotations import read_annotations
from ...componentclass.visitors.xml import (
    ComponentClassXMLLoader, ComponentClassXMLWriter)


class ConnectionRuleXMLLoader(ComponentClassXMLLoader):

    """This class is used by XMLReader internally.
    This class loads a NineML XML tree, and stores
    the components in ``components``. It records which file each XML node
    was loaded in from, and stores this in ``component_srcs``.
    """

    @read_annotations
    def load_connectionruleclass(self, element):
        block_names = ('Parameter', 'PropertyReceivePort', 'Constant',
                       'Alias', 'Select')
        blocks = self._load_blocks(element, block_names=block_names)
        return ConnectionRule(
            name=element.attrib['name'],
            propertyrecieveport=blocks["PropertyReceivePort"],
            parameters=blocks["Parameter"],
            constants=blocks["Constant"],
            aliases=blocks["Alias"],
            select=blocks["Select"])

    @read_annotations
    def load_select(self, element):
        block_names = ('Select')
        # elaborate block names for below
        blocks = self.load_blocks(element, block_names=block_names)
        # Fix capitalization
        return Select(
            mask=blocks["Mask"],
            number=blocks["Number"],
            preference=blocks["Preference"],
            selecteds=blocks["Selected"],
            number_selecteds=blocks["NumberSelected"],
            random_variables=blocks["RandomVariables"],
            select=blocks["Select"],
            repeat_untils=blocks["RepeatUntil"])

    tag_to_loader = dict(
        tuple(ComponentClassXMLLoader.tag_to_loader.iteritems()) +
        (("ConnectionRule", load_connectionruleclass),
         ("Select", load_select)))


class ConnectionRuleXMLWriter(ComponentClassXMLWriter):

    @annotate_xml
    def visit_componentclass(self, component_class):
        return E('ConnectionRule',
                 *[e.accept_visitor(self) for e in component_class],
                 name=component_class.name)

    @annotate_xml
    def visit_select(self, select):
        return E.Select(name=select.name)


from ..base import ConnectionRule
from ..select import Select
from nineml.document import Document
