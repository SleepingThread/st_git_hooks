import os


def getVersion(root="."):

	_version_filename = os.path.join(root,"version.py")

	try:
		_code_file = open(_version_filename, "r")
		_code = _code_file.read()
		_code_file.close()
		_locs = {}
		exec(_code, {}, _locs)
	except:
		pass

	version = _locs.get("version", None)
	branch = _locs.get("branch", None)

	return branch, version


def printVersion(root="./"):
	branch, version = getVersion(root)

	print("Branch: %s"%branch)
	print("Version: %s"%version)

	return