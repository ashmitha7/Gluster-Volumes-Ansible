# Creating Gluster volumes using ansible playbooks

To create physical volumes, volume group and logical volumes and mount them using ansible playbooks on remote hosts. And then creating Ansible roles and achieving the same results. 

Also, I have written a python file. 
The python file takes inputs from the user and returns the value of the variables to the yml files and then the yml files run to create PV,VG,LV and mount the volumes.

### pvcreate.yml 
playbook to create a physical volume.

### vgcreate.yml 
playbook to create volume group.

### lvcreate.yml 
playbook to create a logical volume. 

### mountt.yml   
playbook to create bricks and mount the volumes on the mount point.

### play.yml     
main playbook which has the roles. 
  
### varfile.yml  
playbook that initializes all the variables.

### host.ini     
Host file.
