import json

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key, Encoding, NoEncryption, PrivateFormat, PublicFormat

import requests
from requests_http_signature import HTTPSignatureAuth

key_id = "3ed0451935d27b4f0e225486a634fe40aa3e2cfbc202efc96b174af83211189c"
key_bytes = b"""-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDnC4Kltw04TaKK
XL3skX7KhppgNA+7vxRAjshYkfftwCxy32weQOH0hIHUPylbq8QBwCeroSyNRDLj
eneDrTWEwZ+VvSeP9Mx8OBydkGndDAutBAehNFvMMMEZmdQonf63Noawcn/OeIIM
xRPU9ZH/B3mwDE9bfUIlkqSRu2WzZFXKCwjsFxXYbzlazPNAn10LKz3ggTbVM5Xi
S2g3KxHTmWs/fQ9kFw2zczKvnD7aUUfd0LTDsvXpnh1vn6FYU8CqPlnE2iv7T4+I
ZB2XanptlFrDKVb8SLmHBHbw+s54cY0FsvPB+6aUIIwhOmSsFZ592dOKa5FONP2l
YUdpLWZjAgMBAAECggEAaiZxqe1GF54jlWoyoCPgmu/osVZ5/Ao4Jcjz5y15OTRX
t5dKt0OcDJlshLVYLRPng95i24m7TFQPBVBY5JiJxCqpRUSYjp0r7c5h50pYOQS1
wJHfZ4MEwfWMYlS4ksi0JDza+OpCKfxX08If8HG61+75S5b8Rs5vu496KLJucVJC
ViGjod7j4MQD2P4cgLC9Jtwmaox25MA9BUC1AZVHddP6qlSJSLFnKCkvSx/kfivb
qWgkJdk60ylV5KKWZ+K8NtQ89eLX+GCttY2IgmoO/EYy1Alv+cDngt1HZaFFi4le
1xcaPq13lIbvrEvX4Ym+nu4lIRxXOlCLaMiVE0ACMQKBgQDz+BBS/l3+t5UNE0ma
GrnaLKWpnqqrEtLzpOJy+4TQhDNzG21WmlxE2xdy6SdJuJIixQfEMUeM20lgSyM8
zkHq70vaj1l2ZwsxZnTdPsRcuFmUH8IfecNm40fCZzQbKwM4QpxzMj90QO0uHrUb
VjO7dq8jCgQg73L+InXxU0AMLQKBgQDycEosgP4ysfwozUlRGSH62ufjIl9iaVVP
kbg/MwacFjeyRHp6bDeQQixhNipHIEgDmsSBYXyHKtQxuXCMgzCyZiSTj+Y+SJNI
tISq8mFN/1MIHrMBReA78NhRaYwcTBjL0oc/GMIlWcs/grhmYlUsvGjFjysWdna4
6knhqJSGzwKBgF6SsdlKS6ubBMeNy4FWjOcbWZi4Lhak9GuIZlQGVkTyinM7lZX1
voDeoWdlJFq6lsOtt0YBiGf89aPDXMSMfBcTbkcqPJbeeQNMYU8Grt32hJsb+Id1
Dx9KSZ39ncBOWzAq+jTZrKlnJco0EyamsuUfq+KcVl9iEySavTeweup9AoGAIjUD
0jm1JDQGzz7/7EhuifWfKGYuLTWNiveVlp09foKIA0g0O9fPEzSzDFhXKMf+QTvy
JAs8RdoeLJHstnbARTuyR3vTUdBtr6GA4pnmbtnqvkeOnExesjZuXzZURZ3bFc8z
tAxrQFfmHKT2HcQcHn7LDa0AuF+oqrisCgH+SvMCgYBX7nvnJds0zrbjuatUiZsk
YLcXOq/N6ht7XUqpfjlqjwSodauC4SdvT4cb7Fs4Pme83NYOemEExIgOjIWNpu6G
EfLwfC9n3PiORmeqIfI+EMEvhHKJZc3h9sCWV7k6cNBUR0p18P6vwQ/+cr5YN4UU
4iqeZglebSwlolY3zdLCOw==
-----END PRIVATE KEY-----
"""

if __name__ == '__main__':
  # GET
  r = requests.get('http://localhost:5900/userinfo', auth=HTTPSignatureAuth(
      algorithm='rsa-sha256', key=key_bytes, key_id=key_id, headers=['(request-target)', '(created)']))
  assert r.ok
  
  assert r.json()['key_id'] == key_id

  # POST
  r = requests.post('http://localhost:5900/userinfo', auth=HTTPSignatureAuth(
      algorithm='rsa-sha256', key=key_bytes, key_id=key_id, headers=['(request-target)', '(created)', 'digest']),
      json={'first_name': 'Ashley', 'last_name': 'Madison'})
  print(r.text)
  assert r.ok
  assert r.json()['key_id'] == key_id
  assert r.json()['first_name'] == 'Ashley'
  assert r.json()['last_name'] == 'Madison'
