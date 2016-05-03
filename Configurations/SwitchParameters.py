
datapath1 = {
                "ip":"10.1.1.13",
                "user":"manager",
                "password":"",
                "openflow_instance_name":"mar01",
                "cli_name":"SW11#",
                "dpid":"00:64:38:63:bb:58:eb:00",
                "model":"2920",
                "software_tables":["0"],
                "hardware_tables":["n/a"]}

datapath2 = {
                "ip":"10.1.1.15",
                "user":"manager",
                "password":"",
                "openflow_instance_name":"test01",
                "cli_name":"sw1#",
                "dpid":"00:64:74:46:a0:5f:1e:80",
                "model":"3500",
                "software_tables":["200"],
                "hardware_tables":["100"]}

datapath3 = {
                "ip":"10.1.10.61",
                "user":"manager",
                "password":"",
                "openflow_instance_name":"1",
                "cli_name":"<SW00>",
                "dpid":"00:00:00:00:00:00:00:16",
                "model":"5700",
                "software_tables":["n/a"],
                "hardware_tables":["20"]}

datapath4 = {
                "ip":"10.1.1.72",
                "user":"manager",
                "password":"descartes",
                "openflow_instance_name":"1",
                "cli_name":"<SW42>",
                "dpid":"00:00:00:00:00:00:00:42",
                "model":"5130",
                "software_tables":["n/a"],
                "hardware_tables":["0"]}

datapathList = {"00:64:38:63:bb:58:eb:00":datapath1,
                "00:0a:74:46:a0:5f:1e:80":datapath2,
                "00:00:00:00:00:00:00:16":datapath3,
                "00:00:00:00:00:00:00:42":datapath4}



