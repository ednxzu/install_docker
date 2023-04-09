"""Role testing files using testinfra."""


def test_hosts_file(host):
    """Validate /etc/hosts file."""
    etc_hosts = host.file("/etc/hosts")
    assert etc_hosts.exists
    assert etc_hosts.user == "root"
    assert etc_hosts.group == "root"

def test_docker_service(host):
    """Validate docker service."""
    docker_service = host.service("docker.service")
    assert docker_service.is_enabled
    assert docker_service.is_running
    assert docker_service.systemd_properties["Restart"] == "always"
    assert docker_service.systemd_properties["FragmentPath"] == "/lib/systemd/system/docker.service"

def test_docker_daemon(host):
    """Validate /etc/docker/daemon.json file."""
    docker_daemon_file = host.file("/etc/docker/daemon.json")
    assert docker_daemon_file.exists
    assert docker_daemon_file.user == "root"
    assert docker_daemon_file.group =="root"
    assert docker_daemon_file.mode == 0o644
    assert docker_daemon_file.contains("{}")

def test_docker_interaction(host):
    """Validate interaction with docker."""
    docker_ps = host.check_output("docker ps")
    assert docker_ps == "CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES"

def test_docker_compose(host):
    """Validate docker-compose installation"""
    docker_compose_bin = host.file("/usr/local/bin/docker-compose")
    docker_compose_version = host.check_output("docker-compose --version")
    assert docker_compose_bin.exists
    assert docker_compose_bin.user == "root"
    assert docker_compose_bin.group == "root"
    assert docker_compose_bin.mode == 0o755
    assert docker_compose_version == "Docker Compose version "+ r'^v\d+\.\d+\.\d+$'