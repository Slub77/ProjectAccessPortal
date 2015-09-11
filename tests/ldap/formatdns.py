# Formatting logic for LDAP export, for delete purposes:
# Only keep lines which begin with dn:
# For these lines, remove the dn: prefix
# Print all entries in reverse order

import sys

prefix = 'dn: '

lines = sys.stdin.readlines()

for line in reversed(lines):
    if line.startswith(prefix):
        dn = line[len(prefix):-1]
        dn_with_escaped_spaces = dn.replace(' ', '\\ ')
        print dn_with_escaped_spaces