switch2920_rule_1={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch2920_rule_2={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch2920_rule_3={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch2920_rule_4={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_type":"ipv4"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch2920_rule_5={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch2920_rule_6={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch2920_rule_7={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch2920_rule_8={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch2920_rule_9={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"},{"tcp_src":"80"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch2920_rule_10={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"},{"tcp_src":"80"},{"tcp_dst":"90"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}


switch3500_rule_1_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11}],"instructions":[{"apply_actions":[{"output":17}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_2_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"}],"instructions":[{"apply_actions":[{"output":17}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_3_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"}],"instructions":[{"apply_actions":[{"output":17}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_4_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"}],"instructions":[{"apply_actions":[{"output":17}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_5_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"}],"instructions":[{"apply_actions":[{"output":17}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_6_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"}],"instructions":[{"apply_actions":[{"output":17}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_7_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"}],"instructions":[{"apply_actions":[{"output":17}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_8_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"},{"tcp_src":"80"}],"instructions":[{"apply_actions":[{"output":17}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_9_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"},{"tcp_src":"80"},{"tcp_dst":"90"}],"instructions":[{"apply_actions":[{"output":17}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}


switch3500_rule_action_performace_output=[
{"flow":{"priority":0,"table_id":200,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ipv4_src":"10.100.3.11"},{"ipv4_dst":"10.100.3.17"}],"instructions":[{"apply_actions":[{"output":17}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}},
{"flow":{"priority":0,"table_id":200,"idle_timeout":0,"match":[{"in_port":17},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ipv4_src":"10.100.3.17"},{"ipv4_dst":"10.100.3.11"}],"instructions":[{"apply_actions":[{"output":11}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
]

switch3500_rule_action_performace_output_setipsrc=[
{"flow":{"priority":0,"table_id":200,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ipv4_src":"10.100.3.11/16"},{"ipv4_dst":"10.100.3.17/16"}],"instructions":[{"apply_actions":[{"output":17},{"set_field":{"ipv4_dst":"10.100.3.17"}}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}},
{"flow":{"priority":0,"table_id":200,"idle_timeout":0,"match":[{"in_port":17},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ipv4_src":"10.100.3.17/16"},{"ipv4_dst":"10.100.3.11/16"}],"instructions":[{"apply_actions":[{"output":11},{"set_field":{"ipv4_dst":"10.100.3.11"}}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
]

switch3500_rule_action_performace_output_setipsrcdst=[
{"flow":{"priority":0,"table_id":200,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ipv4_src":"10.100.3.11"},{"ipv4_dst":"10.100.3.17"}],"instructions":[{"apply_actions":[{"output":17},{"set_field":{"ipv4_src":"10.100.3.11"}},{"set_field":{"ipv4_dst":"10.100.3.17"}}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}},
{"flow":{"priority":0,"table_id":200,"idle_timeout":0,"match":[{"in_port":17},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ipv4_src":"10.100.3.17"},{"ipv4_dst":"10.100.3.11"}],"instructions":[{"apply_actions":[{"output":11},{"set_field":{"ipv4_src":"10.100.3.17"}},{"set_field":{"ipv4_dst":"10.100.3.11"}}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
]

switch3500_rule_action_performace_output_setfiled_setttl=[
{"flow":{"priority":0,"table_id":200,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ipv4_src":"10.100.3.11"},{"ipv4_dst":"10.100.3.17"}],"instructions":[{"apply_actions":[{"output":17},{"set_nw_ttl":101},{"set_field":{"ipv4_src":"10.100.3.11"}},{"set_field":{"ipv4_dst":"10.100.3.17"}}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}},
{"flow":{"priority":0,"table_id":200,"idle_timeout":0,"match":[{"in_port":17},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ipv4_src":"10.100.3.17"},{"ipv4_dst":"10.100.3.11"}],"instructions":[{"apply_actions":[{"output":11},{"set_nw_ttl":101},{"set_field":{"ipv4_src":"10.100.3.17"}},{"set_field":{"ipv4_dst":"10.100.3.11"}}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
]


switch3500_rule_1_OF10={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_2_OF10={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_3_OF10={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_4_OF10={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_5_OF10={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_6_OF10={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_7_OF10={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_8_OF10={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"},{"tcp_src":"80"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_9_OF10={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"},{"tcp_src":"80"},{"tcp_dst":"90"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}


switch5700_rule_1={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11}],"instructions":[{"apply_actions":[{"output":"17"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_rule_2={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"}],"instructions":[{"apply_actions":[{"output":"17"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_rule_3={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"}],"instructions":[{"apply_actions":[{"output":"17"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_rule_4={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_src":"11:11:11:11:11:11"}],"instructions":[{"apply_actions":[{"output":"17"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_rule_5={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_src":"11:11:11:11:11:11"},{"eth_dst":"11:11:11:11:11:11"}],"instructions":[{"apply_actions":[{"output":"17"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_rule_6={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_src":"11:11:11:11:11:11"},{"eth_dst":"11:11:11:11:11:11"},{"eth_type":"ipv4"}],"instructions":[{"apply_actions":[{"output":"17"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_rule_7={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_src":"11:11:11:11:11:11"},{"eth_dst":"11:11:11:11:11:11"},{"eth_type":"ipv4"},{"ipv4_src":"10.0.3.2"}],"instructions":[{"apply_actions":[{"output":"17"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_rule_8={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_src":"11:11:11:11:11:11"},{"eth_dst":"11:11:11:11:11:11"},{"eth_type":"ipv4"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"}],"instructions":[{"apply_actions":[{"output":"17"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_rule_9={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_src":"11:11:11:11:11:11"},{"eth_dst":"11:11:11:11:11:11"},{"eth_type":"ipv4"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"}],"instructions":[{"apply_actions":[{"output":"17"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_rule_10={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_src":"11:11:11:11:11:11"},{"eth_dst":"11:11:11:11:11:11"},{"eth_type":"ipv4"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"},{"tcp_src":"80"}],"instructions":[{"apply_actions":[{"output":"17"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_rule_11={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_src":"11:11:11:11:11:11"},{"eth_dst":"11:11:11:11:11:11"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ip_ecn":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"},{"tcp_src":"80"},{"tcp_dst":"90"}],"instructions":[{"apply_actions":[{"output":"17"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}


switch5700_mac_ip_rule={"flow":{"priority":65535,"table_id":10,"idle_timeout":0,"match":[{"eth_dst":"38:63:bb:58:eb:1d"},{"vlan_vid":"100"}],"instructions":[{"write_actions":[{"output":"17"}]}],"cookie":"0xffff000000000000","flow_mod_cmd":"add"}}

switch_compatible_rules = {"2920":[switch2920_rule_1,switch2920_rule_2,switch2920_rule_3,switch2920_rule_4,switch2920_rule_5,switch2920_rule_6,switch2920_rule_7,switch2920_rule_8,switch2920_rule_9,switch2920_rule_10],
                           "3500_OF10":[switch3500_rule_1_OF10,switch3500_rule_2_OF10,switch3500_rule_3_OF10,switch3500_rule_4_OF10,switch3500_rule_5_OF10,switch3500_rule_6_OF10,switch3500_rule_7_OF10,switch3500_rule_8_OF10,switch3500_rule_9_OF10],
                           "3500_OF13":[switch3500_rule_1_OF13,switch3500_rule_2_OF13,switch3500_rule_3_OF13,switch3500_rule_4_OF13,switch3500_rule_5_OF13,switch3500_rule_6_OF13,switch3500_rule_7_OF13,switch3500_rule_8_OF13,switch3500_rule_9_OF13],
                           "5700_NORMAL":[switch5700_rule_1,switch5700_rule_2,switch5700_rule_3,switch5700_rule_4,switch5700_rule_5,switch5700_rule_6,switch5700_rule_7,switch5700_rule_8,switch5700_rule_9,switch5700_rule_10,switch5700_rule_11],
                           "5700_MAC_IP":[switch5700_mac_ip_rule],
                           "5130_NORMAL":[switch5700_rule_1,switch5700_rule_2,switch5700_rule_3,switch5700_rule_4,switch5700_rule_5,switch5700_rule_6,switch5700_rule_7,switch5700_rule_8,switch5700_rule_9,switch5700_rule_10,switch5700_rule_11],
                           "5130_MAC_IP":[switch5700_mac_ip_rule]}



switch2920_ping_rule_1={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":2}],"actions":[{"output": 3}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch2920_ping_rule_2={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3}],"actions":[{"output": 2}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}

#switch3500_ping_flow_1_OF10= {"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"eth_type":"ipv4"},{"ipv4_src":"10.0.3.3"}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
#switch3500_ping_flow_2_OF10= {"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":2},{"eth_type":"ipv4"},{"ipv4_src":"10.0.3.2"}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}

#switch3500_ping_flow_1_OF13= {"flow":{"priority":0,"table_id":100,"idle_timeout":0,"match":[{"in_port":3},{"eth_type":"ipv4"}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
#switch3500_ping_flow_2_OF13= {"flow":{"priority":0,"table_id":100,"idle_timeout":0,"match":[{"in_port":2},{"eth_type":"ipv4"}],"instructions":[{"apply_actions":[{"output":3}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}



switch5700_rule_for_2920_1={"flow":{"priority":0,"table_id":20,"idle_timeout":0,"match":[{"in_port":11}],"instructions":[{"apply_actions":[{"output":"2"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_rule_for_2920_2={"flow":{"priority":0,"table_id":20,"idle_timeout":0,"match":[{"in_port":2}],"instructions":[{"apply_actions":[{"output":"11"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_rule_for_2920_3={"flow":{"priority":0,"table_id":20,"idle_timeout":0,"match":[{"in_port":17}],"instructions":[{"apply_actions":[{"output":"3"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_rule_for_2920_4={"flow":{"priority":0,"table_id":20,"idle_timeout":0,"match":[{"in_port":3}],"instructions":[{"apply_actions":[{"output":"17"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}

switch5700_ping_rule_1={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11}],"instructions":[{"apply_actions":[{"output":"17"}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch5700_ping_rule_2={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":17}],"instructions":[{"apply_actions":[{"output":"11"}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}

testbed_ping_rule_1={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11},{"eth_type":"ipv4"},{"ipv4_src":"10.100.3.11"},{"ipv4_dst":"10.100.3.17"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
testbed_ping_rule_2={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":17},{"eth_type":"ipv4"},{"ipv4_src":"10.100.3.17"},{"ipv4_dst":"10.100.3.11"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
testbed_ping_rule_1_OF10={"flow":{"priority":2,"idle_timeout":0,"match":[{"in_port":11},{"eth_type":"ipv4"},{"ipv4_src":"10.100.3.11"},{"ipv4_dst":"10.100.3.17"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
testbed_ping_rule_2_OF10={"flow":{"priority":2,"idle_timeout":0,"match":[{"in_port":17},{"eth_type":"ipv4"},{"ipv4_src":"10.100.3.17"},{"ipv4_dst":"10.100.3.11"}],"actions":[{"output": 11}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_ShortDummy_1_OF10={"flow":{"priority":2,"table_id":0,"idle_timeout":0,"match":[{"eth_type":"ipv4"},{"ipv4_src":"10.1.3.11"}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_ShortDummy_2_OF10={"flow":{"priority":2,"table_id":0,"idle_timeout":0,"match":[{"eth_type":"ipv4"},{"ipv4_src":"10.1.3.17"}],"actions":[{"output": 11}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
#testbed_ping_rule_1_OF10={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11}],"actions":[{"output": 17}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
#testbed_ping_rule_2_OF10={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":17}],"actions":[{"output": 11}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}

switch3500_ping_rule_1={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11}],"instructions":[{"apply_actions":[{"output":"17"}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_ping_rule_2={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":17}],"instructions":[{"apply_actions":[{"output":"11"}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
