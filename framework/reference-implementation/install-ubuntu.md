---
layout: default
title: Installing SMART on Ubuntu
---

# Repositories 

These instructions apply to each of three github repositories that you'll need
in order to run the SMART Reference EMR in your own environment:

* https://github.com/chb/smart_server.git
* https://github.com/chb/smart_ui_server.git
* https://github.com/chb/smart_sample_apps.git
* https://github.com/chb/smart_sample_patients.git


# System Setup

* Recent Linux installation (Kernel 2.6+).We recommend an up-to-date version of
  Ubuntu, and these instructions are written from that perspective.
* Note: These instructions have been updated for Ubuntu 12.04
* Note: We recommend you do this by sudo'ing from a non-root user. If you
  would like to do this as root make sure you create at least one non-root user
  with `useradd -m {USER}` otherwise the default locale will not be set. This
  issue is most common on a new OS build.

* Update the apt-get manifests:

        $ sudo apt-get update

* Python 2.7 with package `psycopg2`

        $ sudo apt-get install python-psycopg2 python-m2crypto \
            python-simplejson python-argparse python-setuptools python-pyparsing

        $ sudo easy_install -U "rdflib==3.2.3" "rdfextras==0.2" "jsonschema==0.7" httplib2

* Django 1.3+

        $ sudo apt-get install python-django

* PostgreSQL 8.3+

        $ sudo apt-get install postgresql

* git

        $ sudo apt-get install git


# Setup Database

* Create a PostgreSQL user for your SMART service, e.g. `smart` and
  setup a password. You'll have the easiest time if you name your
  database `smart` as well.

        $ sudo su - postgres
        $ pg_dropcluster --stop 9.1 main
        $ pg_createcluster --start -e UTF-8 9.1 main
        $ createuser --superuser smart
        $ psql
        $ postgres=# \password smart
        $ postgres=# \q
        $ exit

* There are two ways to authenticate to PostgreSQL: use your Unix credentials,
  or use a separate username and password. We strongly recommend the latter,
  and our instructions are tailored appropriately. If you know how to use
  PostgreSQL and want to use Unix-logins, go for it, just remember that when
  you use Apache, it will usually try to log in using its username, `www-data`.

* in `/etc/postgresql/9.1/main/pg_hba.conf`, find the line that reads:

        local     all     all        XXX

This should be the second uncommented line in your default config. Note XXX
in this line could be `ident`, `peer`, or another name. Change XXX to `md5`:

        local     all     all        md5

* You will need to restart PostgreSQL:

        $ sudo service postgresql restart


# Install `openrdf-sesame` (and Tomcat)

* get Tomcat and OpenRDF-Sesame:

        $ sudo apt-get install tomcat7
        $ wget http://downloads.sourceforge.net/project/sesame/Sesame%202/2.6.9/openrdf-sesame-2.6.9-sdk.tar.gz

