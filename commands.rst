Configuration Commands
======================

1. config list(查询弹性伸缩配置列表)::

    $ openstack as config list --image=image-WS-Joomla  --name=as-config-TEO  --limit=1
    +--------------------------------------+---------------+--------------------------------------+----------------------+
    | ID                                   | Name          | Image                                | Create Time          |
    +--------------------------------------+---------------+--------------------------------------+----------------------+
    | 498c242b-54a4-48ec-afcd-bc21dd612b57 | as-config-TEO | c35c4f4d-79c6-465f-986d-a928fde80628 | 2016-11-29T12:57:52Z |
    +--------------------------------------+---------------+--------------------------------------+----------------------+

#. config create(创建弹性伸缩配置)::

    # create from an exists instance
    $ openstack as config create woo-config-1 --instance-id=072dc3ce-0abd-421d-9edd-27dcc8f29a43 --metadata=key1=value1
        --metadata=key2=value2 --key-name=woo_test
    Configuration 875ae9c0-0770-41fd-9d08-a02e6c5521aa created

    # create from flavor image
    $ openstack as config create woo-config-2 --image=2e53e766-2315-4c9e-9e93-561b3405ef6e --flavor=h1.large --root-volume=SSD:40
        --data-volume=SSD:40 --data-volume=SATA:120 --metadata=key1=value1 --metadata=key2=value2
        --key-name=woo_test --file=/etc/1.txt=c:\\1.txt --file=/etc/2.txt=c:\\2.txt
    Configuration 875ae9c0-0770-41fd-9d08-a02e6c5521aa created


#. config show(查询弹性伸缩配置详情)::

    $ openstack as config show 498c242b-54a4-48ec-afcd-bc21dd612b57
    +---------------+------------------------------------------------+
    | Field         | Value                                          |
    +---------------+------------------------------------------------+
    | ID            | 498c242b-54a4-48ec-afcd-bc21dd612b57           |
    | Name          | as-config-TEO                                  |
    | Disk          | disk_type='SYS', size='80', volume_type='SATA' |
    | Instance ID   | None                                           |
    | Instance Name | None                                           |
    | Flavor        | normal1                                        |
    | Image         | c35c4f4d-79c6-465f-986d-a928fde80628           |
    | Key Name      | KeyPair-fdv                                    |
    | Public IP     | None                                           |
    | User Data     | None                                           |
    | Metadata      |                                                |
    | Create Time   | 2016-11-29T12:57:52Z                           |
    +---------------+------------------------------------------------+

#. config delete(删除弹性伸缩配置)::

    $ openstack as config delete as-config-name-1 as-config-id-2
    done


Group Commands
==================

1. group list()::

    $ openstack as group list
    +--------------------------------------+--------------------------------------+-----------------------------------------+--------+
    | ID                                   | Name                                 | Instance Number(Current/desire/min/max) | Status |
    +--------------------------------------+--------------------------------------+-----------------------------------------+--------+
    | ac8acbb4-e6ce-4890-a9f2-d8712b3d7385 | ac8acbb4-e6ce-4890-a9f2-d8712b3d7385 | 1/1/0/4                                 | PAUSED |
    | 56e25174-c317-4be1-9fbd-17d5aff10ad5 | 56e25174-c317-4be1-9fbd-17d5aff10ad5 | 0/2/1/4                                 | PAUSED |
    +--------------------------------------+--------------------------------------+-----------------------------------------+--------+


