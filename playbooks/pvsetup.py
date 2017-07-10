import os
import json
from ast import literal_eval
from tempfile import NamedTemporaryFile
import argparse

from ansible.playbook import Playbook
from ansible.module_utils.basic import *
import jinja2
import yaml


parser = argparse.ArgumentParser()
parser.add_argument("--type", '-t',
                    required=True,
                    help="disk type is required",
                    choices=["JBOD", "RAID6", "RAID10"])

parser.add_argument("--pvlocation", '-p')
parser.add_argument("--size", '-s')
parser.add_argument("--number_of_disks", '-n')



class PhysicalVolCreate(object):

    def __init__(self):
        pass

    def data_align(self, type, number_of_disks=None, size=None):
        if type == 'JBOD':
            dalign= 256
            return dalign
        elif type == 'RAID6':
            dalign= (number_of_disks-2)*size
            return dalign
        elif type=='RAID10':
            dalign= (number_of_disks/2)*size
            return dalign

        return ("Not valid")


def main():
    args = parser.parse_args()
    type = args.type
    if type == 'JBOD':
        data_align = PhysicalVolCreate().data_align(type)
    else:
        number_of_disks = args.number_of_disks
        size = args.size
        data_align = PhysicalVolCreate().data_align(type, number_of_disks, size)

    pvlocation = args.pvlocation

    vars = {
        "pvlocation": args.pvlocation,
        "dalign": data_align
    }


    with open('./roles/pv/vars/main.yml', 'w+') as varfile:
        yaml.dump(vars, varfile, default_flow_style=False)

    os.system("ansible-playbook -i host.ini " + ' playbooks/play.yml')

<<<<<<< HEAD:playbooks/pvsetup.py

=======
>>>>>>> 7b18b6150c07465e013534302e8ccef9a01c8914:pvsetup.py
if __name__ == '__main__':
    main()
