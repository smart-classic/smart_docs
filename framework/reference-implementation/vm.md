---
layout: framework
title: SMART - Using the pre-built Virtual Machine
---


<div class='red_box'>
  <p>
    <b>Warning:</b> The SMART VM is <b>NOT</b> locked down for use on a
    public network (it was meant to be used within the confines of a local
    machine). If you decide to host the VM on the public network you will
    need to take a few additional precautions described below to secure the
    server. If you are only going to use the VM on your local machine then
    you can skip the next section</p>
</div>


## Securing the SMART VM for use on a public network

Basic steps:

  * Create an A-record entry in your name server pointing at the public IP
    address of the VM

  * Log in to the "smart" account on the machine and change the password
    to something else from the default: `passwd`

  * Apply the following Tomcat configuration changes to restric public access
    to port 8080:

      + in `/var/lib/tomcat7/conf/context.xml` add within the `<Context>` element:

        <Valve className="org.apache.catalina.valves.RemoteHostValve" allow="localhost"/>

      + and in `/var/lib/tomcat7/conf/server.xml` next to the other `<Connector>` elements:

        <Connector port="8080" protocol="HTTP/1.1" enableLookups="true">

  * Restart Tomcat: `sudo service tomcat7 restart`

  * Run the `./smart_manager.py -s` script to update the server settings
    (substitute "localhost" with the DNS of the machine that you want).

  * Take a look at the apache virtual servers' configurations in
    "/etc/apache2/sites-enabled" and change any occurence of "smart-vm"
    with your server's DNS.

  * Restart Apache: `sudo service apache2 restart`

  * Reset the SMART servers and reload the sample patients: `./smart_manager.py -rl`

  * If you need the SMART REST sample apps as well, then edit the manifest
    files in "/home/smart/manifests" and then run the "load_apps" script.

Beyond this, if you are planning on storing protected patient data on the
machine, you should:

   * change the default secrets on the SMART apps installed on the machine
(or remove them by resetting the sever)
   * disable the unsupervised account creation page (or password protect
it)
   * enforce SSL connections over HTTP in the Apache config

## Current SMART VM Builder

You can build the latest SMART VM (API version 0.6.2) using Vagrant. Follow the instructions on 
[https://github.com/smart-platforms/smart-vm](https://github.com/smart-platforms/smart-vm)
   
## Legacy Pre-built VM Downloads

The legacy SMART server deployments are packaged as generic Ubuntu Server 64-bit
virtual machines. The default username and password are "smart". After
logging in, follow the on-screen instructions to set up the smart-vm
host substitution on your local machine. You can then try out the SMART
reference server by pointing your browser at <http://smart-vm:7001>.

* [SMART VMWare Virtual Machine (API version 0.6.1)](http://media.smartplatforms.org/smart-vm/smart-vm-0.6.1.zip)
* [SMART VMWare Virtual Machine (API version 0.6)](http://media.smartplatforms.org/smart-vm/smart-vm-0.6.zip)
* [SMART VMWare Virtual Machine (API version 0.5.2)](http://media.smartplatforms.org/smart-vm/smart-vm-0.5.2.zip)
* [SMART VMWare Virtual Machine (API version 0.5.1)](http://media.smartplatforms.org/smart-vm/smart-vm-0.5.1.zip)
* [SMART VMWare Virtual Machine (API version 0.4)](http://media.smartplatforms.org/smart-vm/smart-vm-0.4.zip)
* [SMART VMWare Virtual Machine (API version 0.3)](http://media.smartplatforms.org/smart-vm/smart-vm-0.3.zip)
