# Daria Agadzhanova
# CSC 483
# Project 2


import secrets


class Mercenne:

    def __init__(self):
        self.N = 624
        self.M = 397
        self.A = 0x9908b0df
        self.UPPER = 0x80000000
        self.LOWER = 0x7fffffff
        self.mi = self.N
        self.m = [0 for i in range(self.N)]
        self.s = ''
        for i in range(32, 127):
            self.s += chr(i)

    def orders(self, letter):
        return self.s.find(letter)

    # modified set_seed, no pre-computing
    def set_seed(self,seed, i):
        global mi
        self.m[0] = seed & 0xffffff

        self.m[i] = (69069 * self.m[i - 1]) & 0xffffffff
        mi = self.N

    # modified next_int, computes each integer on demand
    def next_int(self,k):
        global mi
        if mi >= self.N:
            # for k in range(0, N):
            y = (self.m[k] & self.UPPER) | (self.m[(k + 1) % self.N] & self.LOWER)
            if y % 2 == 0:
                self.m[k] = self.m[(k + self.M) % self.N] ^ (y >> 1)
            else:
                self.m[k] ^= self.A
    # print("This is m: " + str(m))
        mi = 0
        y = self.m[mi]
        mi += 1
        y ^= (y >> 11)
        y ^= ((y << 7) & 0x9d2c5680)
        y ^= ((y << 15) & 0xefc60000)
        y ^= (y >> 18)
        # print("This is y :" + str(y))
        return y

    # encrypts a message, using one time pad encryption
    def encrypt(self,plaintext, secret_key, init_vector):
        pad = []

        seed = secret_key ^ init_vector
        # set_seed(seed)
        cypher_text = []
        for i in range(0, len(plaintext)):
            self.set_seed(seed, i + 1)
            pad.append(self.next_int(i))
                # (mi+pi)%|S| m message p pad S charset

            c = (self.orders(plaintext[i]) + pad[i]) % len(self.s)  # TODO fix S len
            cypher_text.append(c)
        print(cypher_text)
        return cypher_text

    # decrpyts given cypher text
    def decrypt(self, cypher, secret_key, init_vector):
        pad = []
        seed = secret_key ^ init_vector
        # set_seed(seed)
        plain_text = []

        for i in range(0, len(cypher)):
            self.set_seed(seed, i + 1)

            pad.append(self.next_int(i))
            p = (cypher[i] - pad[i]) % len(self.s)
            plain_text.append(self.s[p])

        print(''.join(plain_text))
        return plain_text


    def eavesdrop_try(self,init_vector, cypher_text):
        pad = []
        secret_key_guess = secrets.randbits(32)
        seed_guess = secret_key_guess ^ init_vector
        plain_text_guess = []

        for i in range(0, len(cypher_text)):
            self.set_seed(seed_guess, i + 1)

            pad.append(self.next_int(i))

            p = (cypher_text[i] - pad[i]) % len(self.s)
            plain_text_guess.append(self.s[p])

        return ''.join(plain_text_guess)

    def eavesdrop(self, init_v, cypher_text):
        found_pass = False
        while not found_pass:
            try_pass = self.eavesdrop_try(init_v, cypher_text)
            print(try_pass)
            if mr.encrypt(''.join(try_pass), secret_key,init_vector) == cypher_text:
                print("Password is " + ''.join(try_pass))
                return ''.join(try_pass)
        print('Message not found')

    # checks is a message is valid assuming it is text
    def is_valid_message(self,input_string):
        try:
            dict_file = open('/usr/share/dict/words')

        except:
            print("Error: Unable to locate file")
            exit()

        dict_lines = dict_file.readlines()
        input_list = input_string.split(' ')
        print(input_list)
        for word in input_list:
            for line in dict_lines:
                if line.lower() == word.lower():
                    return True
        return False

if __name__ == "__main__":
    mr = Mercenne()
    secret_key = secrets.randbits(32)

    init_vector = secrets.randbits(32)
    cip = mr.encrypt('hello world',secret_key,init_vector)
    on = mr.decrypt(cip,init_vector,secret_key)
    mr.eavesdrop(init_vector, cip)

