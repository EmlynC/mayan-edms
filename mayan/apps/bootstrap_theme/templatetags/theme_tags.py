from __future__ import absolute_import

import re

from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError
from django.utils.safestring import mark_safe

from ..conf import settings as bootstrap_theme_settings

register = Library()


class GetThemeNode(Node):
    def __init__(self, var_name, *args):
        self.var_name = var_name

    def render(self, context):
        context['bootstrap_theme'] = bootstrap_theme_settings.THEME
        context['enable_scroll_js'] = bootstrap_theme_settings.ENABLE_SCROLL_JS
        return ''


@register.tag
def get_theme(parser, token):
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError('%r tag requires arguments' % token.contents.split()[0])

    m = re.search(r'as (\w+)', arg)
    if not m:
        raise TemplateSyntaxError('%r tag had invalid arguments' % tag_name)
    var_name = m.groups()

    return GetThemeNode(var_name)


class LoginRedirectNode(Node):
    def render(self, context):
        context['LOGIN_REDIRECT_URL'] = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
        return ''


@register.tag
def get_login_redirect_url(parser, token):
    return LoginRedirectNode()


class SettingsNode(Node):
    def __init__(self, format_string, var_name):
        self.format_string = format_string
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = getattr(bootstrap_theme_settings, self.format_string, '')
        return ''


@register.tag
def get_bootstrap_theme_setting(parser, token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError('%r tag requires arguments' % token.contents.split()[0])
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise TemplateSyntaxError('%r tag had invalid arguments' % tag_name)
    format_string, var_name = m.groups()
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise TemplateSyntaxError('%r tag\'s argument should be in quotes' % tag_name)
    return SettingsNode(format_string[1:-1], var_name)


@register.filter
def highlight(text, word):
    return mark_safe(unicode(text).replace(word, mark_safe('<mark>%s</mark>' % word)))

@register.filter
def convert_to_glyphicon(famfam):
    """
    Given a famfam name return a glyphicon equivalent
    :param famfam:
    :return:
    """

    # let the empties forward to default
    if famfam is '':
        return ''

    mapper = {
        'basket':           'shopping-cart',
        'book_go':          'book',
        'camera_delete':    'camera',
        'chart_curve_go':   'signal',
        'cog':              'cog',
        'comments':         'comment',
        'control_play_blue': 'play',
        'control_stop_blue': 'stop',
        'folder_add':       'plus',
        'folder_delete':    'minus',
        'folder_edit':      'pencil',
        'folder_go':        'folder-open',
        'folder_page':      'credit-card',
        'folder_user':      'folder-open',
        'hourglass':        'tasks',
        'hourglass_add':    'tasks',
        'house':            'home',
        'information':      'info-sign',
        'key':              'transfer',
        'lightning':        'flash',
        'link':             'link',
        'link_add':         'plus',
        'lock':             'lock',
        'lock_go':          'lock',
        'medal_gold_add':   'plus',
        'package':          'list',
        'page':             'file',
        'page_add':         'plus',
        'page_copy':        'th-list',
        'page_delete':      'trash',
        'page_edit':        'pencil',
        'page_gear':        'cog',
        'page_link':        'link',
        'page_paintbrush':  'remove',
        'page_save':        'download',
        'page_white_copy':  'record',
        'page_white_csharp': 'bookmark',
        'page_world':       'globe',
        'printer':          'print',
        'script':           'book',
        'signature':        'barcode',
        'tab':              'credit-card',
        'table':            'th',
        'table_add':        'plus',
        'tag_blue':         'tags',
        'tag_blue_add':     'plus',
        'tag_blue_delete':  'minus',
        'tag_blue_edit':    'pencil',
        'telephone':        'earphone',
        'text_strikethrough': 'text-height',
        'user':             'user',
        'wrench':           'wrench',
        'xhtml_add':        'plus',
        'xhtml_delete':     'minus',
        'xhtml_go':         'pencil',
        'zoom':             'search',
        'zoom_in':          'search',
    }

    if famfam in mapper.keys():
        return mapper[famfam]
    else:
        return ''