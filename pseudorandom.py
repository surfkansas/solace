#!/usr/bin/env python3

import random 

results = {
    '00': 0,
    '01': 0,
    '10': 0,
    '11': 0
}

for i in range(100):
    random_number = random.randint(0,3)
    results['{0:#010b}'.format(random.randint(0,3))[8:]] += 1

print()
print('Pseudo-random completed with the following measurements:')
print()
print('  measurement ║    count    ')
print(' ═════════════╬═════════════')
for key in sorted(results):
    print(f'      {key}      ║     {results[key]}')
print()