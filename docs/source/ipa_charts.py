"""
    sphinx.ext.extlinks
    ~~~~~~~~~~~~~~~~~~~
    Extension to save typing and prevent hard-coding of base URLs in the reST
    files.
    This adds a new config value called ``extlinks`` that is created like this::
       extlinks = {'exmpl': ('https://example.invalid/%s.html', caption), ...}
    Now you can use e.g. :exmpl:`foo` in your documents.  This will create a
    link to ``https://example.invalid/foo.html``.  The link caption depends on
    the *caption* value given:
    - If it is ``None``, the caption will be the full URL.
    - If it is a string, it must contain ``%s`` exactly once.  In this case the
      caption will be *caption* with the role content substituted for ``%s``.
    You can also give an explicit caption, e.g. :exmpl:`Foo <foo>`.
    Both, the url string and the caption string must escape ``%`` as ``%%``.
    :copyright: Copyright 2007-2021 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from typing import Any, Dict, List, Tuple

import sphinx
from docutils import nodes, utils
from docutils.nodes import Node, system_message
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from sphinxcontrib.needs.api import add_dynamic_function
from docutils.parsers.rst.states import Inliner
from sphinx.application import Sphinx
from sphinx.util import caption_ref_re
from sphinx.roles import Abbreviation
from sphinx.util.docutils import SphinxDirective
from sphinx_design.icons import FontawesomeRole, fontawesome



class IpaElement(nodes.Element):
    tagname = 'div'
    default_ipa_class = 'ipa'
    def __init__(self, rawsource='', *children, ipa_class='', **attributes):
        if isinstance(ipa_class, str):
            ipa_class = [ipa_class]
        if self.default_ipa_class not in ipa_class:
            ipa_class.insert(0, self.default_ipa_class)
        self.ipa_classes = ipa_class
        self.ipa_classes =[x if x.startswith('ipa') else 'ipa-'+x for x in self.ipa_classes if x]
        super().__init__(rawsource, *children, **attributes)

    def for_html(self):
        return {'class': ' '.join(self.ipa_classes)}

class Divider(IpaElement):
    default_ipa_class = 'divider'
    def __init__(self):
        circle = CircleIcon()
        t = IpaText('',circle)
        super().__init__('', t)

class IpaToolTip(IpaElement):
    default_ipa_class = 'tooltip'

class IpaPhone(IpaElement):
    default_ipa_class = 'phone'
    def __init__(self, phone, extra_data, *children, **attributes):
        ipa_children = [IpaPhoneCheck(phone), IpaPhoneText(phone)]
        #t = IpaText('', nodes.Text(phone))
        #ipa_children.append(t)
        if extra_data:
            tool_tip_childern = []
            for k,v in extra_data.items():
                key = IpaToolTipKey(k)
                if isinstance(v, dict):
                    value = IpaToolTipValue('')
                    line = IpaToolTipLine('', key, value)
                    tool_tip_childern.append(line)
                    for k2, v2 in v.items():
                        key = IpaToolTipKey(k2, second_level=True, ipa_class=['ipa-second-level'])
                        value = IpaToolTipValue(v2,highlight=phone)
                        line = IpaToolTipLine('', key, value)
                        tool_tip_childern.append(line)

                else:
                    value = IpaToolTipValue(v)
                    line = IpaToolTipLine('', key, value)
                    tool_tip_childern.append(line)
            t = IpaToolTip('', *tool_tip_childern)
            ipa_children.append(t)
        super().__init__('', *children, *ipa_children, **attributes)

class IpaText(IpaElement):
    tagname = 'span'
    default_ipa_class = 'text'
    def __init__(self, text, *children, **attributes):
        n = []
        if text:
            n.append(nodes.Text(text))
        super().__init__('', *n, *children, **attributes)

class IpaPhoneCheck(IpaElement):
    tagname = 'input'
    default_ipa_class = 'phone-checkbox'
    def __init__(self, phone, *children, **attributes):
        super().__init__('', *children, **attributes)
        self.phone = phone

    def for_html(self):
        data = super().for_html()
        data.update({'type': 'checkbox', 'ids':[f'{self.phone}_checkbox']})
        return data

class IpaPhoneText(IpaElement):
    tagname = 'label'
    default_ipa_class = 'phone-text'
    def __init__(self, phone, *children, **attributes):
        self.phone = phone
        t = IpaText(phone)
        attributes.update({'for': f'{phone}_checkbox'})
        super().__init__('',t, *children, **attributes)

    def for_html(self):
        data = super().for_html()
        data.update({'for':f'{self.phone}_checkbox'})
        return data

class IpaToolTipLine(IpaElement):
    default_ipa_class = 'tooltip-line'

class IpaToolTipKey(IpaText):
    default_ipa_class = 'tooltip-key'
    def __init__(self, key, *children, second_level=False, **attributes):
        span_children = []
        if second_level:
            span_children.append(nodes.Text('  * '))
            #span_children.append(CircleIcon())
            #span_children.append(nodes.Text(' '))
        key = nodes.Text(f'{key}:')
        span_children.append(key)
        super().__init__('', *children, *span_children, **attributes)

class IpaToolTipValue(IpaElement):
    default_ipa_class = 'tooltip-value'
    def __init__(self, value, *children, highlight=None, **attributes):
        span_children = []
        try:
            value = int(value)
            value = f"{value:,}"
            value = IpaText(value, ipa_class='highlight')
            span_children.append(value)
        except ValueError:
            if highlight is not None:
                highlight_pattern = re.compile(rf'{highlight}[0-5˩˨˧˦˥ˀ]*')
                phones = value[1:-1].split(' ')
                span_children.append(IpaText('[', ipa_class='bracket'))
                for i, p in enumerate(phones):
                    if highlight_pattern.match(p):
                        span_children.append(IpaText(p, ipa_class=['highlight', 'transcription']))
                    else:
                        span_children.append(IpaText(p, ipa_class='transcription'))
                    if i != len(phones) - 1:
                        span_children.append(nodes.Text(' '))
                span_children.append(IpaText(']', ipa_class='bracket'))

        super().__init__('', *children, *span_children, **attributes)


def checkbox_html_visit(self, node):
    """
    Visitor method for Need-node of builder 'html'.
    Does only wrap the Need-content into an extra <div> with class=need
    """
    self.body.append(self.starttag(node, node.tagname, **node.for_html()))

def checkbox_label_html_visit(self, node):
    """
    Visitor method for Need-node of builder 'html'.
    Does only wrap the Need-content into an extra <div> with class=need
    """
    self.body.append(self.starttag(node, node.tagname, **node.for_html()))

def html_visit(self, node):
    """
    Visitor method for Need-node of builder 'html'.
    Does only wrap the Need-content into an extra <div> with class=need
    """
    extra = {}
    if hasattr(node, "for_html"):
        extra = node.for_html()
    self.body.append(self.starttag(node, node.tagname, "",**extra))


def html_depart(self, node):
    self.body.append(f"</{node.tagname}>")

class CircleIcon(nodes.Element):
    tagname = 'i'

    def for_html(self):
        return {'class': 'fas fa-circle ipa-dot'}

class IpaCell(Directive):
    has_content = True

    def run(self):
        if not self.content:
            return [IpaElement(ipa_class='empty')]
        node = nodes.Element()          # anonymous container for parsing
        self.state.nested_parse(self.content, self.content_offset, node)
        output_nodes = []
        manner_type = ''
        for i, row_list in enumerate(node[0]):
            phone_type = row_list[0].children[0].astext()
            phone_type_list = row_list[1]
            phone_type_children = []
            if phone_type in {'voiceless', 'voiced'}:
                manner_type = 'obstruent'
            elif phone_type in {'unrounded', 'rounded'}:
                manner_type = 'vowel'
            else:
                manner_type = 'sonorant'
            for phone_list in phone_type_list:
                phone = phone_list[0].children[0].astext()
                extra_data = {}
                if len(phone_list) > 1:
                    for extra_list in phone_list[1:]:
                        for extra in extra_list:
                            base = extra.children[0].astext()
                            if ':' in base:
                                key, value = base.split(': ')
                                extra_data[key] = value
                            else:
                                extra_data[base] = {}
                                for e in extra.children[1:]:
                                    for c in e.children:
                                        example = c.children[0].astext()
                                        key, value = example.split(': ')
                                        extra_data[base][key] = value

                phone_type_children.append(IpaPhone(phone, extra_data))
            output_nodes.append(IpaElement('',*phone_type_children, ipa_class=phone_type))
            if phone_type in {'voiceless', 'unrounded'}:
                output_nodes.append(Divider())
                if i == len(node[0]) - 1:
                    if phone_type == 'voiceless':
                        output_nodes.append(IpaElement('', ipa_class='voiced'))
                    else:
                        output_nodes.append(IpaElement('', ipa_class='rounded'))
            elif phone_type in {'voiced', 'rounded'} and i == 0:
                output_nodes.insert(0,Divider())
                if phone_type == 'voiced':
                    output_nodes.insert(0,IpaElement('', ipa_class='voiceless'))
                else:
                    output_nodes.insert(0,IpaElement('', ipa_class='unrounded'))

        root_node = IpaElement('', *output_nodes, ipa_class=['cell', manner_type])
        return [root_node]

icon_short_cuts = {
    'right-arrow': 'long-arrow-alt-right'
}

class IpaFontAwesome(FontawesomeRole):
    def __init__(self):
        super(IpaFontAwesome, self).__init__('fas')

    def run(self) -> Tuple[List[nodes.Node], List[nodes.system_message]]:
        """Run the role."""
        icon, classes = self.text.split(";", 1) if ";" in self.text else [self.text, ""]
        icon = icon.strip()
        icon = icon_short_cuts.get(icon, icon)
        node = fontawesome(
            icon=icon, classes=[self.style, f"fa-{icon}", 'ipa-icon'] + classes.split()
        )
        self.set_source_info(node)
        return [node], []


def xref(
    typ: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: dict = None,
    content: List[str] = None,
) -> Tuple[List[Node], List[system_message]]:

    title = target = text
    # look if explicit title and target are given with `foo <bar>` syntax
    brace = text.find("<")
    if brace != -1:
        m = caption_ref_re.match(text)
        if m:
            target = m.group(2)
            title = m.group(1)
        else:
            # fallback: everything after '<' is the target
            target = text[brace + 1 :]
            title = text[:brace]

    link = xref.links[target]

    if brace != -1:
        pnode = nodes.reference(target, title, refuri=link[1])
    else:
        pnode = nodes.reference(target, link[0], refuri=link[1])

    return [pnode], []


def get_refs(app):
    xref.links = app.config.xref_links

def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_config_value("xref_links", {}, "env")
    app.add_node(IpaPhoneCheck, html=(checkbox_html_visit, html_depart))
    app.add_node(IpaPhoneText, html=(checkbox_label_html_visit, html_depart))
    app.add_node(CircleIcon, html=(html_visit, html_depart))
    app.add_node(Divider, html=(html_visit, html_depart))
    app.add_node(IpaToolTip, html=(html_visit, html_depart))
    app.add_node(IpaToolTipKey, html=(html_visit, html_depart))
    app.add_node(IpaToolTipValue, html=(html_visit, html_depart))
    app.add_node(IpaToolTipLine, html=(html_visit, html_depart))
    app.add_node(IpaPhone, html=(html_visit, html_depart))
    app.add_node(IpaElement, html=(html_visit, html_depart))
    app.add_directive("ipa_cell", IpaCell)
    app.add_role("ipa_icon", IpaFontAwesome())
    app.add_role("xref", xref)
    app.connect("builder-inited", get_refs)
    return {"version": sphinx.__display_version__, "parallel_read_safe": True}
