import os
import sys
import shutil
from git import Repo


def incrementVersion(version):
	res = version.split("-")
	if len(res) == 1:
		res = res[0].split(".")
		for i in range(len(res) - 1, -1, -1):
			try:
				_ind = int(res[i])
				res[i] = str(_ind + 1)
				break
			except:
				pass

		return ".".join(res)
	else:
		for i in range(len(res) - 1, -1, -1):
			_out = incrementVersion(res[i])
			if _out:
				res[i] = _out
				break
		return "-".join(res)
	return None


if __name__=="__main__":
	if len(sys.argv)>2:
		version_filename = os.path.join(sys.argv[2],"version.py")
	else:
		version_filename = "version.py"

	if sys.argv[1]=="precommit":
		try:
			_code_file = open(version_filename, "r")
			_code = _code_file.read()
			_code_file.close()
			_locs = {}
			exec(_code, {}, _locs)
		except:
			pass

		version = _locs.get("version","0.0.0")

		# get current branch
		branch = Repo("./").active_branch.name
		version = incrementVersion(version)

		_code_file = open(version_filename, "w")
		_code = "branch = \"%s\"\nversion = \"%s\"\n" % (branch, version)
		_code_file.write(_code)
		_code_file.close()

		# add changed version file
		Repo("./").git.add(version_filename)

	elif sys.argv[1]=="postcommit":

		# add tag
		try:
			_code_file = open(version_filename, "r")
			_code = _code_file.read()
			_code_file.close()
			exec (_code, globals(), locals())
		except:
			pass

		Repo("./").git.tag("%s_%s"%(branch,version))

	elif sys.argv[1]=="init":
		_dirname = os.path.dirname(__file__)
		if len(sys.argv)>2:
			_version_root = sys.argv[2]
		else:
			_version_root = "./"

		_pre_commit_fn = os.path.join(".git","hooks","pre-commit")
		_post_commit_fn = os.path.join(".git","hooks","post-commit")
		shutil.copy(os.path.join(_dirname,"pre-commit"),_pre_commit_fn)
		shutil.copy(os.path.join(_dirname,"post-commit"),_post_commit_fn)

		with open(_pre_commit_fn,"a") as _file:
			_file.write(" %s"%_version_root)

		with open(_post_commit_fn, "a") as _file:
			_file.write(" %s"%_version_root)

