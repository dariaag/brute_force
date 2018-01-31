import secrets
from mercenne import Mercenne

mr = Mercenne()
secret_key = secrets.randbits(32)

init_vector = secrets.randbits(32)
cip = mr.encrypt('hello world', secret_key, init_vector)
on = mr.decrypt(cip, init_vector, secret_key)
mr.eavesdrop(init_vector, cip)
