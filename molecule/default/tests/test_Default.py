import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

@pytest.mark.parametrize('pkg', [
    'python3'
])
def test_pkg(host, pkg):
    package = host.package(pkg)

    assert package.is_installed


# Check port traffic on ssh port
@pytest.mark.parametrize('rule', [
    '-A ufw-user-input -p tcp -m tcp --dport 22 -j ACCEPT'
])
def test_ufw_rules(host, rule):
    cmd = host.run('iptables -t filter -S')
    assert rule in cmd.stdout


# Somes examples with ansible_vars

@pytest.fixture
def get_ansiblevars(host):
    defaults_files = "file=../../defaults/main.yml name=role_defaults"
    vars_files = "file=../../vars/main.yml name=role_vars"

    ansible_vars = host.ansible(
        "include_vars",
        defaults_files)["ansible_facts"]["role_defaults"]

    ansible_vars.update(host.ansible(
        "include_vars",
        vars_files)["ansible_facts"]["role_vars"])
    print(ansible_vars)
    return ansible_vars

# Verify if user terraform exist
def test_passwd_file(host,get_ansiblevars):
    passwd = host.file("/etc/passwd")
    assert passwd.contains(get_ansiblevars['myvarname_user'])

# Verify if group terraform exist
def test_group_file(host,get_ansiblevars):
    group = host.file("/etc/group")
    assert group.contains(get_ansiblevars['myvarname_user'])

# Verify if terraform_dir exist
def test_terraform_dir_path(host, get_ansiblevars):
    dir_path = get_ansiblevars['mypath_dir']
    config = host.file(dir_path)
    assert config.exists
    assert config.user == get_ansiblevars['myvarname_user']
    assert config.group == get_ansiblevars['myvarname_user']