import requests

endpoint = 'http://localhost:8000/my_customers_list/36/update/api_home/'

# endpoint = 'http://localhost:8000/custom_create?pesel=42'

# response_get = requests.get(endpoint)
response_put = requests.put(endpoint, json={"last_name": "Hughes12344", "adress": {"city" : "Grad123"}})

# print(response_get.text)
print(response_put.text)