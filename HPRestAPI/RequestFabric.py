import json
import requests

import Constants

token = None
header = None
header_json = None

def getControllerAuthenticationToken(user,password):
    payload = json.dumps(
            {'Content-Type': 'application/json', "login": {"user": user, "password": password, "domain": "sdn"}})
    r = requests.post(Constants.auth_url, payload, verify=False)
    r_data = r.json()
    global token
    token = r_data["record"]["token"]
    global header
    header = {'X-Auth-Token':token}
    global header_json
    header_json = {'X-Auth-Token':token,'Content-Type':'application/json'}


def getDataPathsList():
    if token is not None:
        r = requests.get(Constants.datapaths_list_url, headers=header, verify=False)
        json = r.json()
        return json
    return None


def getDataPathFlows(dpid):
    r = requests.get(Constants.rest_url + "/of/datapaths/" + dpid + "/flows", headers=header, verify=False)
    json = r.json()
    #print r
    return json

def getDataPathFlowsForTable(dpid, table_id):
    r = requests.get(Constants.rest_url + "/of/datapaths/" + dpid + "/flows?table_id=" + str(table_id), headers=header, verify=False, timeout=3000)
    json = r.json()
    return json

def addFlow(dpid,flow):
    payload = json.dumps(flow)
    r = requests.post(Constants.rest_url + "/of/datapaths/" + dpid + "/flows", data=payload, headers=header_json, verify=False)

def deleteFlow(dpid,flow):
    payload = json.dumps(flow)
    r = requests.delete(Constants.rest_url + "/of/datapaths/" + dpid + "/flows", data=payload, headers=header_json, verify=False)

def getLinks(dpid):
    r = requests.get(Constants.rest_url + "/net/links?dpid=" + dpid, headers=header, verify=False)
    json = r.json()
    return json

def getNodesForDataPath(dpid):
    r = requests.get(Constants.rest_url + "/net/nodes?dpid=" + dpid, headers=header, verify=False)
    json = r.json()
    return json


