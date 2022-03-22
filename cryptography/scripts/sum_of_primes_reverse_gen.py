#!/usr/bin/python3

from Crypto.Util.number import inverse, long_to_bytes
import gmpy2

x = 0x1b1fb4b96231fe1b723d008d0e7776169ee5d4a8e3573c12c37721cee5de1d882f040d1e3f543d36a574984ad95c1e79e02de14fa136b4be7f4468cbd62773f6a4fd06effc2b845ca07424100466bdfeee652d78b25a4273ba4e950e1a8ebfe256a2f8541fe2207c41f39c2363e23064bc56bed5cf563b8dba873da3c1320256e
n = 0xb6b2353316c7b0a6c0ecae3bd7d2191eee519551f4ed86054e6380663668e595f6f43f867caa8feda217905643d73453f3797f6096c989fd099852239e5d73c753f909d8efd172d211a4ed4a966dbcbf56b9cbadd416de0a3472a253571b4e4f1bab847a407a27eb37449488f63aedb9f5ec72d9e331ab6154fe45c8cb4e2005d124d1ac8ecd588cd2280e215b078d8ea9da438bbcb1b155a339b91f39e3d17bab112436cdbb6d104fdeb0dce1ac41a1fe8fda0490ef3124794e0383565c299df24ad8a915669469c0b0dc604ed359afb3636d5f633362d8ef9fce7a42f64d5f1f4e50911a15459f97c1b11ee44af4e8bb636895cf75da105a8d1564160ba091
c = 0x49e426aba3431d9bb73bfc5dd18115dcea3c78a9915e9cf65e060560015c951327f20fe5dd74bfecd9a00659d4f740e42f707e47d8f6b331d8ad1021de41e15f133cbe7c782f22168149df57a6c37095ba6877765a67d8478434a7a5eabb26097404ad464fa0388cacb97a26aaf3b83b6eb0fa73e16bc1de49b33ee64920118f8483feff3634541df97dadad88302392095059cbe56e7148453f16464da8be2b6ca4a6fc0052210f697975fd3c4f3f94bfa3bb2422124a6f0e9685f0440ed020294b6788d7ea3c002d86d86faced8e37b36673ea2b5c72726c66d1834d2dcafdf40220c41dfb3d1f07c5c0d236ce7af86b937476c5aabe33cae8d535713627de

# x is the sum of the primes
# n is the product of the primes
# c is the ciphertext

e = 65537

# delta is the square root of (x^2 - 4(n))
delta = gmpy2.isqrt(x**2 - 4*n)

# Calculate p and q with delta
# adds delta to the sum, then divides by two
p = gmpy2.c_div(gmpy2.add(x, delta), 2)
# subtracts delta from the sum (by adding a negative delta), then divides by two
q = gmpy2.c_div(gmpy2.add(x, gmpy2.mpz(-1)*delta), 2)

# Start general RSA stuff
phi = (p - 1) * (q - 1)
d = inverse(e, phi)
m = pow(c, d, n)

# Convert m (plaintext in numbers) to text
plaintext = long_to_bytes(m)
print(plaintext.decode())
