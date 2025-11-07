from ncclient import manager
from ncclient.xml_ import to_ele
import xml.dom.minidom
import xmltodict

m = manager.connect(
    host="192.168.56.101",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False,
)

netconf_filter = """
<interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
"""

netconf_reply = m.get(filter=('subtree', to_ele(netconf_filter)))
netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

for interface in netconf_reply_dict['rpc-reply']['data']['interfaces-state']['interface']:
    print("Name: {}: MAC: {} Input: {} Output: {}".format(
        interface['name'],
        interface.get('phys-address', 'N/A'),
        interface['statistics']['in-octets'],
        interface['statistics']['out-octets']
    ))

