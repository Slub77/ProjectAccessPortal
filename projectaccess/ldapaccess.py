
from django.conf import settings

import ldap

def retrieve_users_from_ldap_server():
    ldap_connection = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
    ldap_search = settings.IMPORT_LDAP_USER_SEARCH
    people = ldap_search.execute(ldap_connection)
    return people

def retrieve_users_from_ldif_file():

    def append_user_if_person(users, user_dn, user_attrs):
        if user_dn and user_attrs:
            if 'objectClass' in user_attrs and 'person' in user_attrs['objectClass']:
                users.append((user_dn, user_attrs))

    users = []

    user_dn = None
    user_attrs = None

    for line in open('tests/ldap/Example2.ldif').readlines():
        stripped_line = line.strip()
        if stripped_line.startswith('#'):
            pass
        elif not stripped_line:

            append_user_if_person(users, user_dn, user_attrs)

            user_dn = None
            user_attrs = None
        else:
            (key, value) = stripped_line.split(': ', 1)

            if key == 'dn':
                user_attrs = {}
                user_dn = value
            else:
                if not key in user_attrs:
                    user_attrs[key] = []
                user_attrs[key].append(value)

    append_user_if_person(users, user_dn, user_attrs)

    return users

def retrieve_ldap_users():
    if settings.LDAP_IMPORT_USERS_FROM_SERVER:
        return retrieve_users_from_ldap_server()
    else:
        return retrieve_users_from_ldif_file()