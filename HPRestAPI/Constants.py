




#======================================================= Testing topology configuration =============================================================================================
#Devices_Under_Test={"3500":{"IP":'10.0.1.251',"USER":"manager","PASSWORD":"",}}
#DUT_3500={"3500":{"IP":'10.0.1.251',"USER":"manager","PASSWORD":"","OF_INSTANCE_NAME":"test01","DPID":"00:0a:74:46:a0:5f:1e:80",""}}
# DUT_IP = '10.1.10.61'
# DUT_USER = 'manager'
# DUT_PASS = ''
# DUT_DPID = "00:00:00:00:00:00:00:16"
# DUT_SFT_ID = "200"
# DUT_HWT_ID = "0"
# DUT_PULL_CPU_PARAMETER = 5
#
# DUT_IP = '10.0.1.251'
# DUT_USER = 'manager'
# DUT_PASS = ''
# DUT_OF_INSTANCE = 'test01'
# DUT_DPID = "00:0a:74:46:a0:5f:1e:80"
# DUT_SFT_ID = "200"
# DUT_HWT_ID = "100"
# DUT_PULL_CPU_PARAMETER = 5

SERVER1 = '10.0.1.2'
SERVER1_USER = 'marian'
SERVER1_PASS = 'marian'

SERVER2 = '10.0.1.3'
SERVER2_USER = 'marian'
SERVER2_PASS = 'marian'

PING_SERVER = "10.0.3.3"
PING_TRIES = 5  # times

IPERF_SERVER = "10.0.3.3"
IPERF_TCP_DURATION = 5  # seconds
IPERF_TCP_SERVER_COMMAND = 'iperf -s'
IPERF_TCP_CLIENT_COMMAND = 'iperf -c '+IPERF_SERVER+' -t '+str(IPERF_TCP_DURATION)+' -i 1 -y C'

IPERF_UDP_DURATION = 5  # seconds
IPERF_UDP_FLOW_SPEED = 10000000 #kbit/s
IPERF_UDP_CLIENT_COMMAND = 'iperf -c %s -t '+str(IPERF_UDP_DURATION)+' -i 1 -y C -u -b '+str(IPERF_UDP_FLOW_SPEED)
IPERF_UDP_SERVER_COMMAND = 'iperf -s -u'



#======================================================= HP_SDN_VAN: RestAPI links and data structures ===============================================================================
CONTROLLER_USER = 'sdn'
CONTROLLER_PASS = 'skyline'
OPENFLOW_V = "Openflow13"
#rest_url = "https://10.0.1.117:8443/sdn/v2.0"
rest_url = "https://10.1.3.16:8443/sdn/v2.0"
auth_url = rest_url + "/auth"
datapaths_list_url = rest_url + "/of/datapaths"


