
contacts = {
    'number': 4,
    'students':
        [
            {'name': 'Sarah Holderness', 'email': 'sarah@example.com'},
            {'name': 'Ndeye Penda Sow', 'email': 'ndeyepsow@example.com'},
            {'name': 'Jimi Woddey', 'email': 'jwoddey@example.com'},
            {'name': 'Ron Weasley', 'email': 'ron@example.com'}
        ]
}

print('Student emails:')
for student in contacts['students']:
    print(student['email'])

import requests
print("Requests version:", requests.__version__)

response = requests.get("https://httpbin.org/get")
print("Status code:", response.status_code)
print("Response JSON:", response.json())
