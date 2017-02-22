python-asclient
======================

This is a `OpenStack Client`_ plugin for HuaWei AutoScaling Management API which
provides **command-line scripts** (integrated with openstack) and Python library for
accessing the AutoScaling management API.


Installation
------------
Currently, We can install the plugin from source code

.. code:: console

    $ git clone https://github.com/Huawei/OpenStackClient_Auto-Scaling python-asclient
    $ cd python-asclient
    # use python setup.py develop for test purpose
    $ python setup.py install
    $ pip install -r requirements.txt

Command Line Client Usage
-------------------------
::

    This plugin is integrated with `OpenStack Client`_ , so the command line
    client has all features openstack provided.

User help command::

    $ openstack --help
    usage: openstack [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]
                 [--os-cloud <cloud-config-name>]
                 [--os-region-name <auth-region-name>]
                 [--os-cacert <ca-bundle-file>] [--os-cert <certificate-file>]
                 [--os-key <key-file>] [--verify | --insecure]
                 [--os-default-domain <auth-domain>]
                 [--os-interface <interface>] [--timing] [--os-beta-command]
                 [--os-profile hmac-key]
                 [--os-compute-api-version <compute-api-version>]
                 [--os-network-api-version <network-api-version>]
                 [--os-image-api-version <image-api-version>]
                 [--os-volume-api-version <volume-api-version>]
                 [--os-identity-api-version <identity-api-version>]
                 [--os-object-api-version <object-api-version>]
                 [--os-queues-api-version <queues-api-version>]
                 [--os-clustering-api-version <clustering-api-version>]
                 [--os-search-api-version <search-api-version>]
                 .......



Provided Commands

*The command line client is self-documenting. Use the --help or -h flag to
access the usage options. You can find more command line client examples* `here <./commands.rst>`_



Python Library Usage
-------------------------------

The full api is documented in the `AutoScaling Offical Document`_ site

Here's an example of listing metric types using Python library with keystone V3 authentication:

.. code:: python

    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from cloudeyeclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AutoScaling client
    >>> client = client.Client(session=session)

    >>> # Then we can access all AutoScaling API
    >>> client.groups.get()
    <AutoScalingGroup name= ....>


.. note::

    The example above must be running and configured to use the Keystone Middleware.

    For more information on setting this up please visit: `KeyStone`_


* License: Apache License, Version 2.0
* `OpenStack Client`_
* `AutoScaling Offical Document`_
* `KeyStone`_

.. _OpenStack Client: https://github.com/openstack/python-openstackclient
.. _AutoScaling Offical Document: http://support.hwclouds.com/as/
.. _KeyStone: http://docs.openstack.org/developer/keystoneauth/
