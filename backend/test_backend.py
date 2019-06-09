import requests
# using requests library to test backend without using frontend

def query():
    response = requests.get('http://localhost:5000/todo_db')
    print(response.json())

# data = {'content':'change a old todo ', 'done':True, 'id':1}
# response = requests.post('http://localhost:5000/upload_file', json= data)
# print(response)



# query()

# # add new item
# data = {'content':'add a new todo ', 'done':False}
# response = requests.post('http://localhost:5000/todo_db', json= data)
# query()

# # update the old item
# data = {'content':'change a old todo ', 'done':True, 'id':1}
# response = requests.post('http://localhost:5000/todo_db', json= data)
# query()

# # remove item
# data = {'delete': True, 'id':2}
# response = requests.post('http://localhost:5000/todo_db', json= data)
# query()


query()
# query file_entry
response = requests.get('http://localhost:5000/upload_file')
print(response.json())
