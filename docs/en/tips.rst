
Tips
=============================================

.. module:: allspeak


Take advantage of line breaks
---------------------------------------------

With a long texts you probably don't want one translation key per sentence. You can take advantage of the `|` syntax in YAML to transform your line breaks into paragraphs:

.. sourcecode:: yaml

    long_text: |
        Lorem ipsum dolor sit amet.
        Consectetur adipisicing elit.

.. sourcecode:: html+jinja

    {%- for p in t('long_text').split('\n') %}
    <p>{{ p }}</p>
    {%- endfor %}

This becomes:

.. sourcecode:: html

    <p>Lorem ipsum dolor sit amet.</p>
    <p>Consectetur adipisicing elit.</p>


It work great with lists too:

.. sourcecode:: yaml

    items: |
        Lorem
        Ipsum
        Dolor

.. sourcecode:: html+jinja

    <ul>
      {%- for item in t('items').split('\n') %}
      <li>{{ item }}</li>
      {%- endfor %}
    </ul>

This becomes:

.. sourcecode:: html

    <ul>
      <li>Lorem</li>
      <li>Ipsum</li>
      <li>Dolor</li>
    </ul>


Use multiple YAML files
---------------------------------------------

If your app has different parts with different i18n needs, consider using multiple files.

Perhaps you have an admin section with only one or two locales, and a public section with a bunch.

Instead of having the translator needlessly translate your admin section to every locale, split it into a `locales/en.yml` and a `locales/admin.en.yml`.

Remember that the file names has no mean to Allspeak about what language it contains, it's just for humans to known without having to open the file. You still have to put the language or languages as first-level keys.


Group translations under common keys
---------------------------------------------

Instead of translate a big chunk of html code or to leave small bits without context, what you can do is split up the translations, but keep them under the same key:

.. sourcecode:: yaml

    login:
        intro: "Log in or Register to do stuff."
        login: "Log in"
        login_title: "Welcome back!"
        register: "Register"
        register_title: "You can delete your account at any time"

so you can do:

.. sourcecode:: html+jinja

    <p>{{ t('login.intro') }}</p>
    <p>
        <a href="{{ url_for('login') }}"
          title="{{ t('login.login_title') }}"
        >{{ t('login.login') }}</a>

        <a href="{{ url_for('register') }}"
          title="{{ t('login.register_title') }}"
        >{{ t('login.register') }}</a>
    </p>


This way, the translator sees no code or markup.


Test your locale files
---------------------------------------------

Allspeak comes with a :meth:`~.I18n.test_for_incomplete_locales` method to check a list of locales for keys that are defined in one but not in the other. You can call it from one of your tests.
