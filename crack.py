# Daria Agadzhanova
# CSC 483
# Project 2
import hashlib
import binascii
import os
import sys
import itertools as it
import random

input_chars = ''
for i in range(32, 127):
    input_chars += (chr(i))


#unpacking the file
file_name  = sys.argv[1]

file = open(file_name, 'r')
print('opened file')
lines = file.readlines()
approach = lines[0].strip()
message = lines[1].strip()
salt = lines[2].strip()
password_hash = lines[3].strip()


# hashes password to compare with the given hash value
def hash_password(password_guess, salt):
    password_str = ''.join(password_guess)
    hashed = hashlib.pbkdf2_hmac('sha256', password_str.encode(), binascii.unhexlify(salt), 100000)
    return binascii.hexlify(hashed).decode()


# dictionary attack method, tries every word from the dictionary file
def dictionary_attack(password_hash, salt):
    try:
        dict_file = open('/usr/share/dict/words')
    except:
        print("Error: Unable to locate file")
        exit()

    dict_lines = dict_file.readlines()
    for line in dict_lines:
        line = line.strip()
        print(line)
        if hash_password(line, salt.encode()) == password_hash:
            return "The password is " + line
    return "Password not found in the dictionary"


# brute force attack, tries all possible combinations of passwords from length 6 to 16 by default
def brute_force(password_hash, salt, min, max):
    for k in range(min, max + 1):
        for comb in it.combinations_with_replacement(input_chars, k):
            print(''.join(comb))
            if hash_password(comb, salt.encode()) == password_hash:
                print('Password is: ' + ''.join(comb))
                return ''.join(comb)
    return 'Password not found, try different length'


# brute force attack using random characters
def random_force(length, password_hash, salt):
    pass_guess = ''
    for k in range(length):
        pass_guess += chr(random.randrange(33, 127))
    if hash_password(pass_guess, salt.encode()) == password_hash:
        print('Password is: ' + ''.join(pass_guess))
        return ''.join(pass_guess)


def find_stars(message):
    indices = []
    for i in range(len(message)):
        if message[i] == '*':
            indices.append(i)
    return indices


def prior_knowledge(message, password_hash, salt):
    stars = find_stars(message)
    length = len(stars)
    print(length)
    message = list(message)
    for comb in it.combinations_with_replacement(input_chars, length):
        for k in range(length):
            message[stars[k]] = comb[k]
            print(message)
        if hash_password(message, salt.encode()) == password_hash:
            print('Password is:' + ''.join(message))
            return ''.join(message)
    return 'Password not found'






# runs cracking functions
def may_the_force_be_with_you(approach):
    if approach == '1':
        brute_force(password_hash, salt, 6, 16)
    elif approach == '2':
        dictionary_attack(password_hash, salt)
    elif approach == '3':
        prior_knowledge(message, password_hash, salt)


may_the_force_be_with_you(approach)
