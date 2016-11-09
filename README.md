`pyramid_https_session_redis` creates an https bound version of `pyramid_session_redis`

To configure:
=============

2. In your app/__init__.py main:

	import pyramid_https_session_redis

	## initialize https session
    pyramid_https_session_redis.initialize_https_session_support(config, settings)


3. You will now have a `session_https` attribute on your `request` objects

support for https awareness
===========================

default values are `true`.  They can be set to `false`

*	session_https.ensure_scheme = true
*	pyramid_redis_https_session.ensure_scheme = true

If `request.scheme` is not "https", then `session_https` will be `None`.

`request.scheme` can be supported for backend proxies via paste deploy's prefix middleware:

Add this to your environment.ini's [app:main]

	filter-with = proxy-prefix

Then add this section

	[filter:proxy-prefix]
	use = egg:PasteDeploy#prefix


requirements
============

This package (obviously) requires `pyramid` and `pyramid_session_redis` https://github.com/jvanasco/pyramid_session_redis

This package also requires `pyramid_https_session_core` https://github.com/jvanasco/pyramid_https_session_core


PyPi
==========

This package is not yet available on PyPi



License
=======

MIT