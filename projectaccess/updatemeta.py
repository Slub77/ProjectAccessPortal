
from models import P4User, LDAPUser, MetaUser

import logging
logger = logging.getLogger(__name__)

def clear_meta_users():
    MetaUser.objects.all().delete()

# List all LDAP and P4 users, and concile them into meta-users

def construct_meta_users_from_real_users():

    remaining_ldap_users = {}
    remaining_p4_users = {}

    meta_users = []

    for ldap_user in LDAPUser.objects.all():
        remaining_ldap_users[ldap_user.dn] = True

    for p4_user in P4User.objects.all():
        remaining_p4_users[p4_user.user] = True

    for ldap_user_dn in remaining_ldap_users:
        ldap_user = LDAPUser.objects.get(dn=ldap_user_dn)

        try:
            p4_user=P4User.objects.get(user=ldap_user.uid)
            meta_users.append((ldap_user, p4_user))
            del remaining_p4_users[p4_user.user]
            del remaining_ldap_users[ldap_user.dn]
        except:
            pass

    for ldap_user_dn in remaining_ldap_users:
        ldap_user = LDAPUser.objects.get(dn=ldap_user_dn)
        meta_users.append((ldap_user, None))

    for p4_user_user in remaining_p4_users:
        p4_user=P4User.objects.get(user=p4_user_user)
        meta_users.append((None, p4_user))

    return meta_users

# Update the Meta user object set based on LDAP and P4 user object sets

def update_meta_users():

    new_meta_users = construct_meta_users_from_real_users()

    logger.info(str(len(new_meta_users)))

    def create(new_meta_users):
        for (ldap_user, p4_user) in new_meta_users:

            try:
                MetaUser.objects.get(ldap_user=ldap_user, p4_user=p4_user)
            except:
                meta_user = MetaUser.objects.create(ldap_user=ldap_user, p4_user=p4_user)
                logger.info("Creating Django model for meta user " + str(meta_user))
                meta_user.save()

    create(new_meta_users)

    def remove(new_meta_users):

        users_to_keep = {}
        for (ldap_user, p4_user) in new_meta_users:
            users_to_keep[MetaUser.hash(ldap_user, p4_user)] = True

        for old_meta_user in MetaUser.objects.all():
                if not MetaUser.hash(old_meta_user.ldap_user, old_meta_user.p4_user) in users_to_keep:
                    logger.info("Removing Django model for meta user " + str(old_meta_user))
                    old_meta_user.delete()

    remove(new_meta_users)

def updatemeta():
#    clear_meta_users()

    update_meta_users()
