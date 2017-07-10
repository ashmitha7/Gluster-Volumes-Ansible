# Creating Gluster volumes using ansible playbooks

To create physical volumes, volume group and logical volumes and mount them using ansible playbooks on remote hosts. And then creating Ansible roles and achieving the same results. 

Also, I have written a python file. 
The python file takes input from the user and creates a new temporary playbook by filling out the variables inclosed in the Jinja expression and finally executes the playbooks to create a PV,VG,Lv and mount the volumes.

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

### pvsetup.py
The python file takes input from the user and creates a varfile in the var directory within the role directory and finally executes the playbook to create a PV.  

For example - 
        ``` python pvsetup.py -t JBOD -p /dev/vdb ```

where 

       -t is for the type of data disk 
       
       -p is for the location of the physical volume

### vgsetup.py
The python file takes input from the user and creates a varfile in the var directory within the role directory and finally executes the playbook to create a VG.

For example -
      ``` python vgsetup.py -t JBOD -s 1280K -n volgroup -p /dev/vdb ```
      
where 

      -t is for the type of data disk

      -s is for the physical extent size

      -n is for the name of volume group 

      -p is for the location of physical volume
         
 ### lvsetup.py
 The python file takes input from the user and creates a varfile in the var directory within the role directory and finally executes the playbook to create a LV.
 
 for example - 
      ``` python lvsetup.py -t JBOD -l lvname -n volgroup -p /dev/vdb ```
      
    where
    
          -t is for the type of data disk
          
          -l is for the logical volume name
          
          -n is for the name of volume group 
          
          -p is for the location of physical volume    
