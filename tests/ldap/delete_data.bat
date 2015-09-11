REM Remove all entries from LDAP directory

ldapsearch -x -b "" -s sub "(objectclass=*)" | python formatdns.py | ldapdelete -c -v -x -w secret -D "cn=Manager"
