from ansible.module_utils.basic import *
import json
from ast import literal_eval


class PvOps(object):

    def __init__(self, module):
        self.module = module
        self.action = self.validated_params('action')
        self.options = self.module.params['options'] 

    def validated_params(self, opt):
        value = self.module.params[opt]
        if value is None:
            msg = "Please provide %s option in the playbook!" % opt
            self.module.fail_json(rc=1, msg=msg)
        return value

    def run_command(self, op, options):
        cmd = self.module.get_bin_path(op, True)  + options
        return self.module.run_command(cmd)

    def get_output(self, rc, output, err):
        if not rc:
            self.module.exit_json(rc=rc, stdout=output, changed=1)
        else:
            self.module.fail_json(rc=rc, msg=err)

    def pv_presence_check(self, disk):
        rc, out, err = self.run_command('pvdisplay', ' ' + disk)
        ret = 0
        if self.action == 'create' and not rc:
            self.module.exit_json(rc=0, changed= 0, msg="%s Physical Volume Exists!" % disk)
        else:
            ret = 1
        return ret

    def pv_action(self):
        self.disks = self.validated_params('disks')
        if not self.disks:
            self.module.exit_json(msg="Nothing to do")
        return self.get_volume_command(self.disks)

    def get_volume_command(self, disk):
        op = 'pv' + self.action
        args = " %s %s" % (self.options, disk)
        return args



if __name__ == '__main__':
    module = AnsibleModule(
        argument_spec=dict(
            action=dict(choices="create", required=True),
            disks=dict(),
            options=dict(type='str'),
            size=dict(),
        ),
    )

    pvops = PvOps(module)
    cmd = pvops.pv_action()
    pvops.pv_presence_check(pvops.disks)
    rc, out, err = pvops.run_command('pv' + pvops.action, cmd)
pvops.get_output(rc, out, err)