python-antiddosclient
=====================

This is a `OpenStack Client`_ plugin for HuaWei Auto-Scaling Management API which
provides **command-line scripts** (integrated with openstack) and Python library for
accessing the Auto-Scaling management API.


Installation
------------
Currently, We can install the plugin from source code

.. code:: console

  git clone https://github.com/Huawei/OpenStackClient_Auto-Scaling python-asclient
  cd python-asclient
  python setup.py install


Command Line Client Usage
-----------------------------------------

.. note::

    The command line client is self-documenting. Use the --help or -h flag to access the usage options.
    You can find more command line client examples `here <./commands.rst>`_

This plugin is integrated with `OpenStack Client`_ , so the command line client
follow all the usage **openstack** provided.

.. code:: console

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


.. code:: console

    $ openstack as --help
    Command "antiddos" matches:
      antiddos close
      antiddos config
      antiddos daily
      antiddos logs
      antiddos open
      antiddos set
      antiddos show
      antiddos status list
      antiddos status show
      antiddos task show
      antiddos weekly


.. code:: console

    $ openstack antiddos list --help
    usage: openstack antiddos status list [-h] [-f {csv,json,table,value,yaml}]
                                          [-c COLUMN] [--max-width <integer>]
                                          [--print-empty] [--noindent]
                                          [--quote {all,minimal,none,nonnumeric}]
                                          [--status {normal,configging,notConfig,pac                                                      ketcleaning,packetdropping}]
                                          [--ip IP] [--limit LIMIT]
                                          [--offset OFFSET]

    List AntiDDos status

    optional arguments:
      -h, --help            show this help message and exit
      --status {normal,configging,notConfig,packetcleaning,packetdropping}
                            list AntiDDos with status
      --ip IP               list EIP matches the ip segment
      --limit LIMIT         return result limit
      --offset OFFSET       return result offset

    output formatters:
      output formatter options

      -f {csv,json,table,value,yaml}, --format {csv,json,table,value,yaml}
                            the output format, defaults to table
      -c COLUMN, --column COLUMN
                            specify the column(s) to include, can be repeated

    table formatter:
      --max-width <integer>
                            Maximum display width, <1 to disable. You can also use
                            the CLIFF_MAX_TERM_WIDTH environment variable, but the
                            parameter takes precedence.
      --print-empty         Print empty table if there is no data to show.

    json formatter:
      --noindent            whether to disable indenting the JSON

    CSV Formatter:
      --quote {all,minimal,none,nonnumeric}
                            when to include quotes, defaults to nonnumeric



.. code:: console

    $ openstack antiddos list --ip=160.44.197
    +--------------------------------------+---------------------+--------------+-----------+
    | Floating IP id                       | floating ip address | network type | status    |
    +--------------------------------------+---------------------+--------------+-----------+
    | 11427e0f-dc37-4319-a0e2-390e560fe116 | 160.44.197.150      | EIP          | normal    |
    | 22b0d54b-ca21-402e-b4f6-fc59a347e8bc | 160.44.197.15       | EIP          | notConfig |
    | a07be473-26b1-4619-b50f-2b208889c992 | 160.44.197.151      | EIP          | notConfig |
    +--------------------------------------+---------------------+--------------+-----------+


Python Library Usage
-------------------------------

The full api is documented in the `AntiDDos Offical Document`_ site

Here's an example of listing antiddos status using Python library with keystone V3 authentication:

.. code:: python

    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import as_client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from antiddosclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import as_client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from antiddosclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = as_client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from antiddosclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = as_client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from antiddosclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import as_client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from antiddosclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import as_client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from antiddosclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = as_client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from antiddosclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = as_client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from antiddosclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from antiddosclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = as_client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from antiddosclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = as_client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from asclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]




    >>> from keystoneauth1 import session
    >>> from keystoneauth1 import client
    >>> from antiddosclient.v1 import client

    >>> # Use Keystone API v3 for authentication as example
    >>> auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
    ...                             username=u'admin_user',
    ...                             user_domain_name=u'Default',
    ...                             password=u'password',
    ...                             project_name=u'demo',
    ...                             project_domain_name=u'Default')

    >>> # Next create a Keystone session using the auth plugin we just created
    >>> session = session.Session(auth=auth)

    >>> # Now we use the session to create a AntiDDos client
    >>> antiddos = client.Client(session=session)

    >>> # Then we can access all antiddos API
    >>> # Let's try list antiddos status API
    >>> antiddos_client.antiddos.list()
    [<AntiDDos floating_ip_address=160.44.1 ....>, ....]


.. note::

    The example above must be running and configured to use the Keystone Middleware.

    For more information on setting this up please visit: `KeyStone`_


* License: Apache License, Version 2.0
* `OpenStack Client`_
* `AntiDDos Offical Document`_
* `KeyStone`_

.. _OpenStack Client: https://github.com/openstack/python-openstackclient
.. _AntiDDos Offical Document: http://support.hwclouds.com/antiddos_dld/index.html
.. _KeyStone: http://docs.openstack.org/developer/keystoneauth/
