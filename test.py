
# import getpass
# import os
# import subprocess

# print("User:", getpass.getuser())
# print("UID:", os.getuid())

# result = subprocess.run(
#     ["docker", "ps"],
#     capture_output=True,
#     text=True
# )

# print("Return code:", result.returncode)
# print("STDOUT:", result.stdout)
# print("STDERR:", result.stderr)

# from tools import list_running_containers

# containers = list_running_containers()

# print(containers)

import subprocess
import shutil
import os

def list_running_containers():
    print("Python executable:", shutil.which("python"))
    print("Docker executable:", shutil.which("docker"))
    print("PATH:", os.environ.get("PATH"))

    result = subprocess.run(
        ["/usr/bin/docker", "ps"],
        capture_output=True,
        text=True
    )

    print("Return code:", result.returncode)
    print("STDERR:", result.stderr)

    if result.returncode != 0:
        return f"Error: {result.stderr}"

    return result.stdout

print(list_running_containers())