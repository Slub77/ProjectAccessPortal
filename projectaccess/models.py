from django.db import models

# Create your models here.

# Example of an LDAP user entry (this has been extracted from an example .ldif file)
#
## rdaugherty, People, example.com
# dn: uid=rdaugherty,ou=People,dc=example,dc=com
# objectClass: person
# objectClass: inetOrgPerson
# objectClass: organizationalPerson
# objectClass: posixAccount
# objectClass: top
# uid: rdaugherty
# userPassword:: YXBwbGVz
# facsimileTelephoneNumber: +1 408 555 1992
# givenName: Robert
# cn: Robert Daugherty
# telephoneNumber: +1 408 555 1296
# sn: Daugherty
# roomNumber: 0194
# homeDirectory: /home/rdaugherty
# mail: rdaugherty@example.com
# l: Sunnyvale
# ou: Human Resources
# ou: People
# uidNumber: 1014
# gidNumber: 1000

class LDAPUser(models.Model):
	dn = models.CharField("Distinguished Name", max_length=1024)	# dn: uid=rdaugherty,ou=People,dc=example,dc=com
	uid = models.CharField("User ID", max_length=256)		# uid: rdaugherty
	cn = models.CharField("Canonical Name", max_length=1024)	# cn: Robert Daugherty
	mail = models.CharField("E-Mail", max_length=1024)		# mail: rdaugherty@example.com


# Example of a P4 user specification
#
# User: rdaugherty
#
# Email: rdaugherty@example.com
#
# FullName: Robeert Daugherty


class P4User(models.Model):
	user = models.CharField("User", max_length=1024)			# example: rdaugherty
	email = models.CharField("E-Mail", max_length=1024)			# example: rdaugherty@example.com
	full_name = models.CharField("Full Name", max_length=1024)	# example: Robert Daugherty


class MetaUser(models.Model):
	ldap_user = models.OneToOneField(LDAPUser, null=True)
	p4_user = models.OneToOneField(P4User, null=True)

	@staticmethod
	def hash(ldap_user, p4_user):
		if ldap_user:
			ldap_user_dn = ldap_user.dn
		else:
			ldap_user_dn = "None"

		if p4_user:
			p4_user_user = p4_user.user
		else:
			p4_user_user = "None"

		return "(%s, %s)" % (ldap_user_dn, p4_user_user)

	def __str__(self):
		return MetaUser.hash(self.ldap_user, self.p4_user)
