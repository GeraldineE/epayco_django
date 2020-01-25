"""
    This module follows the approach Django Rest Framework settings.
    The 'settings.py' file might look like this:
    EPAYCO = {
        'PUBLIC_KEY': '',
        'SECRET_KEY':  '',
        'P_KEY': '',
        'TEST': False # Defaults to true
    }
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse

USER_SETTINGS = getattr(settings, "EPAYCO", None)

if not isinstance(USER_SETTINGS, dict):
    raise ImproperlyConfigured('The ePayco setting is not properly set."')

# List of settings that have a default when a value is not provided by the user.
DEFAULTS = {
    'PUBLIC_KEY': None,
    'PRIVATE_KEY': None,
    'P_KEY': None,
    'TEST': False,
    'CONFIRMATION_URL': 'epayco_confirmation',
    'RESPONSE_URL': 'epayco_response_validation',
    'CHECKOUT_BUTTON_URL': 'https://369969691f476073508a-60bf0867add971908d4f26a64'
                           '519c2aa.ssl.cf5.rackcdn.com/btns/boton_carro_de_compras_epayco5.png'
}

# List of settings that cannot be empty
MANDATORY = (
    'PUBLIC_KEY',
    'PRIVATE_KEY',
    'P_KEY',
)


class EpaycoSettings(object):
    """
        Settings object that allows accessing the ePayco settings as properties.
    """

    def __init__(self, user_settings=None, defaults=None, mandatory=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or {}
        self.mandatory = mandatory or {}

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid ePayco setting: %r" % (attr))

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        if attr in ['CONFIRMATION_URL', 'RESPONSE_URL'] and not attr.startswith('https://'):
            val = reverse(val)

        self.validate_setting(attr, val)
        
        # Cache the result
        setattr(self, attr, val)

        return val

    def validate_setting(self, attr, val):
        if not val and attr in self.mandatory:
            raise ImproperlyConfigured("ePayco setting: '{}' is mandatory".format(attr))


epayco_settings = EpaycoSettings(USER_SETTINGS, DEFAULTS, MANDATORY)
