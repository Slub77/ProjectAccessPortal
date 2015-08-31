
import ldap

con = ldap.initialize('ldap://localhost')


print con.simple_bind_s()

print con.whoami_s()

#retrieve list of all people from ldap

base_dn='dc=example,dc=com'
filter='(objectclass=person)'
attrs=['sn']

people = con.search_s( base_dn, ldap.SCOPE_SUBTREE, filter, attrs )

print len(people)


#



con.unbind()