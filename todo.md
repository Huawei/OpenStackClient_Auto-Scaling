1. as group create
2. as group edit
3. as group delete (Test)


auto scaling 调整

5.4 5.5 合并 留下 5.5
6.2 6.3 合并 留下 6.3
9.1 9.2 合并 使用可选参数来区分 -> openstack as quota list [--group <group>]


7.3 group 必须，导致无法通过 policy-name 查找policy

openstack as group create Woo-Test-1 --network=f5ebe00f-3ac1-4ec5-9175-090d9d43e4ef --subnet=60a86b97-1501-4d89-949c-25a49c5c3c31 --security-group=d3e2e1ad-b7f2-414c-9b5a-2d485686a96a --config=as-config-TEO --desire-instance=1 --max-instance=3 --min-instance=1 --cool-down=900 --lb-listener=038a1208f15b47ab8c2f5f4238c9e783 --health-periodic-audit-time=15 --health-periodic-audit-method=ELB_AUDIT --instance-terminate-policy=OLD_CONFIG_OLD_INSTANCE --delete-public-ip