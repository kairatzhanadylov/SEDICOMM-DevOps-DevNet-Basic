from ncclient import manager

m = manager.connect(
    host="192.168.56.101",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False,
)

file = open("lab27_capabilities.txt", "w")

print("# Supported Capabilities (YANG models):\n")
file.write("# Supported Capabilities (YANG models):\n\n")

for capability in m.server_capabilities: # type: ignore
    print(capability)
    file.write(capability + "\n")

file.close()

