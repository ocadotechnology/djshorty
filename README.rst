Shorty
======

A URL shortening app written in Django.

Shortened URLs will work at either shorty.example.com/short-url or short-url.shorty.example.com (i.e. the short path can either be in the URL, or a subdomain).

Quick Start
-----------

Get started with Shorty by following these steps:

* Install ``djshorty`` with ``pip``::

    pip install djshorty

* Add ``shorty`` to your ``INSTALLED_APPS`` in ``settings.py``::

    INSTALLED_APPS = (
        ...
        'shorty',
        ...
    )

* Either set ``short.urls`` as your ``ROOT_URLCONF``, or include it in your own ``urls.py``.

* Shorty relies on django-autoconfig_, which requires the following at the end of ``settings.py``::

    from django_autoconfig.autoconfig import configure_settings
        configure_settings(globals())


Settings
--------

Shorty provides the following settings:

* ``SHORTY_EXTERNAL_FLAG``: If Shorty is deployed in a corporate environment, and you want the ability for some short URLs to resolve outside the company and others to remain internal, set this to ``True``. URLs not marked as 'external' will require authentication. This is designed to work with a Single Sign On solution.

* ``SHORTY_CANONICAL_DOMAIN``: Set this to normalise the domain before redirection. This is useful if you have multiple domains, but the SSO system (see above) requires a single domain to work. For example, if Shorty is primarily deployed at ``https://shorty.example.com/<short-url>``, but you also allow short URLs to resolve at ``https://<short-url>.shorty.example.com``, you may need to set this to ``'https://shorty.example.com'``. It should include the scheme (http or https), and not end with a trailing slash.

Contributing
------------

To contribute, fork the repo, do your work, and issue a pull request. We ask that contributors adhere to `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ standards, and include full tests for all their code.

.. _`django-autoconfig`: http://github.com/mikebryant/django-autoconfig/
