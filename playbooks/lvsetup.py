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
                    help="disk type is required",
                    choices=["JBOD", "RAID6", "RAID10"], default='JBOD')

parser.add_argument("--pvlocation", '-p', default='/dev/vdb')
parser.add_argument("--lvname", '-l', default='lvol')
parser.add_argument("--vgname", '-n', default='volgroup')



class LogicalVolCreate(object):

    def __init__(self):
        pass

    def chunk_size(self, type, number_of_disks=None, size=None):
        if type == 'JBOD':
            ch_size= 256
            return ch_size
        elif type == 'RAID6':
            ch_size= (number_of_disks-2)*size
            return ch_size
        elif type=='RAID10':
            ch_size= (number_of_disks/2)*size
            return ch_size

        return ("Not valid")


def main():
    args = parser.parse_args()
    type = args.type
    if type == 'JBOD':
        chunk_size = LogicalVolCreate().chunk_size(type)
    else:
        number_of_disks = args.number_of_disks
        size = args.size
        chunk_size = LogicalVolCreate().chunk_size(type,
                     number_of_disks, size)

    vars = {
        "pvlocation": args.pvlocation,
        "lvname": args.lvname,
        "volgroup": args.vgname,
        "size": chunk_size
    }


    with open('./roles/lv/vars/main.yml', 'w+') as varfile:
        yaml.dump(vars, varfile, default_flow_style=False)

    os.system("ansible-playbook -i host.ini " + ' play.yml')


if __name__ == '__main__':
    main()
