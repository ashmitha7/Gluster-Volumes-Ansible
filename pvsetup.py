import os
import json
from ast import literal_eval
from tempfile import NamedTemporaryFile

from ansible.playbook import Playbook
from ansible.module_utils.basic import *
import jinja2

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
    type = raw_input("Enter the value of data alignment : ")
    if type == 'JBOD':
        data_align = PhysicalVolCreate().data_align(type)
    else:
        number_of_disks = input("Enter the number of disks :")
        size = raw_input("Enter the size : ")
        data_align = PhysicalVolCreate().data_align(type, number_of_disks, size)

    pvlocation = raw_input("Enter the physical volume location : ")

    playbook = open('pvcreate.yml','r+')
    playbook_template = jinja2.Template(playbook.read())

    rendered_template = playbook_template.render({
        'pvlocation': pvlocation,
        'dalign': data_align
})
    new_playbook =  open('./tmp.yml', 'w+')
    new_playbook.write(rendered_template)
    new_playbook.write('\n')
    new_playbook.close()

    os.system("ansible-playbook -i host.ini " + new_playbook.name)


    import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()
