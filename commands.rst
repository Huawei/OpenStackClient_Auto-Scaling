Command Samples
===============

1. antiddos config

#. antiddos open (开启AntiDDos）

.. code:: console

    # open antiddos with IP
    $ openstack antiddos open 160.44.196.90 --enable-l7 --traffic-pos=1 --http-request-pos=1
            --cleaning-access-pos=1 --app-type=1 --os-antiddos-endpoint-override=https://antiddos.eu-de.otc.t-systems.com
    Request Received, task id: 13f621cb-3dfa-4d96-9821-cd7d11fb15af

    # open antiddos with floating ip id
    $ openstack antiddos open 194bca90-9c23-43fb-b744-9d0bbd043a76 --enable-l7 --traffic-pos=1 --http-request-pos=1
            --cleaning-access-pos=1 --app-type=1 --os-antiddos-endpoint-override=https://antiddos.eu-de.otc.t-systems.com
    Request Received, task id: 13f621cb-3dfa-4d96-9821-cd7d11fb15af


