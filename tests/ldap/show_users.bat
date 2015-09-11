REM display all person-objects that exist in LDAP directory

ldapsearch -x -b "" -s sub "(objectclass=person)"