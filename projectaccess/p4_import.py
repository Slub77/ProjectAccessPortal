
from P4Connection import P4Connection
from models import PAUser

import logging
logger = logging.getLogger(__name__)

def clear_django_users():
    PAUser.objects.all().delete()

def update_django_users(new_p4_users):

    def create(new_p4_users):
        for new_p4_user in new_p4_users:
            user = new_p4_user['User']
            try:
                PAUser.objects.get(name=user)
            except:
                logger.info("Creating Django model for P4 user " + user)
                pa_user = PAUser.objects.create(name=user)
                pa_user.save()

    create(new_p4_users)

    def update(new_p4_users):
        for new_p4_user in new_p4_users:
            user = new_p4_user['User']
            try:
                old_pa_user = PAUser.objects.get(name=user)

                if (old_pa_user.email != new_p4_user['Email'] \
                    or old_pa_user.full_name != new_p4_user['FullName']):

                    logger.info("Updating Django model for P4 user " + user)
                    old_pa_user.email = new_p4_user['Email']
                    old_pa_user.full_name = new_p4_user['FullName']
                    old_pa_user.save()
            except:
                pass

    update(new_p4_users)

    def remove(new_p4_users):
        users_to_keep = {}
        for new_p4_user in new_p4_users:
            users_to_keep[new_p4_user['User']] = True

        for old_pa_user in PAUser.objects.all():
                if not old_pa_user.name in users_to_keep:
                    logger.info("Removing Django model for P4 user " + old_pa_user.name)
                    old_pa_user.delete()

    remove(new_p4_users)

def import_p4_to_django():
#    clear_django_users()

    with P4Connection('localhost', '1666', 'kalms') as p4:
        current_p4_users = p4.get_users()

    update_django_users(current_p4_users)
