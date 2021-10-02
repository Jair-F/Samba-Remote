from ast import ExtSlice
import pwd
import subprocess
import sys
import grp
import os


def run_subprocess(command:str, input_pipe_str:str="") -> subprocess.CompletedProcess:
	return subprocess.run([command], input=input_pipe_str.encode("utf-8"), capture_output=True)

def change_samba_password(username:str, old_password:str, new_password) -> str:
	"""
		Return the error Output(stderr) of the Command
	"""
	command = f"smbpasswd -s {username}"	# the command we would run in the console/terminal
	input_pipe_str = f"{old_password}\n{new_password}\n{new_password}\n"	# the input we would type in after we started the command(at the input("") methods)
	process = run_subprocess(command, input_pipe_str)
	return process.stderr

def delete_user(username:str):
	pass

def add_user(username:str, password:str, user_type:str, able_to_login:bool = False):
	pass

def shutdown_system():
	"""
		Shutdown the whole machine/System/PC
	"""
	run_subprocess("shutdown -P 0")

def reboot_system():
	"""
		Reboot the whole machine/System/PC
	"""
	run_subprocess("shutdown -r 0")







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


def get_users_in_group(group_name: str) -> tuple:
	"""
		Returns a tuple with the names of the users, which are part of the given group
	"""
	return tuple(grp.getgrnam(group_name).gr_mem())





if __name__ == "__main__":
	host = input("Server-Hostname: ")
	username = input("Username: ")
	oldpassword = input("Old Password: ")
	newpassword = input("New Password: ")
	verify_password = input("New Password: ")

	if newpassword != verify_password:	# Verify that the password is spelled correct
		print("New Passwords dont match!!", file=sys.stderr)
		exit(-1)

	process=subprocess.run(args=["smbpasswd", "-s", "-r", host, "-U", username], input=f"{oldpassword}\n{newpassword}\n{newpassword}\n".encode("utf-8"), capture_output=True)
	try:
		process.check_returncode()	# check if the process returned an ok(returncode 0)
	except subprocess.TimeoutExpired as exception:
		pass
	except subprocess.CalledProcessError as exception:
		pass
	except ...:
		print("An unknown error occurred", file=sys.stderr)
	
	print(process.args)
	print("stdout:")
	print(process.stdout.decode("utf-8"))
	print("stderr:")
	print(process.stderr.decode("utf-8"))
	print("returncode:")
	print(process.returncode)