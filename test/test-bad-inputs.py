# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import os

from init import provider 
from init import provider 
from init import resource_server

RS = "iisc.iudx.org.in"

policy = "x can access *" # dummy policy
provider.set_policy(policy)

invalid_policy = "invalid policy *"
assert provider.set_policy(invalid_policy)['success'] is False

r = provider.get_policy()['response']['policy']
assert policy in r
assert invalid_policy not in r

invalid_policy = "invalid policy *"
assert provider.append_policy(invalid_policy)['success'] is False

r = provider.get_policy()['response']['policy']
assert policy in r
assert invalid_policy not in r
