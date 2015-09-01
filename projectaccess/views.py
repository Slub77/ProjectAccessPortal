from django.http import HttpResponse
from django.template import RequestContext, loader

import random
from P4 import P4, P4Exception

import ldap

class p4_connection():
    def __enter__(self):
        p4 = P4()                        # Create the P4 instance
        self.p4 = p4
        p4.host = "localhost"
        p4.port = "1666"
        p4.user = "kalms"
        p4.connect()                   # Connect to the Perforce server
        return p4

    def __exit__(self, type, value, traceback):
        self.p4.disconnect()

def get_users_from_p4():
    with p4_connection() as p4:
        users = p4.run("users")
    return users

def generate_random_users(count):

    def generate_random_user():
        id = random.randint(0, 999999)
        return {
            'id': str(id),
            'name': 'user_name_' + str(id),
            'email': 'firstname_lastname_' + str(id)
            }

    users = [generate_random_user() for i in range(count)]
    
    return users

def find_p4_user_with_email(p4_users, email):
    for p4_user in p4_users:
        if p4_user['Email'] == email:
            return p4_user

    return None

def combine_users(ldap_users, p4_users):

    combined_users = []

    for ldap_user in ldap_users:
        ldap_user_email = ldap_user['mail']
        p4_user = find_p4_user_with_email(p4_users, ldap_user_email)
        if p4_user:
            combined_user = { 'ldap': ldap_user, 'p4': p4_user}
            combined_users.append(combined_user)
        else:
            combined_user = { 'ldap': ldap_user, 'p4': None}
            combined_users.append(combined_user)

    for p4_user in p4_users:
        p4_user_email = p4_user['mail']
        ldap_user = find_ldap_user_with_email(ldap_users, p4_user_email)
        if not ldap_user:
            combined_user = { 'ldap' : ldap_user, 'p4' : p4_user}
            combined_users.append(combined_user)

    pass

def index(request):

    from updateldap import updateldap

    updateldap()

    p4_users = get_users_from_p4()

    users = generate_random_users(10)
    template = loader.get_template('users.html')
    context = RequestContext(request, {
        'users': users,
    })
    return HttpResponse(template.render(context))
