import subprocess


def run_subprocess(args:tuple, input_pipe_str:str="", user:str=None) -> subprocess.CompletedProcess:
	return subprocess.run(args, input=input_pipe_str.encode("utf-8"), capture_output=True, user=user)

def change_samba_password(username:str, old_password:str, new_password):
	"""
		Return: returncode and the error Output(stderr) of the Command
	"""
	command = ("smbpasswd", "-s")	# the command we would run in the console/terminal(we start the command only with the privileges of the right user)
	input_pipe_str = f"{old_password}\n{new_password}\n{new_password}\n"	# the input we would type in after we started the command(at the input("") methods)
	process = run_subprocess(command, input_pipe_str, username)

	command_output = (process.stdout if process.stderr == None else process.stderr) # its in bytes
	command_output = str(command_output, "utf-8")
	return process.returncode, command_output	# if there is no error(stdout) return the stdout, otherwise the error-message

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

