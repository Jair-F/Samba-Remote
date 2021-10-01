import pwd

def get_linux_users_list(include_root: bool = False) -> tuple:
	"""
		Retruns a tuple of the real linux users of the type:struct_passwd on the system - the users of deamons not included
	"""
	users = pwd.getpwall()
	linux_users = list()
	for user in users:
		# Real users in linux(meaning no users for deamons) usually have a uid higher than 1000 and a real login shell
		if user.pw_uid >= 1000 and user.pw_shell != "/usr/bin/nologin" and user.pw_shell != "/bin/false":
			linux_users.append(user)
	
	if include_root == True:
		linux_users.append(pwd.getpwuid(0))	# root user has always uid=0

	return tuple(linux_users)