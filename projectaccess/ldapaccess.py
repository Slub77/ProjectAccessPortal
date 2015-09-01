
import ldap

def retrieve_ldap_users():
    con = ldap.initialize('ldap://localhost')
    con.simple_bind_s()
    base_dn='dc=example,dc=com'
    filter='(objectclass=person)'
    attrs=['uid', 'cn', 'mail']

    people = con.search_s( base_dn, ldap.SCOPE_SUBTREE, filter, attrs )
    return people
