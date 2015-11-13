from pyramid.settings import asbool

import pyramid_https_session_core

import pyramid_redis_sessions


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


def initialize_https_session_support(config, settings):
    """
    Parses config settings, builds a https session factory, registers it
    """


    https_options = {}
    https_prefixes = ('session_https.',
                      'redis.sessions_https.',
                      )
    for k, v in settings.items():
        for prefix in https_prefixes:
            if k.startswith(prefix):
                option_name = k[len(prefix):]
                if option_name in ('cookie_on_exception',
                                   'cookie_secure',
                                   'cookie_httponly',
                                   ):
                    v = asbool(v)
                https_options[option_name] = v
            for option in ('client_callable',
                           'serialize',
                           'deserialize',
                           'id_generator'
                           ):
                  key = '%s.%s' % (prefix, option)
                  if key in settings:
                      https_options[key] = config.maybe_dotted(settings[key])

    # ensure compatibility with our options
    RedisConfigurator.ensure_compatibility(https_options)
    RedisConfigurator.ensure_security(config, https_options)
    RedisConfigurator.cleanup_options(https_options)

    # now recast everything into the redis_sessions namespace
    https_options = RedisConfigurator.recast_options(https_options, 'redis.sessions')

    # build a session
    https_session_factory = pyramid_redis_sessions.session_factory_from_settings(https_options)

    # okay!  register our factory
    pyramid_https_session_core.register_https_session_factory(config,
                                                              settings,
                                                              https_session_factory
                                                              )
