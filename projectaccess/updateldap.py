
from ldapaccess import retrieve_ldap_users
from models import LDAPUser

import logging
logger = logging.getLogger(__name__)

def clear_django_users():
    LDAPUser.objects.all().delete()

def update_django_users(new_ldap_users):

    def create(new_ldap_users):
        for (new_ldap_user_dn, new_ldap_user_details) in new_ldap_users:
            try:
                LDAPUser.objects.get(dn=new_ldap_user_dn)
            except:
                logger.info("Creating Django model for LDAP user " + new_ldap_user_dn)
                ldap_user = LDAPUser.objects.create(dn=new_ldap_user_dn)
                ldap_user.save()

    create(new_ldap_users)

    def update(new_ldap_users):
        for (new_ldap_user_dn, new_ldap_user_details) in new_ldap_users:
            try:
                old_ldap_user = LDAPUser.objects.get(dn=new_ldap_user_dn)
                logger.info("Updating Django model for LDAP user " + new_ldap_user_dn)
                old_ldap_user.cn = new_ldap_user_details['cn']
                old_ldap_user.uid = new_ldap_user_details['uid']
                old_ldap_user.mail = new_ldap_user_details['mail']
                old_ldap_user.save()
            except:
                pass

    update(new_ldap_users)

    def remove(new_ldap_users):
        dns_to_keep = {}
        for (new_ldap_user_dn, new_ldap_user_details) in new_ldap_users:
            dns_to_keep[new_ldap_user_dn] = True

        for old_ldap_user in LDAPUser.objects.all():
                if not old_ldap_user.dn in dns_to_keep:
                    logger.info("Removing Django model for LDAP user " + old_ldap_user.dn)
                    old_ldap_user.delete()

    remove(new_ldap_users)


def updateldap():
#    clear_django_users()

    current_ldap_users = retrieve_ldap_users()
    update_django_users(current_ldap_users)