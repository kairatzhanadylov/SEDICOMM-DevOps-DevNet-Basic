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

netconf_data = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"> 
  <interface> 
   <Loopback> 
    <name>111</name> 
    <description>TEST1</description> 
    <ip> 
     <address> 
      <primary> 
       <address>100.100.100.100</address> 
       <mask>255.255.255.0</mask> 
      </primary> 
     </address> 
    </ip> 
   </Loopback> 
  </interface> 
 </native> 
</config>
"""

netconf_config = to_ele(netconf_data)

netconf_reply = m.edit_config(target="running", config=netconf_config)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

