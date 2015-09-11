REM import LDAP directory from .ldif file

ldapmodify -a -x -w secret -D "cn=Manager" -f Example2.ldif
