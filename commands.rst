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


Instance Commands
=================

1. instance list(查询弹性伸缩组中的实例列表)::

    $ openstack as instance list --group=ac8acbb4-e6ce-4890-a9f2-d8712b3d7385
    +-----------------------------+------------------------+---------------+----------------+------------------+---------------+
    | Instance ID                 | Instance Name          | AS Group Name | AS Config Name | Lifecycle Status | Health Status |
    +-----------------------------+------------------------+---------------+----------------+------------------+---------------+
    | abe6a889-d689-4528-aa0d-    | as-config-TEO_MMUCM9KR | as-group-teo  | as-config-TEO  | INSERVICE        | NORMAL        |
    | e48f5274c83d                |                        |               |                |                  |               |
    +-----------------------------+------------------------+---------------+----------------+------------------+---------------+

#. instance remove(批量移出实例)::

    $ openstack as instance remove --instance=as-config-TEO_MMUCM9KR --group=ac8acbb4-e6ce-4890-a9f2-d8712b3d7385 --delete
    done


#. instance add(批量添加实例)::

    $ openstack as instance add --instance=as-config-TEO_MMUCM9KR --group=ac8acbb4-e6ce-4890-a9f2-d8712b3d7385
    done



Policy Commands
===============

1. policy create(创建弹性伸缩策略)::

    $  openstack as policy create WooTest --action=ADD:1 --group=ac8acbb4-e6ce-4890-a9f2-d8712b3d7385
        --type=SCHEDULED --launch-time=2017-02-19T13:40
    Policy xxxxxxx created

    $ openstack as policy create WooTest --action=ADD:1 --group=ac8acbb4-e6ce-4890-a9f2-d8712b3d7385
        --type=RECURRENCE --start-time=2017-02-19T14:00 --end-time=2017-02-28T23:00
        --recurrence=Daily:12:00 --action=SET:1
    Policy e0eb7de0-aa5b-435c-8d4c-46867fdf087d created

#. policy edit(修改弹性伸缩策略)::

    $ openstack as policy edit  e0eb7de0-aa5b-435c-8d4c-46867fdf087d  --action=SET:2
        --cool-down=60 --name=WooTest2 --type=RECURRENCE --recurrence=Weekly:1,3,5
        --start-time=2017-02-20T00:00 --end-time=2017-03-20T00:00 --debug
    done


#. policy list(查询弹性伸缩策略列表)::

    $ openstack as policy list --group=ac8acbb4-e6ce-4890-a9f2-d8712b3d7385
    +--------------------------------------+----------------+-------------+-------------+----------------+-----------+
    | Policy ID                            | Policy Name    | Policy Type | CoolDown(s) | Trigger Action | Status    |
    +--------------------------------------+----------------+-------------+-------------+----------------+-----------+
    | 67174f3d-0a7a-4c13-a890-edbe11b45242 | as-policy-rpdj | ALARM       |         900 | ADD 1          | INSERVICE |
    | 81c5051a-cb1d-4993-b036-3d3afc6c9648 | as-policy-tfum | SCHEDULED   |         900 | ADD 4          | PAUSED    |
    | c8e2c794-f8ef-428a-8efe-3ff1268f6804 | WooTest        | SCHEDULED   |         900 | ADD 1          | INSERVICE |
    | 2a19d97f-8d2e-44f7-873e-c1e7c321e68f | WooTest        | SCHEDULED   |         900 | ADD 1          | INSERVICE |
    | e0eb7de0-aa5b-435c-8d4c-46867fdf087d | WooTest        | RECURRENCE  |         900 | SET 1          | INSERVICE |
    +--------------------------------------+----------------+-------------+-------------+----------------+-----------+


#. policy show()::

    $ openstack as policy show 81c5051a-cb1d-4993-b036-3d3afc6c9648
    +------------------+--------------------------------------+
    | Field            | Value                                |
    +------------------+--------------------------------------+
    | Group Id         | ac8acbb4-e6ce-4890-a9f2-d8712b3d7385 |
    | Policy ID        | 81c5051a-cb1d-4993-b036-3d3afc6c9648 |
    | Policy Name      | as-policy-tfum                       |
    | Policy Type      | SCHEDULED                            |
    | Alarm Id         |                                      |
    | CoolDown(s)      | 900                                  |
    | Scheduled Policy | launch_time='2016-12-24T13:44Z'      |
    | Trigger Action   | ADD 4                                |
    | Create Time      | 2016-11-30T13:44:21Z                 |
    | Status           | INSERVICE                            |
    +------------------+--------------------------------------+

#. policy pause(停止弹性伸缩策略)::

    $ openstack as policy pause 81c5051a-cb1d-4993-b036-3d3afc6c9648
    done


#. policy resume(启用弹性伸缩策略)::

    $ openstack as policy resume 81c5051a-cb1d-4993-b036-3d3afc6c9648
    done


#. policy execute(执行弹性伸缩策略)::

    $ openstack as policy execute 81c5051a-cb1d-4993-b036-3d3afc6c9648
    done


#. policy delete(删除弹性伸缩策略)::

    $ openstack as policy delete 81c5051a-cb1d-4993-b036-3d3afc6c9648
    done

Log Commands
============

1. log list(查询伸缩活动日志)::

    $ openstack as log list --group=ac8acbb4-e6ce-4890-a9f2-d8712b3d7385 --start-time=2016-11-28T17:45:10
        --end-time=2017-01-01T00:00:00 --limit=2 --offset=1
    +----------------------+----------------------+------------------------+-----------------------------------------------+---------+
    | Start Time           | End Time             | Current/Desire/Scaling | Scaling Reason                                | Status  |
    +----------------------+----------------------+------------------------+-----------------------------------------------+---------+
    | 2016-11-30T14:17:52Z | 2016-11-30T14:19:41Z | 2/1/1                  | change_reason='MANNUAL_DELETE',               | SUCCESS |
    |                      |                      |                        | change_time='2016-11-30T14:17:52Z',           |         |
    |                      |                      |                        | new_value='1', old_value='2'                  |         |
    | 2016-11-29T17:45:10Z | 2016-11-29T17:46:31Z | 3/2/1                  | change_reason='SCHEDULED',                    | SUCCESS |
    |                      |                      |                        | change_time='2016-11-29T17:45:00Z',           |         |
    |                      |                      |                        | new_value='2', old_value='3'                  |         |
    +----------------------+----------------------+------------------------+-----------------------------------------------+---------+


Quota Commands
==============

1. quota list(查询配额)::

    $ openstack as quota list
    +------------------+-------+------+------+
    | type             | quota | used |  max |
    +------------------+-------+------+------+
    | scaling_Group    |    25 |    2 |   50 |
    | scaling_Config   |   100 |    2 |  200 |
    | scaling_Policy   |    50 |   -1 |   50 |
    | scaling_Instance |   200 |   -1 | 1000 |
    +------------------+-------+------+------+

#. quota list(查询弹性伸缩策略和伸缩实例配额)::

    $ openstack as quota list --group=ac8acbb4-e6ce-4890-a9f2-d8712b3d7385
    +------------------+-------+------+------+
    | type             | quota | used |  max |
    +------------------+-------+------+------+
    | scaling_Policy   |    50 |    2 |   50 |
    | scaling_Instance |   200 |    0 | 1000 |
    +------------------+-------+------+------+
