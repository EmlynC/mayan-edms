"""Configuration options for the bootstrap_theme app"""
from django.utils.translation import ugettext_lazy as _
from smart_settings.api import register_settings

register_settings(
    namespace=u'bootstrap',
    module=u'bootstrap_theme.conf.settings',
    settings=[
        {
            'name': u'THEME',
            'global_name': u'BOOTSTRAP_THEME',
            'default': u'cosmo',
            'description': _(u'CSS theme to apply, options: Default, Cosmo, Flatly, Journal')
        },
        {
             'name': u'ENABLE_SCROLL_JS',
             'global_name': u'BOOTSTRAP_ENABLE_SCROLL_JS',
             'default': True,
             'hidden': True
        },
        {
             'name': u'VERBOSE_LOGIN',
             'global_name': u'BOOTSTRAP_VERBOSE_LOGIN',
             'default': True,
             'description': _(u'Display extra information in the login screen.')
        },
    ]
)
