import requests
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmVzIjoxNjcxNzM5ODEzLjIyOTg4NjgsInVzZXJuYW1lIjoiYWRtaW4yIiwicGFzc3dvcmQiOiJhZG1pbiJ9.zz4kW_3DpP9de8dhcpwZgBuQ7c6gHD_w9ikclrJto6I'
headers = {
    'Authorization': f'Bearer {token}'
}
body = {
    'id': 11,
    'title': '666',
    'color_scheme': 1
}

resp = requests.post('http://localhost:8000/api/update_group',
                     headers=headers,
                     json=body
                     )
print(resp.status_code)