

from P4 import P4,P4Exception    # Import the module
p4 = P4()                        # Create the P4 instance
p4.host = "localhost"
p4.port = "1666"
p4.user = "kalms"

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

def p4_get_users():
	with p4_connection() as p4:
		users = p4.run("users")
	return users

def p4_get_groups():
	with p4_connection() as p4:
		groups = p4.run("groups")
	return groups

	
	
try:                             # Catch exceptions with try/except

  print "Users: " + str(p4_get_users())
  print "Groups: "  + str(p4_get_groups())

  p4.connect()                   # Connect to the Perforce server
  info = p4.run( "info" )        # Run "p4 info" (returns a dict)

 
  for key in info[0]:            # and display all key-value pairs
    print key, "=", info[0][key]
  p4.run( "edit", "file.txt" )   # Run "p4 edit file.txt"
  p4.disconnect()                # Disconnect from the server
except P4Exception:
  for e in p4.errors:            # Display errors
      print e