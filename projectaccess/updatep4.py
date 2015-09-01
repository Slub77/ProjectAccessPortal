
from p4access import p4_get_users
from models import P4User

def clear_p4_users():
    P4User.objects.all().delete()

def update_p4_users(new_p4_users):

    def create(new_p4_users):
        for new_p4_user in new_p4_users:
            user = new_p4_user['User']
            try:
                P4User.objects.get(user=user)
            except:
                print "Creating P4 user " + user
                p4_user = P4User.objects.create(user=user)
                p4_user.save()

    create(new_p4_users)

    def update(new_p4_users):
        for new_p4_user in new_p4_users:
            user = new_p4_user['User']
            try:
                old_p4_user = P4User.objects.get(user=user)
                print "Updating P4 user " + user
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
                    print "Removing P4 user " + old_p4_user.user
                    old_p4_user.delete()

    remove(new_p4_users)


def updatep4():
#    clear_p4_users()

    current_p4_users = p4_get_users()
    update_p4_users(current_p4_users)