* install OpenRDF Sesame as a Tomcat web application

        $ tar -xzvf openrdf-sesame-2.6.9-sdk.tar.gz
        $ sudo mkdir /usr/share/tomcat7/.aduna
        $ sudo chown tomcat7.tomcat7 /usr/share/tomcat7/.aduna/
        $ sudo cp -r openrdf-sesame-2.6.9/war/* /var/lib/tomcat7/webapps/

* restart Tomcat (optional since autoDeploy is typically enabled in Tomcat by default)
  
        $ sudo service tomcat7 restart

* check that Tomcat and OpenRDF Sesame are running by hitting
  <http://localhost:8080/openrdf-workbench/>. You should see the main OpenRDF
  status page.

The OpenRDF store doesn't support access control. You will probably want to
limit access to just `localhost`. To limit servlet access to `localhost`, make two
tomcat configuration changes:

* in `/var/lib/tomcat7/conf/context.xml` add within the `<Context>` element:

        <Valve className="org.apache.catalina.valves.RemoteHostValve" allow="localhost"/>

* and in `/var/lib/tomcat7/conf/server.xml` next to the other `<Connector>` elements:

        <Connector port="8080" protocol="HTTP/1.1" enableLookups="true">

You'll need to restart Tomcat again if you make these changes


# Automated approach: Download, Install, and Configure SMART Server Components

At this point you are ready to install the SMART server components. There are
two ways to do this. You can either use the easy install script (described here)
or skip this step and follow the manual setup steps. If you complete the
installation via the automated script, there are no further steps that you need
to do after running the script (your SMART server will be fully functional).

    $ wget https://raw.github.com/chb/smart_server/master/load_tools/smart_manager.py
    $ python smart_manager.py -a

(Note:  if you'd like to run the bleeding-edge SMART development branch, replace `master` with `dev` in the `wget`
command above and pass the `-d` flag to `smart_manager.py`.  If you're unsure, you probably want to stick with the
master branch!)

## Usage examples for smart_manager.py

Kill and restart the development servers

    $ python smart_manager.py -k -v -w

Reset the SMART server, regenerate sample data, and reload:

    $ python smart_manager.py -r -p -l

## Loading additional apps

    $ cd smart_server

    # file path can be a URL or local file; OAuth secret can be any string
    $ python manage.py load_app http://path/to/manifest.json smartapp-secret

# Manual steps: if you don't take the automated approach...

## 1. Download, Install, and Configure SMART Backend Server

* get the code

      $ git clone --recursive https://github.com/chb/smart_server.git

* copy `settings.py.default` to `settings.py` and update it:
  * set `APP_HOME` to the complete path to the location where you've
    installed `smart_server`, e.g. `/web/smart_server`
  * set `SITE_URL_PREFIX` to the URL where your server is running,
    including port number  e.g. `http://localhost:7000`
  * set `CHROME_CONSUMER` to `chrome`
  * set `CHROME_SECRET` to `chrome`
  * set `SMART_UI_SERVER_LOCATION` to the URL where your UI server will
    be running, including port number  e.g. `http://localhost:7001`
  * set PLUGIN_USE_PROXY to `False`
  * set `TRIPLESTORE['engine']` to `sesame`
  * set `TRIPLESTORE['record_endpoint']` to `http://localhost:8080/openrdf-sesame/repositories/record_rdf`
  * set `DATABASE_USER` to the username you chose, in this documentation
    `smart`, and set `DATABASE_PASSWORD` accordingly.

* copy `bootstrap_helpers/application_list.json.default` to
  `bootstrap_helpers/application_list.json` and customize it to include
  the apps that you want.

* copy `bootstrap_helpers/bootstrap_applications.py.default` to
  `bootstrap_helpers/bootstrap_applications.py` and customize it to include
  the service apps that you want.

* update the database and repository settings in `reset.sh` (if you
  changed the default DB and repository endpoints in `settings.py`)

* set things up (supplying the smart db password when prompted twice)

        $ ./reset.sh

  NOTE: On the first run of `reset.sh`, you will also see some 500s.
  Don't worry about them.  When the reset process completes, you should see:

        ...
        No fixtures found.

This is normal -- nothing has gone wrong.

IMPORTANT: if you've enabled apps that are part of the sample apps below, you
should *wait* to run `reset.sh` until you've got the sample apps server
running. The SMART Reference EMR attempts to download the apps' manifest files,
and if they're not available over HTTP, `reset.sh` won't complete successfully.
If you mistakenly run `reset.sh` before setting up the SMART Sample Apps, don't
worry, just set up the SMART Sample Apps server, and run `reset.sh` again.

## 2. Download, Install, and Configure SMART UI Server

* get the code

        $ git clone --recursive https://github.com/chb/smart_ui_server.git

* copy `settings.py.default` to `settings.py` and update:
	* set `APP_HOME` to the complete path to the location where
      you've installed `smart_ui_server`, e.g. `/web/smart_ui_server`
	* set `SMART_API_SERVER_BASE`, `CONSUMER_KEY`,
      `CONSUMER_SECRET` appropriately to match the SMART Server's
      location and chrome credentials. (Check your `bootstrap.py` within
      `smart_server` for those credentials. If you change them, you'll
      need to run `reset.sh` again on the SMART server. If you never
      changed `bootstrap.py`, then your `CONSUMER_KEY` and
      `CONSUMER_SECRET` are both `chrome`, and you don't need to
      change their value in the UI server default settings file.)
	* set `DATABASE_USER` to the username you chose, in this
      documentation `smart`, and set `DATABASE_PASSWORD`
      accordingly.

* set things up (supplying the smart db password when prompted twice)

        $ ./reset.sh


## 3. Download, Install, and Configure SMART Sample Apps

* get the source code

       $ git clone --recursive https://github.com/chb/smart_sample_apps.git

* copy `settings.py.default` to `settings.py` and update:
    * set `APP_HOME` to the complete path to the location where you've
      installed `smart_sample_apps`, e.g. `/web/smart_sample_apps`
    * set `SMART_APP_SERVER_BASE` to `http://localhost:8001`
    * set `SMART_API_SERVER_BASE` to point to the location of the SMART
      Server. If you are running the SMART server on `localhost:7000` as
      we suggest, there's no need to change anything.


## 4. Manual steps: Generate  and Load Sample Patient Records

* get the source code and generate sample data

        $ git clone --recursive https://github.com/chb/smart_sample_patients.git
        $ cd smart_sample_patients/bin
        $ python generate.py --write ../generated-data/

* Load into SMART EMR

        $ cd /path/to/smart_server
        $ PYTHONPATH=.:.. DJANGO_SETTINGS_MODULE=settings /usr/bin/python \
          load_tools/load_one_patient.py /path/to/smart_sample_patients/generated-data/*
 
 Expect this to take a few minutes.


## 5.Running the Development Servers

The Django development servers are easy to run at the prompt.

The backend server can run on localhost in the configuration given above:

    cd /path/to/smart_server/
    nohup python manage.py runconcurrentserver 7000 --noreload > log.txt 2>&1 &

The UI server, if you want it accessible from another machine, needs to specify
a hostname or IP address. If you want port 80, you need to be root of course.
The mask "0.0.0.0" will allow all incoming connections:

    cd /path/to/smart_ui_server/
    nohup python manage.py runconcurrentserver 0.0.0.0:7001 --noreload > log.txt 2>&1 &

And finally, the Sample Apps:


    cd /path/to/smart_sample_apps/
    nohup python manage.py runconcurrentserver 0.0.0.0:8001 --noreload > log.txt 2>&1 &

*Note*: In the above examples the console output is suppressed. If you are having
trouble with the server, you may want to redirect the output to the console or a
log file.

<h2>The SMART EMR is now at: http://localhost:7001/login</h2>
