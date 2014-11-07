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
        'basket': 'shopping-cart',
        'cog': 'cog',
        'folder_user': 'folder-open',
        'house': 'home',
        'information': 'info-sign',
        'page':  'file',
        'tab': 'credit-card',
        'tag_blue': 'tags',
        'user': 'user',
        'wrench': 'wrench',
        'zoom':  'search',
        'page_add': 'plus',
        'tag_blue_add': 'plus',
        'telephone': 'earphone',
        'script': 'book',
        'xhtml_add': 'plus',
        'xhtml_go': 'pencil',
        'xhtml_go': 'pencil',
        'xhtml_delete': 'minus',
        'hourglass_add': 'tasks',
        'tag_blue_add': 'plus',
        'tag_blue_delete': 'minus',
        'folder_add': 'plus',
        'page_paintbrush':'remove',
        'page_delete':'trash',
        'page_save': 'download',
        'zoom_in': 'search',
    }

    if famfam in mapper.keys():
        return mapper[famfam]
    else:
        return ''