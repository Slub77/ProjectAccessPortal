
from django.conf import settings

import ldap

def retrieve_ldap_users():
    ldap_connection = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
    ldap_search = settings.IMPORT_LDAP_USER_SEARCH
    people = ldap_search.execute(ldap_connection)
    return people