fool_flows_cookie = "0xaaaadddd"
fool_flows_cookie_mask = "0xffff0000"
add_fool_flow_template={"flow":{"priority":30000,"table_id":100,"idle_timeout":0,
                            "match":[{"eth_type":"ipv4"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"}],
                            "instructions":[{"apply_actions":[{"output":"2"}]}],
                            "cookie":fool_flows_cookie,"cookie_mask":fool_flows_cookie_mask,"flow_mod_cmd":"add"}}

add_fool_flow_template={"flow":{"priority":30000,"table_id":0,"idle_timeout":0,
                            "match":[{"eth_type":"ipv4"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"}],
                            "instructions":[{"apply_actions":[{"output":"2"}]}],
                            "cookie":fool_flows_cookie,"cookie_mask":fool_flows_cookie_mask,"flow_mod_cmd":"add"}}


#{"flow":{"priority":30000,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"eth_src":"11:11:11:11:11:11"},{"eth_dst":"11:11:11:11:11:11"},{"eth_type":"ipv4"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"},{"tcp_src":"80"},{"tcp_dst":"90"}],"instructions":[{"apply_actions":[{"output":"2"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}


del_fool_flows_template = {"flow":{"priority":30000,"table_id":0xff,"match":[{"eth_type":"ipv4"},{"ipv4_src":"10.0.4.4"},{"ipv4_dst":"10.0.3.3"}],"cookie":fool_flows_cookie,"cookie_mask":fool_flows_cookie_mask}}

ping_flows_cookie = "0xaaaabbbb"
ping_flows_cookie_mask = "0xffff0000"
add_flows_for_INDIRECT_ping = {
"flow_mod_structure3_2":{"flow":{"priority":30000,"table_id":100,"idle_timeout":3000,
                            "match":[{"in_port":3},{"eth_type":"ipv4"}],
                            "instructions":[{"apply_actions":[{"output":"2"}]}],
                            "cookie":ping_flows_cookie,"cookie_mask":ping_flows_cookie_mask,"flow_mod_cmd":"add"}},
"flow_mod_structure2_11":{"flow":{"priority":30000,"table_id":100,"idle_timeout":3000,
                            "match":[{"in_port":2},{"eth_type":"ipv4"}],
                            "instructions":[{"apply_actions":[{"output":"11"}]}],
                            "cookie":ping_flows_cookie,"cookie_mask":ping_flows_cookie_mask,"flow_mod_cmd":"add"}},
"flow_mod_structure10_3":{"flow":{"priority":30000,"table_id":100,"idle_timeout":3000,
                            "match":[{"in_port":10},{"eth_type":"ipv4"}],
                            "instructions":[{"apply_actions":[{"output":"3"}]}],
                            "cookie":ping_flows_cookie,"cookie_mask":ping_flows_cookie_mask,"flow_mod_cmd":"add"}}

}

del_flows_for_INDIRECT_ping = {
    "flow_del_structure3_2":{"flow":{"priority":30000,"table_id":100,"match":[{"in_port":3},{"eth_type":"ipv4"}],"cookie":ping_flows_cookie,"cookie_mask":ping_flows_cookie_mask}},
    "flow_del_structure2_11":{"flow":{"priority":30000,"table_id":100,"match":[{"in_port":2},{"eth_type":"ipv4"}],"cookie":ping_flows_cookie,"cookie_mask":ping_flows_cookie_mask}},
    "flow_del_structure10_3":{"flow":{"priority":30000,"table_id":100,"match":[{"in_port":10},{"eth_type":"ipv4"}],"cookie":ping_flows_cookie,"cookie_mask":ping_flows_cookie_mask}}
}


add_flows_for_direct_ping = {
"flow_mod_structure3_2":{"flow":{"priority":30000,"table_id":100,"idle_timeout":3000,
                            "match":[{"in_port":3},{"eth_type":"ipv4"}],
                            "instructions":[{"apply_actions":[{"output":"2"}]}],
                            "cookie":ping_flows_cookie,"cookie_mask":ping_flows_cookie_mask,"flow_mod_cmd":"add"}},
"flow_mod_structure2_3":{"flow":{"priority":30000,"table_id":100,"idle_timeout":3000,
                            "match":[{"in_port":2},{"eth_type":"ipv4"}],
                            "instructions":[{"apply_actions":[{"output":"3"}]}],
                            "cookie":ping_flows_cookie,"cookie_mask":ping_flows_cookie_mask,"flow_mod_cmd":"add"}}
}
del_flows_for_direct_ping = {
    "flow_del_structure3_2":{"flow":{"priority":30000,"table_id":100,"match":[{"in_port":3},{"eth_type":"ipv4"}],"cookie":ping_flows_cookie,"cookie_mask":ping_flows_cookie_mask}},
    "flow_del_structure2_3":{"flow":{"priority":30000,"table_id":100,"match":[{"in_port":2},{"eth_type":"ipv4"}],"cookie":ping_flows_cookie,"cookie_mask":ping_flows_cookie_mask}}
}


#RULE 1: in_port
controller_rule_patter_1={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3}],"instructions":[{"apply_actions":[{"output":"2"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
#RULE 2: in_port, vlan_id
controller_rule_patter_2={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"100"}],"instructions":[{"apply_actions":[{"output":"2"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
#RULE 3: in_port, vlan_id, dl_vlan_pcp
controller_rule_patter_3={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"100"},{"vlan_pcp":"1"}],"instructions":[{"apply_actions":[{"output":"2"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
#RULE 4: in_port, vlan_id, dl_vlan_pcp, eth_src
controller_rule_patter_4={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_src":"11:11:11:11:11:11"}],"instructions":[{"apply_actions":[{"output":"2"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
#RULE 5: in_port, vlan_id, dl_vlan_pcp, eth_src, eth_dst
controller_rule_patter_5={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_src":"11:11:11:11:11:11"},{"eth_dst":"11:11:11:11:11:11"}],"instructions":[{"apply_actions":[{"output":"2"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
#RULE 6: in_port, vlan_id, dl_vlan_pcp, eth_src, eth_dst eth_type
controller_rule_patter_6={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_src":"11:11:11:11:11:11"},{"eth_dst":"11:11:11:11:11:11"},{"eth_type":"ipv4"}],"instructions":[{"apply_actions":[{"output":"2"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
#RULE 7: in_port, vlan_id, dl_vlan_pcp, eth_src, eth_dst eth_type, ip_src
controller_rule_patter_7={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_src":"11:11:11:11:11:11"},{"eth_dst":"11:11:11:11:11:11"},{"eth_type":"ipv4"},{"ipv4_src":"10.0.3.2"}],"instructions":[{"apply_actions":[{"output":"2"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
#RULE 8: in_port, vlan_id, dl_vlan_pcp, eth_src, eth_dst eth_type, ip_src, ip_dst
controller_rule_patter_8={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_src":"11:11:11:11:11:11"},{"eth_dst":"11:11:11:11:11:11"},{"eth_type":"ipv4"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"}],"instructions":[{"apply_actions":[{"output":"2"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
#RULE 9: in_port, vlan_id, dl_vlan_pcp, eth_src, eth_dst eth_type, ip_src, ip_dst, ip_proto
controller_rule_patter_9={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_src":"11:11:11:11:11:11"},{"eth_dst":"11:11:11:11:11:11"},{"eth_type":"ipv4"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"}],"instructions":[{"apply_actions":[{"output":"2"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
#RULE 10: in_port, vlan_id, dl_vlan_pcp, eth_src, eth_dst eth_type, ip_src, ip_dst, ip_proto, tcp_src
controller_rule_patter_10={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_src":"11:11:11:11:11:11"},{"eth_dst":"11:11:11:11:11:11"},{"eth_type":"ipv4"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"},{"tcp_src":"80"}],"instructions":[{"apply_actions":[{"output":"2"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
#RULE 11: in_port, vlan_id, dl_vlan_pcp, eth_src, eth_dst eth_type, ip_src, ip_dst, ip_proto, tcp_src, tcp_dst
controller_rule_patter_11={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"100"},{"vlan_pcp":"1"},{"eth_src":"11:11:11:11:11:11"},{"eth_dst":"11:11:11:11:11:11"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ip_ecn":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"},{"tcp_src":"80"},{"tcp_dst":"90"}],"instructions":[{"apply_actions":[{"output":"2"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
controller_rule_patter_XX={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"dl_vlan":"100"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ip_ecn":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"},{"tcp_src":"80"},{"tcp_dst":"90"}],"instructions":[{"apply_actions":[{"output":"2"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
#controller_rule_patterns_for_5700=[controller_rule_patter_1,controller_rule_patter_2,controller_rule_patter_3,controller_rule_patter_4,controller_rule_patter_5,controller_rule_patter_6,controller_rule_patter_7,controller_rule_patter_8,controller_rule_patter_9,controller_rule_patter_10,controller_rule_patter_11]
switch5700_mac_ip_rule={"flow":{"priority":65535,"table_id":10,"idle_timeout":0,"match":[{"eth_dst":"38:63:bb:58:eb:1d"},{"vlan_vid":"100"}],"instructions":[{"write_actions":[{"output":"3"}]}],"cookie":"0xffff000000000000","flow_mod_cmd":"add"}}
controller_rule_patterns_for_5700=[controller_rule_patter_1]
switch5700_rule_for_2920_1={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11}],"instructions":[{"apply_actions":[{"output":"2"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_rule_for_2920_2={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":2}],"instructions":[{"apply_actions":[{"output":"11"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_rule_for_2920_3={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":17}],"instructions":[{"apply_actions":[{"output":"3"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_rule_for_2920_4={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3}],"instructions":[{"apply_actions":[{"output":"17"}]}],"cookie":"0xaaaabbbb","cookie_mask":"0x0000ffff","flow_mod_cmd":"add"}}
switch5700_ping_rule_1={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":11}],"instructions":[{"apply_actions":[{"output":"17"}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch5700_ping_rule_2={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":17}],"instructions":[{"apply_actions":[{"output":"11"}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}




        # 1)Fields specified: in_port, else = * : MRC = 381
        # 2)Fields specified: in_port, vlan_id else = * : MRC = 381
        # 3)Fields specified: in_port, vlan_id, eth_type else = * : MRC = 1021/908
        # 4)Fields specified: in_port, vlan_id, eth_type, dst/src_ip else = * : MRC = 1526
        # 5)Fields specified: in_port, vlan_id, eth_type, dst/src_ip else, ip_protocol else = * : MRC = 1526
        # 6)Fields specified: in_port, vlan_id, eth_type, dst/src_ip else, ip_protocol, src/dst_tcp else = * : MRC = 1526

        #ovs-ofctl -O Openflow13 add-flow tcp:10.0.1.251:6633 cookie=0xaaaabbbb,table=100,priority=30000,in_port=5,action=output:2 //OFPBMC_BAD_WILDCARDS
        #ovs-ofctl -O Openflow13 add-flow tcp:10.0.1.251:6633 cookie=0xaaaabbbb,table=100,priority=30000,in_port=5,dl_vlan=5,action=output:2 //OFPBMC_BAD_WILDCARDS
        #ovs-ofctl -O Openflow13 add-flow tcp:10.0.1.251:6633 cookie=0xaaaabbbb,table=100,priority=30000,in_port=5,dl_type=800,action=output:2

ovsofctl_command_for_3500 = ""
ovsofctl_rule_patterns_for_3500=[
",table=100,in_port=2,dl_type=0x800,action=output:3",
",table=100,in_port=2,dl_vlan=0,dl_type=0x800,action=output:3",
",table=100,in_port=2,dl_vlan=0,dl_vlan_pcp=*,dl_type=0,action=output:3",
",table=100,in_port=2,dl_vlan=0,dl_vlan_pcp=*,dl_type=0x800,dl_src=*,dl_dst=*,nw_tos=0x22,action=output:3",
",table=100,in_port=2,dl_vlan=0,dl_vlan_pcp=*,dl_type=0x800,dl_src=*,dl_dst=*,nw_tos=0x22,nw_src=10.0.0.0,action=output:3",
",table=100,in_port=2,dl_vlan=0,dl_vlan_pcp=*,dl_type=0x800,dl_src=*,dl_dst=*,nw_tos=0x22,nw_src=10.0.0.0,nw_dst=10.0.1.25,action=output:3",
",table=100,in_port=2,dl_vlan=0,dl_vlan_pcp=*,dl_type=0x800,dl_src=*,dl_dst=*,nw_tos=0x22,nw_src=10.0.0.0,nw_dst=10.0.1.25,nw_proto=6,action=output:3",
",table=100,in_port=2,dl_vlan=0,dl_vlan_pcp=*,dl_type=0x800,dl_src=*,dl_dst=*,nw_tos=0x22,nw_src=10.0.0.0,nw_dst=10.0.1.25,nw_proto=6,tp_src=666,action=output:3",
",table=100,in_port=2,dl_vlan=0,dl_vlan_pcp=*,dl_type=0x800,dl_src=*,dl_dst=*,nw_tos=0x22,nw_src=10.0.0.0,nw_dst=10.0.1.25,nw_proto=6,tp_src=666,tp_dst=777,action=output:3"
]
#ovs-ofctl -O Openflow13 add-flow tcp:10.0.1.251:6633 cookie=0xaaaabbbb,table=100,in_port=2,dl_vlan=0,dl_vlan_pcp=*,dl_type=0x800,dl_src=*,dl_dst=*,nw_tos=0x22,nw_src=10.0.0.0,nw_dst=10.0.1.25,nw_proto=6,tp_src=666,tp_dst=777,action=output:3

ovsofctl_command_for_2950 = "ovs-ofctl -O Openflow10 add-flow tcp:10.1.1.13:6633 cookie=0xaaaabbbb,"
ovsofctl_rule_patterns_for_2950=[
",in_port=2,action=output:3",
",in_port=2,dl_type=0x800,action=output:3",
",in_port=2,dl_type=0x800,nw_tos=0x22,action=output:3",
",in_port=2,dl_type=0x800,nw_tos=0x22,nw_src=10.0.0.0,action=output:3",
",in_port=2,dl_type=0x800,nw_tos=0x22,nw_src=10.0.0.0,nw_dst=10.0.1.25,action=output:3",
",in_port=2,dl_type=0x800,nw_tos=0x22,nw_src=10.0.0.0,nw_dst=10.0.1.25,nw_proto=6,action=output:3",
",in_port=2,dl_type=0x800,nw_tos=0x22,nw_src=10.0.0.0,nw_dst=10.0.1.25,nw_proto=6,tp_src=666,action=output:3",
",in_port=2,dl_type=0x800,nw_tos=0x22,nw_src=10.0.0.0,nw_dst=10.0.1.25,nw_proto=6,tp_src=666,tp_dst=777,action=output:3"
]








#RULE 1: in_port
switch3500_rule_patter_1={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3}],"actions":[{"output": 2}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_patter_1_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_patter_111_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"vlan_vid":"10"}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
#RULE 2: in_port, vlan_id
switch3500_rule_patter_2={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"10"}],"actions":[{"output": 2}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_patter_2_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"10"}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
#RULE 4: in_port, vlan_id, dl_vlan_pcp, eth_type
switch3500_rule_patter_3={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"10"},{"eth_type":"ipv4"}],"actions":[{"output": 2}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_patter_33={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"eth_type":"ipv4"}],"actions":[{"output": 2}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_patter_3_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"10"},{"eth_type":"ipv4"}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
#RULE 5: in_port, vlan_id, dl_vlan_pcp, eth_type, ip_dscp
switch3500_rule_patter_4={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"10"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"}],"actions":[{"output": 2}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_patter_4_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"10"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
#RULE 6: in_port, vlan_id, dl_vlan_pcp, eth_type, ip_dscp, ipv4_src
switch3500_rule_patter_5={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"10"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"}],"actions":[{"output": 2}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_patter_5_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"10"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
#RULE 7: in_port, vlan_id, dl_vlan_pcp, eth_type, ip_dscp, ipv4_src, ipv4_dst
switch3500_rule_patter_6={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"10"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"}],"actions":[{"output": 2}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_patter_6_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"10"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
#RULE 8: in_port, vlan_id, dl_vlan_pcp, eth_type, ip_dscp, ipv4_src, ipv4_dst, ip_proto
switch3500_rule_patter_7={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"10"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"}],"actions":[{"output": 2}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_patter_7_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"10"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
#RULE 9: in_port, vlan_id, dl_vlan_pcp, eth_type, ip_dscp, ipv4_src, ipv4_dst, ip_proto, tcp_src
switch3500_rule_patter_8={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"10"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"},{"tcp_src":"80"}],"actions":[{"output": 2}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_patter_8_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"10"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"},{"tcp_src":"80"}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
#RULE 10: in_port, vlan_id, dl_vlan_pcp, eth_type, ip_dscp, ipv4_src, ipv4_dst, ip_proto, tcp_src, tcp_dst
switch3500_rule_patter_9={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"10"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"},{"tcp_src":"80"},{"tcp_dst":"90"}],"actions":[{"output": 2}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_rule_patter_9_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"vlan_vid":"10"},{"eth_type":"ipv4"},{"ip_dscp":"0x800"},{"ipv4_src":"10.0.3.2"},{"ipv4_dst":"10.0.3.3"},{"ip_proto":"tcp"},{"tcp_src":"80"},{"tcp_dst":"90"}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}

switch3500_rule_patter_10_OF13={"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"eth_type":"ipv4"},{"ipv4_src":"10.0.3.2"}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}

#switch3500_rule_patterns=[switch3500_rule_patter_1,switch3500_rule_patter_2,switch3500_rule_patter_3,switch3500_rule_patter_4,switch3500_rule_patter_5,switch3500_rule_patter_6,
#                          switch3500_rule_patter_7,switch3500_rule_patter_8,switch3500_rule_patter_9,switch3500_rule_patter_10]
switch3500_rule_patterns=[switch3500_rule_patter_3_OF13]

switch3500_ping_flow_1_OF10= {"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":3},{"eth_type":"ipv4"},{"ipv4_src":"10.0.3.3"}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_ping_flow_2_OF10= {"flow":{"priority":0,"table_id":0,"idle_timeout":0,"match":[{"in_port":2},{"eth_type":"ipv4"},{"ipv4_src":"10.0.3.2"}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_ping_flow_1_OF13= {"flow":{"priority":0,"table_id":100,"idle_timeout":0,"match":[{"in_port":3},{"eth_type":"ipv4"}],"instructions":[{"apply_actions":[{"output":2}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_ping_flow_2_OF13= {"flow":{"priority":0,"table_id":100,"idle_timeout":0,"match":[{"in_port":2},{"eth_type":"ipv4"}],"instructions":[{"apply_actions":[{"output":3}]}],"cookie":"0xaaaabbbb","flow_mod_cmd":"add"}}
switch3500_ping_flows_OF13 = [switch3500_ping_flow_1_OF13,switch3500_ping_flow_2_OF13]





