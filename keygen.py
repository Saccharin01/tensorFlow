import json

json_path = 'athletes_data.json'

with open(json_path, "r") as f:
  jsondata = json.load(f)
  

print(len(jsondata))

class_list = []
for item in jsondata:
  class_list.extend(item.keys())
  
key_to_remove = "img"
class_list = [key for key in class_list if key != key_to_remove]
class_list = list(set(class_list))

print(class_list)