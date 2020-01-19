# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import json
import requests

class Auth():
#{
	def __init__(self, certificate, key, auth_server="auth.iudx.org.in", version=1):
	#
		self.url		= "https://" + auth_server + "/auth/v" + str(version)
	        self.credentials	= (certificate, key)
	#

	def call(self, api, body=None):
	#
		ret = "success"

		body = json.dumps(body)

		response = requests.post (
			url	= self.url + "/" + api,
			verify	= True,
			cert	= self.credentials,
			data	= body,
			headers	= {"content-type":"application/json"}
		)

		if response.status_code != 200:
		#
			sys.stderr.write (
				"WARNING: auth API failure  | "	+
				self.url + "/" + api	+ " | "	+
				response.reason 	+ " | "	+
				response.text
			)

			ret = "failed"
		#

		if response.headers['content-type'] == 'application/json':
			return [ret, json.loads(response.text)]
		else:
		#
			sys.stderr.write (
				"WARNING: auth did not send 'application/json'"
			)

			return ["failed", None]
		#
	#

	def get_token(self, request, token_time=None, existing_token=None):
	#
		body = {'request': request}

		if token_time:
			body['token-time'] = token_time

		if existing_token:
			body['existing-token'] = existing_token

		return self.call("token", body)
	#

	def get_policy(self):
		return self.call("acl")

	def set_policy(self, policy):
        	body = {'policy': policy}
		return self.call("acl/set", body)

	def append_policy(self, policy):
		body = {'policy': policy}
		return self.call("acl/append", body)

	def introspect_token(self, token, server_token=None):
	#
		body = {'token': token}

		if server_token:
			body['server-token'] = server_token

		return self.call("token/introspect", body)
	#

	def revoke_tokens(self, tokens):
	#
		if type(tokens) is type([]):
			body = {'tokens': tokens}
		else:
			body = {'tokens': [tokens]}

        	return self.call("token/revoke", body)
	#

	def revoke_token_hashes(self, token_hashes):
	#
		if type(token_hashes) is type([]):
			body = {'token-hashes': token_hashes}
		else:
			body = {'token-hashes': [token_hashes]}

		return self.call("token/revoke", body)
	#

	def audit_tokens(self, hours):
		body = {'hours': hours}
		return self.call("audit/tokens", body)

	def add_consumer_to_group(self, consumer, group, valid_till):
		body = {'consumer': consumer, 'group': group, 'valid-till' : valid_till}
		return self.call("group/add", body)

	def delete_consumer_from_group(self, consumer, group):
		body = {'consumer': consumer, 'group': group}
		return self.call("group/delete", body)

	def list_group(self, consumer, group=None):
	#
		body = {'consumer': consumer}

		if group:
			body['group'] = group

		return self.call("group/list", body)
	#
#}