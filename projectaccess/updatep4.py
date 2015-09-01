
from p4access import P4Connection
from models import P4User

import logging
logger = logging.getLogger(__name__)

def clear_p4_users():
    P4User.objects.all().delete()

def update_p4_users(new_p4_users):

    def create(new_p4_users):
        for new_p4_user in new_p4_users:
            user = new_p4_user['User']
            try:
                P4User.objects.get(user=user)
            except:
                logger.info("Creating Django model for P4 user " + user)
                p4_user = P4User.objects.create(user=user)
                p4_user.save()

    create(new_p4_users)

    def update(new_p4_users):
        for new_p4_user in new_p4_users:
            user = new_p4_user['User']
            try:
                old_p4_user = P4User.objects.get(user=user)

                if (old_p4_user.email != new_p4_user_details['Email'] \
                    or old_p4_user.full_name != new_p4_user_details['FullName']):

                    logger.info("Updating Django model for P4 user " + user)
                    old_p4_user.email = new_p4_user_details['Email']
                    old_p4_user.full_name = new_p4_user_details['FullName']
                    old_p4_user.save()
            except:
                pass

    update(new_p4_users)

    def remove(new_p4_users):
        users_to_keep = {}
        for new_p4_user in new_p4_users:
            users_to_keep[new_p4_user['User']] = True

        for old_p4_user in P4User.objects.all():
                if not old_p4_user.user in users_to_keep:
                    logger.info("Removing Django model for P4 user " + old_p4_user.user)
                    old_p4_user.delete()

    remove(new_p4_users)


def updatep4():
    clear_p4_users()

    with P4Connection('localhost', '1666', 'kalms') as p4:
        current_p4_users = p4.get_users()
    update_p4_users(current_p4_users)

def create_missing_p4_users():

    with P4Connection('localhost', '1666', 'kalms') as p4:

        from models import MetaUser
        for meta_user in MetaUser.objects.all():
            if meta_user.ldap_user:
                if not meta_user.p4_user:
                    setup_student_in_p4(p4, meta_user.ldap_user.uid, meta_user.ldap_user.mail, meta_user.ldap_user.cn)

def setup_student_in_p4(p4, login, email, fullname):

        p4.create_user(login, email, fullname)

        welcome_local_file = 'static/welcome.txt'
        welcome_depot_file = '//Users/%s/welcome.txt' % login
        p4.import_local_file(welcome_local_file, welcome_depot_file, 'Setting up things for %s' % login)

