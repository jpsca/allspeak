.. module:: allspeak

Choosing what locale / time zone to use
=============================================

Language
---------------------------------------------

On each request, Allspeak tries to guess the user's prefered locale (an ISO 639-1 language code like 'es', 'en-US', etc.) that is also available in the list of available locales defined by your application.

It tries the following sources, in order, until it found a suitable option:

- A `request` attribute named `'locale'`
- A `'locale'` parameter in the URL. Eg: `http://example.com/foo/?locale=es`.
- The browser languages, defined in the "accept language" header
- The default locale


Timezone
---------------------------------------------

In a similar way, the user's timezone —used to localize dates— is looked up in:

- A `request` attribute named `'tzinfo'`
- A `'tzinfo'` parameter in the URL.
	Eg: `http://example.com/foo/?tzinfo=America/Lima`.
- The default timezone


Forcing a locale and/or timezone
---------------------------------------------

Because the locale and timezone are looked up first as attributes of the `request` object, you can use that to inject, on each request, the preferences or your logged users.

In Flask you do it by decorating a function with `before_request`. Other frameworks have similar methods for doing it.

.. sourcecode:: python

    @app.before_request
    def set_locale(request, **kwargs):

        # Overwrite the browser language with the
        # user defaults (if available)
        if g.user:
            if g.user.locale:
                request.locale = user.locale
            if g.user.tzinfo:
                request.tzinfo = user.tzinfo

You could also read the locale from the URL (the path or a subdomain). For example:

.. sourcecode:: python

    bp = Blueprint('my_blueprint', __name__)
    app.register_blueprint(bp, url_prefix='<locale>')

    @bp.before_request
    def set_locale(request, **kwargs):
        request.locale = kwargs.pop('locale', None)
