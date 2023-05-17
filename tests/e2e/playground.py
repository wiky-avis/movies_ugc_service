import jwt

payload = dict()
payload["user_id"] = "1ff75749-a557-44e4-a99e-4cbe2ca77534"

secret = """"12345"""

token = jwt.encode(payload, secret, algorithm="HS256")

print(token)
