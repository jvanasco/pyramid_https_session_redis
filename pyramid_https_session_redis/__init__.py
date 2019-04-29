# pypi
from pyramid.settings import asbool
import pyramid_https_session_core
import pyramid_session_redis


# ==============================================================================

__VERSION__ = '0.2.1'

# ==============================================================================


class RedisConfigurator(pyramid_https_session_core.SessionBackendConfigurator):

    # used to ensure compatibility
    compatibility_options = {'key': 'cookie_name',
                             'domain': 'cookie_domain',
                             'path': 'cookie_path',
                             'secure': 'cookie_secure',
                             'set_on_exception': 'cookie_on_exception',
                             'httponly': 'cookie_httponly',
                             }


def initialize_https_session_support(config, settings, prefix_selected=None, register_factory=True):
    """
    Parses config settings, builds a https session factory, optionally registers it, returns it

    Params:
        `config`: pyramid config
        `settings`: pyramid settings
        `prefix_selected=None`: if specified, will only parse this prefix
        `register_factory=True`: if `True`, will register the factory. If not true, the factory must be registered

    Returns:
        this returns the generated factory
    """
    https_options = {}
    https_prefixes = ('session_https.',
                      'redis.sessions_https.',
                      )
    if prefix_selected:
        https_prefixes = (prefix_selected, )
    for k, v in settings.items():
        for prefix in https_prefixes:
            # only worry about our prefix
            if k.startswith(prefix):
                option_name = k[len(prefix):]
                # cast certain options to bool
                if option_name in pyramid_session_redis.configs_bool:
                    v = asbool(v)
                https_options[option_name] = v
            # some options maybe_dotted
            for option in pyramid_session_redis.configs_dotable:
                if option in https_options:
                    https_options[option] = config.maybe_dotted(https_options[option])

    # ensure compatibility with our options
    RedisConfigurator.ensure_compatibility(https_options)
    RedisConfigurator.ensure_security(config, https_options)
    RedisConfigurator.cleanup_options(https_options)

    # now recast everything into the redis_sessions namespace
    https_options = RedisConfigurator.recast_options(https_options, 'redis.sessions')

    # build a session
    https_session_factory = pyramid_session_redis.session_factory_from_settings(https_options)

    # okay!  register our factory
    if register_factory:
        pyramid_https_session_core.register_https_session_factory(config,
                                                                  settings,
                                                                  https_session_factory
                                                                  )
    # return the factory
    return https_session_factory
