from typing import TypeAlias
__typ2 : TypeAlias = "Configuration"
__typ0 : TypeAlias = "Host"
__typ1 : TypeAlias = "str"
# $ pipenv run setup  [--test/--no-test]

import logging
import socket
import itertools

import click

from enoslib.types import Host, Roles
from enoslib.api import (play_on, ensure_python3)
from enoslib.infra.enos_g5k.provider import G5k
from enoslib.infra.enos_g5k.configuration import (Configuration)


logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)
TEAMS = [
    ("alebre", "mdelavergne"),
    ("antnguyen", "npierre"),
    ("bpaillette", "pbeslin"),
    ("fafilal", "sbenalaya"),
    ("jdumont", "smoro"),
    ("jklein", "xsong"),
    ("jkerleroderosbo", ""),
    ("mmoussaoui", ""),
]


def get_ip_addr(h: __typ0) :
    'Returns the IP address of a Host `h`'
    try:
        return f'{socket.gethostbyname(h.address)}, {h.address}'
    except socket.gaierror:
        return h.address


def __tmp3(testing=True) -> __typ2:
    conf = {
        "reservation": "2022-03-08 21:52:01",
        "walltime": "19:30:00",
        "job_name": "lab-2022-imta-fisea3-os",
        "env_name": "ubuntu2004-x64-min",
        "project": "lab-2022-imta-fisea3-os",
        "resources": {
            "networks": [
                {
                    "id": "net",
                    "type": "prod",
                    "roles": ["network_interface"],
                    "site": "rennes",
                },
                # Keep this for future work, for a deployment
                # based OpenStack.
                # {
                #     # Note: *NEVER* assigns this to a machine!
                #     "id": "net_ext",
                #     "type": "slash_22",
                #     "roles": ["neutron_external_interface"],
                #     "site": "rennes",
                # },
            ],
            "machines": [
                {
                    "roles": ["OpenStack"],
                    "cluster": "paravance",
                    "nodes": 8,
                    "primary_network": "net",
                    "secondary_networks": [ ],
                }
            ],
        }
    }

    if testing:
        del(conf["reservation"])
        conf["walltime"] = "08:30:00"
        conf["job_name"] = "lab-2021-imta-fila3-oss"
        conf["resources"]["machines"][0]["nodes"] = 1

    return __typ2.from_dictionnary(conf)


def provision(__tmp0: <FILL>):
    ensure_python3(roles=__tmp0)

    with play_on(roles=__tmp0, pattern_hosts="OpenStack") as p:
        # Install the bare necessities
        p.raw('apt update')
        p.apt(pkg=['bat', 'curl', 'htop', 'tcpdump', 'lynx', 'vim', 'kmod'],
              update_cache=True)
        # Workaround ripgrep error
        # https://bugs.launchpad.net/ubuntu/+source/rust-bat/+bug/1868517
        p.raw('apt download ripgrep')
        p.raw('dpkg --force-overwrite -i ripgrep*.deb')

        # IP Forwarding
        p.raw('sysctl -w net.ipv4.ip_forward=1')

        # Setup ssh for root w/ password
        p.raw('echo "root:lab-os" | chpasswd')
        p.blockinfile(path='/etc/ssh/sshd_config',
                      block='''
                      PasswordAuthentication yes
                      PermitRootLogin yes
                      ''')
        p.systemd(name='ssh', state='restarted')

        # Enhance default bash
        for l in ('. /etc/bash_completion',         # Offer bash completion
                  'export PATH=/snap/bin:${PATH}',  # Put /snap/bin in PATH
                  'alias cat="bat --style=plain"',    # Better cat
                  'alias fgrep="rg --fixed-strings"'  # Better fgrep
                  ) :
            p.lineinfile(path='/root/.bashrc', line=l)



# Main
@click.command()
@click.option('--test/--no-test', default=False)
def __tmp1(__tmp2):
    # Claim the resources
    infra = G5k(__tmp3(testing=__tmp2))
    roles, networks = infra.init(force_deploy=False)

    # Provision machines
    provision(roles)

    # Display subnet
    subnet = [n for n in networks
                if "neutron_external_interface" in n["roles"]]
    print(subnet)

    # Assign machines
    print("Lab machine assignations:")
    addrs = map(get_ip_addr, roles["OpenStack"])
    for (usr, addr) in itertools.zip_longest(TEAMS, addrs):
        print(f"- {addr} ({usr}): ")


if __name__ == "__main__":
    __tmp1()
