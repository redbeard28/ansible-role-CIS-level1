ANSIBLE-ROLE-CIS-LEVEL1
=======================

  WORK IN PROGRESS !!!

Ansible role CIS Hardening Level1


## Howto use this role?
This role need to be include in a playbook. 

Call this **Galaxy** role  like this:

````bash
ansible-galaxy install -r requirements.yml 
````

Inside requirements.yml
````yaml
# from GitHub, overriding the name and specifying a specific tag
- src: redbeard28.CIS-level1
````

More info => [Ansible Docs](https://docs.ansible.com/ansible-container/roles/access.html)

## Requirements

 * Ansible 2.9+


Role Variables
--------------

```yaml
---
my_prefered_repositories:
  - { name: "Main Updates {{ ansible_distribution_release | lower }}", definition: "deb http://deb.debian.org/debian/ {{ ansible_distribution_release | lower }}-updates main contrib non-free" }
  - { name: "SRC Main Updates {{ ansible_distribution_release | lower }}", definition: "deb-src http://deb.debian.org/debian/ {{ ansible_distribution_release | lower }}-updates main contrib non-free" }
  - { name: "Main for {{ ansible_distribution_release | lower }}", definition: "deb http://deb.debian.org/debian/ {{ ansible_distribution_release | lower }} main non-free contrib" }
  - { name: "SRC Main for {{ ansible_distribution_release | lower }}", definition: "deb-src http://deb.debian.org/debian/ {{ ansible_distribution_release | lower }} main non-free contrib" }

blacklist_fs:
  - { name: "cramfs", desactivated: "true" }
  - { name: "freevxfs", desactivated: "true" }
  - { name: "hfs", desactivated: "true" }
  - { name: "hfsplus", desactivated: "true" }
  - { name: "jffs2", desactivated: "true" }
  - { name: "udf", desactivated: "true" }

debian_cis_rules_1_1_1: false
debian_cis_rules_1_1_2: true

tmp_mount_file:
  RedHat: /usr/lib/systemd/system/tmp.mount
  Debian: /usr/share/systemd/tmp.mount
tmp_mount_options:
  RedHat: mode=1777,strictatime,noexec,nodev,nosuid
  Debian: mode=1777,strictatime,nodev,nosuid
```

Difficulties
------------

This role is difficult to test in docker image with molecule. I create a ssh_delegated scenario.



Molecule testing framework
--------------------------

This role is tested with the driver name delegated.

### Playbook converge
It use  ansible-role-CIS-level1/.vault file:
```bash
ansible_sudo_pass: "mysecrete_pass"
```

```yaml
---
- name: Converge
  hosts: all
  become: true
  gather_facts: true

  vars_files:
    - "{{ lookup('env', 'MOLECULE_PROJECT_DIRECTORY') }}/.vault"

  roles:
    - role: ansible-role-CIS-level1
```
### You have to create a file in
```bash
[ -d "~/.ssh/config.d" ] && touch ~/.ssh/config.d/delegated || mkdir -p ~/.ssh/config.d && touch ~/.ssh/config.d/delegated
```

### Inside ~/.ssh/config.d/delegated

```bash
ForwardAgent yes
# Yes, I know...
StrictHostKeyChecking no
# oO^^Oo
UserKnownHostsFile /dev/null

Host myserver.molecule
  Hostname XXX.XXX.XXX.XXX
  User myuser
  IdentityFile ~/.ssh/id_rsa
```

In molecule.yml, argument for ssh is "-F config"
```yaml
driver:
  name: delegated
  options:
    managed: False
    login_cmd_template: 'ssh {instance}'
    ansible_connection_options:
      ansible_connection: ssh
      ansible_ssh_common_args: '-F config'
```

Inside ansible-role-CIS-level1/molecule/ssh-delegated/config file is
```bash
Include config.d/*
```

You can use molecule to test this role.
```bash
image=debian tag="buster" molecule converge 
image=debian tag="buster" molecule verify 
```

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: all
      roles:
         - { role: redbeard28.CIS-level1, tags: mytags }
         
         
## Sources documentations

Stanford: ==>> [here](https://web.stanford.edu/~akkornel/CIS_debian8/CIS_Debian_Linux_8_Benchmark_v1.0.0.pdf)


Author Information
------------------

Jeremie CUADRADO[¹](mailto:info@redbeard-consulting.fr) from Redbeard-Consulting
