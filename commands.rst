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

1. group create()::
    $ openstack as group create Woo-Test-1 --network=f5ebe00f-3ac1-4ec5-9175-090d9d43e4ef
    --subnet=60a86b97-1501-4d89-949c-25a49c5c3c31 --security-group=d3e2e1ad-b7f2-414c-9b5a-2d485686a96a
    --config=as-config-TEO --desire-instance=1 --max-instance=3 --min-instance=1
    --cool-down=900 --lb-listener=038a1208f15b47ab8c2f5f4238c9e783
    --health-periodic-audit-time=15 --health-periodic-audit-method=ELB_AUDIT
    --instance-terminate-policy=OLD_CONFIG_OLD_INSTANCE --delete-public-ip  --debug

#. group list(查询弹性伸缩组列表)::

    $ openstack as group list
    +--------------------------------------+--------------------------------------+-----------------------------------------+--------+
    | ID                                   | Name                                 | Instance Number(Current/desire/min/max) | Status |
    +--------------------------------------+--------------------------------------+-----------------------------------------+--------+
    | ac8acbb4-e6ce-4890-a9f2-d8712b3d7385 | ac8acbb4-e6ce-4890-a9f2-d8712b3d7385 | 1/1/0/4                                 | PAUSED |
    | 56e25174-c317-4be1-9fbd-17d5aff10ad5 | 56e25174-c317-4be1-9fbd-17d5aff10ad5 | 0/2/1/4                                 | PAUSED |
    +--------------------------------------+--------------------------------------+-----------------------------------------+--------+

#. group show(查询弹性伸缩组详情)::

    $ openstack as group show as-group-teo
    +----------------------------------+-------------------------------------------+
    | Field                            | Value                                     |
    +----------------------------------+-------------------------------------------+
    | ID                               | ac8acbb4-e6ce-4890-a9f2-d8712b3d7385      |
    | Name                             | as-group-teo                              |
    | Instance(Current/desire/min/max) | 1/1/0/4                                   |
    | Scaling Configuration Id         | 498c242b-54a4-48ec-afcd-bc21dd612b57      |
    | Scaling Configuration Name       | as-config-TEO                             |
    | Cool down time                   | 200                                       |
    | LB listener id                   | 038a1208f15b47ab8c2f5f4238c9e783          |
    | Security Groups                  | id='d3e2e1ad-b7f2-414c-9b5a-2d485686a96a' |
    | Create Time                      | 2016-11-29T12:57:52Z                      |
    | VPC id                           | f496ae99-6e3e-4957-924d-087ca5b0b2f0      |
    | Health periodic audit method     | ELB_AUDIT                                 |
    | Health periodic audit time       | 5                                         |
    | Instance Terminate Policy        | OLD_CONFIG_OLD_INSTANCE                   |
    | Scaling                          | False                                     |
    | Delete Public IP                 | False                                     |
    | Notifications                    |                                           |
    | Status                           | PAUSED                                    |
    +----------------------------------+-------------------------------------------+

#. group resume(启用弹性伸缩组)::

    $ openstack as group resume as-group-teo
    done

#. group resume(停止弹性伸缩组)::

    $ openstack as group pause as-group-teo
    done

#. group delete(停止弹性伸缩组)::

    $ openstack as group delete as-group-teo
    done


