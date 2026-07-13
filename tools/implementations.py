import subprocess

def list_running_containers():
    result = subprocess.run(
        ["/usr/bin/docker", "ps"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return f"Error: {result.stderr}"

    return result.stdout


def list_images():
    result = subprocess.run(
        ["/usr/bin/docker", "images"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return f"Error: {result.stderr}"

    return result.stdout


def container_logs(container):
    result = subprocess.run(
        ["/usr/bin/docker", "logs", container],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return f"Error: {result.stderr}"

    return result.stdout

def stop_container(container):
    result = subprocess.run(
        ["/usr/bin/docker", "stop", container],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return f"Error: {result.stderr}"

    return result.stdout

def  remove_container(container):
    result = subprocess.run(
        ["/usr/bin/docker", "rm", container],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return f"Error: {result.stderr}"

    return result.stdout


def list_all_containers():
    result = subprocess.run(
        ["/usr/bin/docker", "ps", "-a"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return f"Error: {result.stderr}"

    return result.stdout