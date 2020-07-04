# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys,  random
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

n_workers = 2
flavor = "ssc.medium" 
private_net = "SNIC 2020/20-13 Internal IPv4 Network"
floating_ip_pool_name = None
floating_ip = None
#Ubuntu 18.04 LTS (Bionic Beaver) - latest
image_name = "380b438b-f5d6-4afa-9d5f-a0ee972d60bc"

identifier = random.randint(1000,9999)

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_name=env['OS_USER_DOMAIN_NAME'],
                                #project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print ("user authorization completed.")

image = nova.glance.find_image(image_name)

flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")
cfg_file_path =  os.getcwd()+'/cloud-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata = open(cfg_file_path)
else:
    sys.exit("cloud-cfg.txt is not in current working directory")

secgroups = ['default','SSH']


print ("Creating {} instances...".format(n_workers))
instances = []
for i in range(n_workers):
    instance = nova.servers.create(name="dask_worker_"+str(identifier), image=image, flavor=flavor,userdata=userdata, nics=nics,security_groups=secgroups)
    instances.append(instance)

# incase you want to login to the production server 
#instance = nova.servers.create(name="prod_server_without_docker", image=image, flavor=flavor, key_name='access-key-name',userdata=userdata, nics=nics,security_groups=secgroups)

print ("waiting for 10 seconds.. ")
building = True
time.sleep(10)

while building:
    for i in instances:
        if i.status == 'BUILD':
            building = True
            break
        else:
            building = False
    if building:
        for i in instances:
            print ("Instance: "+i.name+" is in "+inst_status+" state...")
        time.sleep(5)
    
print ("All instances done")
