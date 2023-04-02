import requests

BASE = "http://127.0.0.1:5000/"

headers = {'Content-Type': 'application/json'}
data = [{'Name': 'Ishaan', 'Views': 100, 'Likes': 10},
        {'Name': 'Lavanya', 'Views': 69000, 'Likes': 10001},
        {'Name': 'Patu', 'Views': 10000, 'Likes': 998}]

for i in range(len(data)):
    response = requests.put(BASE + "video/"+str(i), json=data[i], headers=headers)
    print(response.json())

response = requests.get(BASE + "video/0")
print(response.json())
response = requests.get(BASE + "video/1")
print(response.json())
response = requests.get(BASE + "video/6")
print(response.json())

response = requests.patch(BASE + "video/1", json={'Views':99}, headers=headers)
print(response.json())