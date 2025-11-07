# file=open("devices.txt","r")
# for item in file:
#     print(item)
# file.close()

# file=open("devices.txt","r")
# for item in file:
#    item=item.strip()
#    print(item)
# file.close()

# devices=[]
# file=open("devices.txt","r")
# for item in file:
#    item=item.strip()
#    devices.append(item)
# file.close()
# print(devices)

devices=[]
file=open("devices.txt","a")
while True:
    newItem=input("Enter device name or type 'exit' to stop: ")
    if newItem.lower()=='exit':
        print("All done!")
        break
    else:
        file.write(newItem+"\n")

