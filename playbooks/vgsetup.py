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
parser.add_argument("--extentsize", '-s')
parser.add_argument("--vgname", '-n')



class VolGroupCreate(object):

    def __init__(self):
        pass

    def physical_extent_size(self, type, number_of_disks=None, size=None):
        if type == 'JBOD':
            ext_size= 256
        elif type == 'RAID6':
            ext_size= (number_of_disks-2)* size
        elif type=='RAID10':
            ext_size= (number_of_disks/2)*size
        else:
            raise Exception("Invalid type")
        return ext_size


def main():
    args = parser.parse_args()
    type = args.type
    if type == 'JBOD':
        ext_size = VolGroupCreate().physical_extent_size(type)
        physical_extent_size = VolGroupCreate().physical_extent_size(type)
    else:
        number_of_disks = args.number_of_disks
        size = args.size
        physical_extent_size = VolGroupCreate().physical_extent_size(type, number_of_disks, size)


    pvlocation = args.pvlocation
    vars = {
        "pvlocation": args.pvlocation,
        "volgroup": args.vgname,
        "extent_size": physical_extent_size
    }

    import pdb; pdb.set_trace()


    with open('./roles/vg/vars/main.yml', 'w+') as varfile:
        yaml.dump(vars, varfile, default_flow_style=False)


    # os.system("ansible-playbook -i host.ini " + 'play.yml')

if __name__ == '__main__':
    main()
