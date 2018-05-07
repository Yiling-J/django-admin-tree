# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.admin.templatetags.admin_list import (result_headers,
                                                          result_hidden_fields)
from django.template import Library
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import get_language_bidi

from ..models import TreeNode

try:
    from django.urls import NoReverseMatch
except ImportError:  # Django < 1.10 pragma: no cover
    from django.core.urlresolvers import NoReverseMatch
try:
    from django.utils.deprecation import RemovedInDjango20Warning
except ImportError:
    RemovedInDjango20Warning = RuntimeWarning


register = Library()


def format_path(tree, node, html='', order=0, path_list=[]):
    html += '<li class="dd-item" data-id={} data-order={} data-name={}>'.format(node.id, order, node.title)
    if node.type == 'Root':
        html += '<div class="checkbox"><input class="ignore" type="checkbox"></div>'
        html += '<div class="dd-handle dd-nodrag">{}</div>'.format(node.title + ', ' + node.type)
    else:
        html += '<div class="dd-handle">{}</div>'.format(node.title + ', ' + node.type)
    if node.id not in path_list:
        path_list.append(node.id)
    else:
        return html
    if node.children.filter(tree=tree).exists():
        html += '<ol class="dd-list">'
        for c in node.children.filter(tree=tree):
            html += format_path(tree, c.node_to, '', c.order, path_list)
        html += '</ol>'
        return html
    else:
        html += '</li>'
        return html


def tree_items_for_result(cl, result, form):
    """
    Generates the actual list of data.
    """
    yield format_html(format_path(result, result.start_node, order=0, path_list=[]))


def tree_nodes_for_result(cl, result, form):
    """
    Generates the actual list of data.
    """
    return result.start_node


def tree_results(cl):
    if cl.formset:
        for res, form in zip(cl.result_list, cl.formset.forms):
            yield list(tree_items_for_result(cl, res, form))
    else:
        for res in cl.result_list:
            yield list(tree_items_for_result(cl, res, None))


def nodes_results(cl):
    results = []
    nodes = TreeNode.objects.exclude(type='Root')
    for node in nodes:
        results.append(format_html('<li class="dd-item" data-id={} ><div class="dd-handle node">{}</div></li>'.format(node.id, node.title + ', ' + node.type)))
    return results


def tree_result_list(cl):
    """
    Displays the headers and data list together
    """
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': list(result_headers(cl)),
            'results': list(tree_results(cl)),
            'nodes': nodes_results(cl)}


tree_result_list = register.inclusion_tag(
    "admin/tree_change_list_results.html")(tree_result_list)
