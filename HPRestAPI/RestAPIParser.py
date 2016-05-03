from Monitor.Models import PhysicalLink


def getDataPathsList(json):
    if 'datapaths' in json:
        dps = []
        for dp in json['datapaths']:
            id = dp['dpid']
            dps.append(id)
        return dps
    return None

def getDataPathFlowsCountForAllTables(json):
    tables_flows_count = {}
    try:
        flows = json['flows']
        for flow in flows:
            if tables_flows_count.__contains__(flow['table_id']):
                tables_flows_count[flow['table_id']] = tables_flows_count[flow['table_id']]+1
            else:
                tables_flows_count[flow['table_id']] = 1
        return tables_flows_count
    except:
        return tables_flows_count


def parseLinks(src_dpid, json):
    res = []
    if 'links' in json:
        links = json["links"]
        for l in links:
            if l["src_dpid"] == src_dpid:
                pl = PhysicalLink.PhysicalLink(l["src_dpid"], l["src_port"], l["dst_dpid"], l["dst_port"])
                res.append(pl)
        return res



