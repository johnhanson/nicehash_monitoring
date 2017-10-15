# todo: some way to automate/automatically update this

algo = dict([
    (0, 'Scrypt'),
    (1, 'SHA256'),
    (2, 'ScryptNf'),
    (3, 'X11'),
    (4, 'X13'),
    (5, 'Keccak'),
    (6, 'X15'),
    (7, 'Nist5'),
    (8, 'NeoScrypt'),
    (9, 'Lyra2RE'),
    (10, 'WhirlpoolX'),
    (11, 'Qubit'),
    (12, 'Quark'),
    (13, 'Axiom'),
    (14, 'Lyra2REv2'),
    (15, 'ScryptJaneNf16'),
    (16, 'Blake256r8'),
    (17, 'Blake256r14'),
    (18, 'Blake256r8vnl'),
    (19, 'Hodl'),
    (20, 'DaggerHashimoto'),
    (21, 'Decred'),
    (22, 'CryptoNight'),
    (23, 'Lbry'),
    (24, 'Equihash'),
    (25, 'Pascal'),
    (26, 'X11Gost'),
    (27, 'Sia'),
    (28, 'Blake2s'),
    (29, 'Skunk')
])

# got this from https://www.nicehash.com/profitability-calculator
# couldn't find it in the API, except in the stats.provider.ex call
# might be wrong
speed = dict([
    (0, 'MH/s'),
    (1, 'TH/s'),
    (2, 'MH/s'),
    (3, 'MH/s'),
    (4, 'MH/s'),
    (5, 'MH/s'),
    (6, 'MH/s'),
    (7, 'MH/s'),
    (8, 'MH/s'),
    (9, 'MH/s'),
    (10, 'MH/s'),
    (11, 'MH/s'),
    (12, 'MH/s'),
    (13, 'kH/s'),
    (14, 'MH/s'),
    (15, 'kH/s'),
    (16, 'GH/s'),
    (17, 'GH/s'),
    (18, 'GH/s'),
    (19, 'kH/s'),
    (20, 'MH/s'),
    (21, 'GH/s'),
    (22, 'kH/s'),
    (23, 'GH/s'),
    (24, 'Sol/s'),
    (25, 'GH/s'),
    (26, 'MH/s'),
    (27, 'GH/s'),
    (28, 'GH/s'),
    (29, 'MH/s')
])

# in seconds
fast = 60 * 1 -1
slow = 60 * 5 -1
refresh_rate = dict([
    ('Axiom',           slow),
    ('Blake256r14',     slow),
    ('Blake256r8',      slow),
    ('Blake256r8vnl',   slow),
    ('Blake2s',         fast),
    ('CryptoNight',     fast),
    ('DaggerHashimoto', fast),
    ('Decred',          fast),
    ('Equihash',        fast),
    ('Hodl',            slow),
    ('Keccak',          fast),
    ('Lbry',            slow),
    ('Lyra2RE',         slow),
    ('Lyra2REv2',       fast),
    ('NeoScrypt',       fast),
    ('Nist5',           fast),
    ('Pascal',          slow),
    ('Quark',           slow),
    ('Qubit',           slow),
    ('SHA256',          slow),
    ('Scrypt',          slow),
    ('ScryptJaneNf16',  slow),
    ('ScryptNf',        slow),
    ('Sia',             fast),
    ('Skunk',           slow),
    ('WhirlpoolX',      slow),
    ('X11',             slow),
    ('X11Gost',         fast),
    ('X13',             slow),
    ('X15',             slow)
])

def get_algo():
    return algo

def num_to_algo(num):
    return algo[num]

def get_speed():
    return speed

def num_to_speed(num):
    return speed[num]

def algo_to_refresh_rate(algo):
    return refresh_rate[algo]