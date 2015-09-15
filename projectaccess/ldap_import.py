
from django.db import transaction

from django.conf import settings

from ldapaccess import retrieve_ldap_users
from models import LDAPUser, PAUser

import logging
logger = logging.getLogger(__name__)

@transaction.atomic
def clear_django_users():
    PAUser.objects.all().delete()

@transaction.atomic
def update_django_users(new_ldap_users):

    def create(new_ldap_users):
        for (new_ldap_user_dn, new_ldap_user_details) in new_ldap_users:
            ldap_user, created = LDAPUser.objects.get_or_create(dn=new_ldap_user_dn.decode('utf-8'))
            if created:
                logger.info("Creating Django model for LDAP user " + new_ldap_user_dn.decode('utf-8'))
                pa_user = PAUser.objects.create()
                ldap_user.pa_user = pa_user
                pa_user.save()
                ldap_user.save()

    create(new_ldap_users)

    def update(new_ldap_users):
        for (new_ldap_user_dn, new_ldap_user_details) in new_ldap_users:
            old_ldap_user = LDAPUser.objects.get(dn=new_ldap_user_dn.decode('utf-8'))
            old_pa_user = old_ldap_user.pa_user

            new_ldap_user_name = new_ldap_user_details[settings.IMPORT_LDAP_ATTRIBUTE_CONTAINING_LDAP_USER_NAME][0].decode('utf-8')
            new_p4_user_name = new_ldap_user_details[settings.IMPORT_LDAP_ATTRIBUTE_CONTAINING_PERFORCE_USER_NAME][0].decode('utf-8')
            new_display_name = new_ldap_user_details[settings.IMPORT_LDAP_ATTRIBUTE_CONTAINING_DISPLAY_NAME][0].decode('utf-8')

            if old_pa_user.name != new_ldap_user_name:
                print 'Diff: %s %s' % (repr(old_pa_user.name), repr(new_ldap_user_name))
            if old_pa_user.p4_user_name != new_p4_user_name:
                print 'Diff: %s %s' % (repr(old_pa_user.p4_user_name), repr(new_p4_user_name))
            if old_pa_user.display_name != new_display_name:
                print 'Diff: %s %s' % (repr(old_pa_user.display_name), repr(new_display_name))

            if (old_pa_user.name != new_ldap_user_name
                or old_pa_user.p4_user_name != new_p4_user_name
                or old_pa_user.display_name != new_display_name):

                logger.info("Updating Django model for LDAP user " + new_ldap_user_dn.decode('utf-8'))
                old_pa_user.name = new_ldap_user_name
                old_pa_user.p4_user_name = new_p4_user_name
                old_pa_user.display_name = new_display_name
                old_pa_user.save()

    update(new_ldap_users)

    def remove(new_ldap_users):
        dns_to_keep = {}
        for (new_ldap_user_dn, new_ldap_user_details) in new_ldap_users:
            dns_to_keep[new_ldap_user_dn.decode('utf-8')] = True

        for old_ldap_user in LDAPUser.objects.all():
                if not old_ldap_user.dn in dns_to_keep:
                    logger.info("Removing Django model for LDAP user " + old_ldap_user.dn)
                    old_ldap_user.pa_user.delete()
                    old_ldap_user.delete()

    remove(new_ldap_users)


def import_ldap_users_to_django():
#    clear_django_users()

    current_ldap_users = retrieve_ldap_users()
    update_django_users(current_ldap_users)
