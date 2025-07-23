from typing import TypeAlias
__typ0 : TypeAlias = "str"
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
    ("Ronan", "Adrien"),
    # ("Thomas Herbelin", "Simon Le Bars"),
    # ("Samy Le Galloudec", "Marc Lamy"),
    # ("Maël Gaonach", "Antoine Omond"),
    # ("Robin Carrez", "Evrard-Nil Daillet"),
    # ("Paul Bavazzano", "Hoan My TRAN"),
    # ("Florian Le Menn", "" ),
    # ("Xavier Aleman", "Ismaïl El Khantache"),
    # ("Barthélémy Tek", ""),
    # ("Javed  Syed Khasim", "Emeric Chonigbaum"),
    # ("Lucas Pelec", ""),
    # ("Théo Coutant", ""),
    # ("Raphael Hascoet", ""),
    # ("", ""),
    # ("", "")
    # ("ronana",      "alebre"),
    # ("alacour",     "mnoritop"),
    # ("aqueiros",    "rlao"),
    # ("blemee",      "launea"),
    # ("bpeyresaube", "nguegan"),
    # ("cg",          "mmainchai"),
    # ("damarti",     "eguerin"),
    # ("jfreta",      "vjorda"),
    # ("kforest",     "maguyo"),
    # ("lparis",      "sedahmani"),
    # ("mmaheo",      "qeud"),
    # ("nfrayssinhe", "thlailler"),
    # ("rgrison",     "tandrieu"),
]


def __tmp0(h: Host) :
    'Returns the IP address of a Host `h`'
    try:
        return f'{socket.gethostbyname(h.address)}, {h.address}'
    except socket.gaierror:
        return h.address


def __tmp3(testing=True) -> Configuration:
    conf = {
        "reservation": "2021-03-05 07:00:01",
        "walltime": "11:59:58",
        "job_name": "lab-2021-imta-fise-login-os",
        "env_name": "ubuntu2004-x64-min",
        "project": "lab-2021-imta-fise-login-os",
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
                    "nodes": 13,
                    "primary_network": "net",
                    "secondary_networks": [ ],
                }
            ],
        }
    }

    if testing:
        del(conf["reservation"])
        conf["walltime"] = "07:00:00"
        conf["job_name"] = "test-lab-2021-imta-fise-login-os"
        conf["resources"]["machines"][0]["nodes"] = 1

    return Configuration.from_dictionnary(conf)


def provision(__tmp2: <FILL>):
    ensure_python3(roles=__tmp2)

    with play_on(roles=__tmp2, pattern_hosts="OpenStack") as p:
        # Install the bare necessities
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
def main(__tmp1):
    # Claim the resources
    infra = G5k(__tmp3(testing=__tmp1))
    roles, networks = infra.init(force_deploy=False)

    # Provision machines
    provision(roles)

    # Display subnet
    subnet = [n for n in networks
                if "neutron_external_interface" in n["roles"]]
    print(subnet)

    # Assign machines
    print("Lab machine assignations:")
    addrs = map(__tmp0, roles["OpenStack"])
    for (usr, addr) in zip_longest(TEAMS, addrs):
        print(f"- {addr} ({usr}): ")


if __name__ == "__main__":
    main()
