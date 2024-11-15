import json

data = [{"role":"user","parts":["hello"],},{"role":"model","parts":["hiii how are you"]}]

with open(r'D:\python programs\discord bot\memory.json', 'w') as history:
    json.dump(data,history,indent=4)




with open(r'D:\python programs\discord bot\memory.json', 'r') as history:
    load=json.load(history)


print(load)