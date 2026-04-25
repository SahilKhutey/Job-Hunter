from jose import jwt
import json

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc3MDIzNDk1LCJpYXQiOjE3NzcwMjI1OTUsIm5iZiI6MTc3NzAyMjU5NX0.mW2U_TBZB7D3sUVYRhRdl4Sf1XbulramsneEdw0Eg0k"
secret = "your_jwt_secret_here"
algo = "HS256"

try:
    payload = jwt.decode(token, secret, algorithms=[algo])
    print(json.dumps(payload, indent=2))
except Exception as e:
    print(f"Error: {e}")
