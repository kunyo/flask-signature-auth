from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat, PublicFormat
from flask import Flask, jsonify, request
from flask_signature_auth import FlaskSignatureAuth
from flask_testing import LiveServerTestCase

import requests
from requests_http_signature import HTTPSignatureAuth

priv_key = rsa.generate_private_key(
    public_exponent=65537, key_size=2048, backend=default_backend())


class PublicKeyAuthenticationTestCaseLive(LiveServerTestCase):
  def create_app(self):
    app = Flask(__name__)
    app.config['TESTING'] = True
    # Default port is 5000
    app.config['LIVESERVER_PORT'] = 8943
    # Default timeout is 5 seconds
    app.config['LIVESERVER_TIMEOUT'] = 10
    app.debug = True

    auth = FlaskSignatureAuth(
        key_bytes=priv_key.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo))

    @app.route('/authorize/challenge', methods=['POST'])
    def get_challenge():
      content_type = request.headers.get('Content-Type')
      if content_type != 'application/jwk+json':
        return 'invalid_request', 400

      try:
        public_key = jwk.JWK(**dict(request.json['publicKey']))
      except (KeyError, ValueError):
        return 'invalid_request', 400

      challenge = pubkey_auth.get_challenge(public_key)
      return jsonify({'challenge': challenge}), 200

    @app.route('/authorize/key', methods=['POST'])
    def authorize_key():
      try:
        key_id, public_key = pubkey_auth.verify_challenge(
            **request.json)
        raise Exception("blah")
        return jsonify({'key_id': key_id}), 200
      except ChallengeVerificationError:
        return '', 400

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

    @app.route('/')
    def home():
      return '', 200

    return app

  def test_server_is_up(self):
    r = requests.get(self.get_server_url())
    self.assertEqual(r.status_code, 200)

  def test_httpget_signature_auth_with_valid_credential(self):
    key_id = "test-key-id"
    priv_key_bytes = priv_key.private_bytes(
        encoding=Encoding.PEM, format=PrivateFormat.PKCS8, encryption_algorithm=NoEncryption())
    r = requests.get(self.get_server_url() + '/userinfo', auth=HTTPSignatureAuth(
        algorithm='rsa-sha256', key=priv_key_bytes, key_id=key_id, headers=['(request-target)', '(created)']))
    self.assertEqual(r.status_code, 200)
    self.assertEqual(r.json()['key_id'], key_id)

  def test_httppost_signature_auth_with_valid_credential(self):
    key_id = "test-key-id"
    first_name = "Test First Name"
    last_name = "Test Last Name"
    priv_key_bytes = priv_key.private_bytes(
        encoding=Encoding.PEM, format=PrivateFormat.PKCS8, encryption_algorithm=NoEncryption())
    r = requests.post(self.get_server_url() + '/userinfo', auth=HTTPSignatureAuth(
        algorithm='rsa-sha256', key=priv_key_bytes, key_id=key_id, headers=['(request-target)', '(created)', 'digest']),
        json={'first_name': first_name, 'last_name': last_name})
    self.assertEqual(r.status_code, 200)
    self.assertEqual(r.json()['key_id'], key_id)
    self.assertEqual(r.json()['first_name'], first_name)
    self.assertEqual(r.json()['last_name'], last_name)
