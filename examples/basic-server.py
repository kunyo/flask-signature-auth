from flask import Flask, request, jsonify
from flask_signature_auth import FlaskSignatureAuth

public_key_id = "3ed0451935d27b4f0e225486a634fe40aa3e2cfbc202efc96b174af83211189c"
public_key = b'''
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5wuCpbcNOE2iily97JF+
yoaaYDQPu78UQI7IWJH37cAsct9sHkDh9ISB1D8pW6vEAcAnq6EsjUQy43p3g601
hMGflb0nj/TMfDgcnZBp3QwLrQQHoTRbzDDBGZnUKJ3+tzaGsHJ/zniCDMUT1PWR
/wd5sAxPW31CJZKkkbtls2RVygsI7BcV2G85WszzQJ9dCys94IE21TOV4ktoNysR
05lrP30PZBcNs3Myr5w+2lFH3dC0w7L16Z4db5+hWFPAqj5ZxNor+0+PiGQdl2p6
bZRawylW/Ei5hwR28PrOeHGNBbLzwfumlCCMITpkrBWefdnTimuRTjT9pWFHaS1m
YwIDAQAB
-----END PUBLIC KEY-----
'''
auth = FlaskSignatureAuth(key_bytes=public_key)
app = Flask(__name__)


@app.route('/userinfo', methods=['GET'])
@auth.auth_required()
def get_userinfo():
  return jsonify({'key_id': auth.current_user().key_id}), 200


@app.route('/userinfo', methods=['POST'])
@auth.auth_required()
def change_userinfo():

  if not request.is_json:
    return '', 400

  return jsonify({
      'key_id': auth.current_user().key_id,
      'first_name': request.json['first_name'],
      'last_name': request.json['last_name']
  }), 200


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5900)
