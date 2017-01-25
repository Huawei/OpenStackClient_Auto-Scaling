NO.	API URI	Function
1	POST /autoscaling-api/v1/{tenant_id}/scaling_group	Creating an AS Group
2	GET /autoscaling-api/v1/{tenant_id}/scaling_group	Querying AS Groups
3	GET /autoscaling-api/v1/{tenant_id}/scaling_group/{scaling_group_id}	Querying AS Group Details
4	PUT /autoscaling-api/v1/{tenant_id}/scaling_group/{scaling_group_id}	Modifying an AS Group
5	DELETE /autoscaling-api/v1/{tenant_id}/scaling_group/{scaling_group_id}	Deleting an AS Group
6	POST /autoscaling-api/v1/{tenant_id}/scaling_group/{scaling_group_id}/action	Enabling an AS Group
7	POST /autoscaling-api/v1/{tenant_id}/scaling_group/{scaling_group_id}/action	Disabling an AS Group
8	POST /autoscaling-api/v1/{tenant_id}/scaling_configuration	Creating an AS Configuration
9	GET /autoscaling-api/v1/{tenant_id}/scaling_configuration	Querying AS Configurations
10	GET /autoscaling-api/v1/{tenant_id}/scaling_configuration/{scaling_configuration_id}	Querying AS Configuration Details
11	DELETE /autoscaling-api/v1/{tenant_id}/scaling_configuration/{scaling_configuration_id}	Deleting an AS Configuration
12	GET /autoscaling-api/v1/{tenant_id}/scaling_group_instance/{scaling_group_id}/list	Querying Instances in an AS Group
13	DELETE /autoscaling-api/v1/{tenant_id}/scaling_group_instance/{instance_id}	Removing Instances from an AS Group
14	POST /autoscaling-api/v1/{tenant_id}/scaling_group_instance/{scaling_group_id}/action	Batch Removing or Adding Instances
15	POST /autoscaling-api/v1/{tenant_id}/scaling_policy	Creating an AS Policy
16	PUT /autoscaling-api/v1/{tenant_id}/scaling_policy/{scaling_policy_id}	Modifying an AS Policy
17	GET /autoscaling-api/v1/{tenant_id}/scaling_policy/{scaling_group_id}/list	Querying AS Policies
18	GET /autoscaling-api/v1/{tenant_id}/scaling_policy/{scaling_policy_id}	Querying AS Policy Details
19	POST /autoscaling-api/v1/{tenant_id}/scaling_policy/{scaling_policy_id}/action	Executing an AS Policy
20	POST /autoscaling-api/v1/{tenant_id}/scaling_policy/{scaling_policy_id}/action	Enabling an AS Policy
21	POST /autoscaling-api/v1/{tenant_id}/scaling_policy/{scaling_policy_id}/action	Disabling an AS Policy
22	DELETE /autoscaling-api/v1/{tenant_id}/scaling_policy/{scaling_policy_id}	Deleting an AS Policy
23	GET /autoscaling-api/v1/{tenant_id}/scaling_activity_log/{scaling_group_id}	Querying Scaling Action Logs
24	GET /autoscaling-api/v1/{tenant_id}/quotas	Querying Quotas for AS Groups and AS Configurations
25	GET /autoscaling-api/v1/{tenant_id}/quotas/{scaling_group_id}	Querying Quotas for AS Instances and AS Policies
