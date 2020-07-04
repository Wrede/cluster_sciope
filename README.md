# cluster_sciope

## TODO
Currently a random worker port is used. Need to add ports to security groups 


### Steps for the contextualization

0. Start a VM from the SSC dashboard and login to the client VM.

```console 
ssh -i PATH-TO-PRIVATE-KEY ubuntu@<CLIENT-VM-FLOATING-IP>
```
1. apt update and install all dependencies for sciope, including dask, tensorflow and keras

2. start dask scheduler with default port, e.g using a tmux session


3. Clone the git repository.

```console
git clone https://github.com/Wrede/cluster_sciope.git
```

4. Goto the `cluster_sciope/openstack/` directory. This is the code that we will use to contextualize our dask worker servers. The code is based on the following two files:

```console
- CloudInit configuration file  
  -- cloud-cfg.txt
- OpenStack python code
  -- start_workers.py
```
5. Change \<scheduler-ip\>:\<scheduler-port\> in cloud-cfg.txt. If one like to give a specific worker port use --worker-port \<port\>. n_workers = 2, change this to the amount of workers you want.


6. In order to run this code, you need to have OpenStack API environment running. 

_NOTE: Openstack APIs are only need to be installed on the client VM._ 

Follow the instructions available on the following links: 

- Goto https://docs.openstack.org/install-guide/environment-packages-ubuntu.html , http://docs.openstack.org/cli-reference/common/cli_install_openstack_command_line_clients.html and download the client tools and API for OpenStack.

- Download the Runtime Configuration (RC) file (version 3) from the SSC site (Top left frame, Project->API Access->Download OpenStack RC File).

- Set API access password. Goto https://cloud.snic.se/, Left frame, under _Services_ "Set your API password".  

- Confirm that your RC file have following enviroment variables:

```console
export OS_USER_DOMAIN_NAME="snic"
export OS_IDENTITY_API_VERSION="3"
export OS_PROJECT_DOMAIN_NAME="snic"
export OS_PROJECT_NAME="SNIC 2020/20-13"
```

- Set the environment variables by sourcing the RC-file:

```console 
source <project_name>_openrc.sh
```
_NOTE: You need to enter the API access passward._

- The successful execution of the following commands will confirm that you have the correct packages available on your VM:

```console
openstack server list
```

```console
openstack image list
```

- For the API communication, we need following extra packages (might not be necessary):

```console
apt install python3-openstackclient
apt install python3-novaclient
apt install python3-keystoneclient
```

------------------

NOTE: You need to setup \<YOUR-KEY\> in the start_workers.py script if you like to be able to log in to the workers.

4. Once you have setup the environment, run the following command. 

```console 
python3 start_workers.py
```

The command will start a new server and initiate the contextualization process of the workers. The progress can be seen on the cloud dashboard. Once the process finish start a jupyter notebook and start a dask Client() with the client's private IP and the scheduler port.

