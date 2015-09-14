
from django.core.management.base import NoArgsCommand

from ...ldap_import import import_ldap_users_to_django

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        import_ldap_users_to_django()
