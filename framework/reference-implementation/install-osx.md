---
layout: default
title: Installing SMART on OS X
---

This walks you through installing an *insecure SMART testing environment* on
Mac OS X. We will be installing everything needed for SMART into the directory
`/Library/SMART`, all the instructions assume that you are running a Terminal
open from this location. Of course you can use your own location, just remember
to return to your `SMART` directory. Tested on OS X Lion and Mountain Lion.


Install Homebrew
================

We use [Homebrew] as package manager to install most libraries. Since this
needs some extra command line tools to compile code, you first have to do
*one* of the following:

* Install [Xcode] from the App Store (it's free, if large), then open
  `Xcode > Preferences > Downloads > Components` and install the `Command Line
  Tools`

* Download only the [Command Line Tools][shell] (search for the correct version) from
  the Apple Developer Center (you will need a free developer account for this)


[Homebrew] is a superb replacement for the old managers Fink and MacPorts and
you will love it! Here's a one-line installer for it:

    $ /usr/bin/ruby -e "$(/usr/bin/curl -fsSL https://raw.github.com/mxcl/homebrew/master/Library/Contributions/install_homebrew.rb)"

If you had Homebrew installed before, make sure to update it:

    $ brew update

[Homebrew]: http://mxcl.github.com/homebrew/
[Xcode]: http://itunes.apple.com/ch/app/xcode/id497799835?l=en&mt=12
[shell]: https://developer.apple.com/downloads/index.action


Install Django and Python Tools
===============================

We have to use [Django 1.3][django] for now. You will see a lot of warnings from clang that you can safely ignore.

    $ sudo easy_install django==1.3.2
    $ sudo easy_install lxml, psycopg2
    $ sudo easy_install -U rdflib rdfextras jsonschema httplib2

At the time of this writing, this will install Django `1.3.2`, lxml `3.1.0`, psycopg `2.4.6`, rdflib `3.4.0`, rdfextras `0.4` and jsonschema `1.1`. Those versions all work well, if you are having trouble with newer versions you want to specify which version to install.

[django]: https://www.djangoproject.com/download/


PostgreSQL
==========

OS X 10.8 ships with PostgreSQL including a launchd-item, but I was out of luck finding its data directory. So we...

* Install postgres with homebrew (installs version 9.2.3):

        $ brew install postgresql
        $ initdb /usr/local/var/postgres -E utf8
        $ cp /usr/local/Cellar/postgresql/9.2.3/homebrew.mxcl.postgresql.plist \
          ~/Library/LaunchAgents/

* Launch Postgres

        $ launchctl load -w ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist

* Because of some socket issues we must symlink the socket from its default in `/tmp` to `/var/pgsql_socket`. Both are needed and I haven't been able to figure out why. First, create the directory and make it yours:

        $ sudo mkdir /var/pgsql_socket
        $ sudo chown `whoami`:admin /var/pgsql_socket/
        $ ln -s /tmp/.s.PGSQL.5432 /var/pgsql_socket/.s.PGSQL.5432

  > If you know how to circumvent this, let us know!

* Create a PostgreSQL user for your SMART service. We will be using *smart*,
  use your own password:
      
        $ createuser --superuser smart
        $ psql postgres
        $ postgres=# \password smart
        $ postgres=# \q

> **Caveat**: When using Postgres < 9.1 see the [instructions] on how to change
the Postgres config to use md5 passwords.

[postgres-mac]: http://www.postgresql.org/download/macosx/
[instructions]: https://github.com/chb/smart_server


Tomcat and openrdf-sesame
=========================

* Install Tomcat

        $ brew install tomcat

* Configure Tomcat: The environment variable *$CATALINA_HOME* needs to point
  to the tomcat base directory. So in your Bash `.profile` add:

        $ export CATALINA_HOME=/usr/local/Cellar/tomcat/7.0.32/libexec
  
  If brew didn't install version 7.0.32, change that number accordingly. If you don't use Bash adjust accordingly. Reload your profile file with:

        $ source ~/.profile

* Install openrdf-sesame

        $ curl -O http://freefr.dl.sourceforge.net/project/sesame/Sesame%202/2.7.2/openrdf-sesame-2.7.2-sdk.tar.gz
        $ tar -xzvf openrdf-sesame-2.7.2-sdk.tar.gz
        $ mkdir $CATALINA_HOME/.aduna
        $ mkdir $CATALINA_HOME/logs
        $ cp -r openrdf-sesame-2.7.2/war/* $CATALINA_HOME/webapps/
          
* Launch Tomcat and check its availability
  
        $ $CATALINA_HOME/bin/startup.sh
  
You should now be able to access `http://localhost:8080/openrdf-workbench/`

> OS X no longer ships with **Java** installed. Tomcat runs on Java, so if you haven't installed Java yet simply type `java` in the Terminal and the OS will prompt and install Java for you.


Automated SMART install
=======================

We're now ready to get the latest and greatest from SMART.

* Download the SMART manager
  
        $ curl -O https://raw.github.com/chb/smart_server/master/load_tools/smart_manager.py

* Run the manager. This will install the current `master` branch of all SMART
  repositories that we need. If you want the bleeding edge `dev` version, add a
  `-d` switch to the following command

        $ python smart_manager.py -a

This will fetch all needed repositories, run an installer that asks you for some configurations, generate patient sample data and in the end run the server.

## The reset script

If you didn't run the automated install, mostly because you had an old SMART version around already, you might want to use the script `smart_server/reset.sh` to recreate your Postgres databases.

> This drops the current database, so all data will be lost!


Running SMART
=============

If you've just run the automated install, you only need to start Tomcat via
`$CATALINA_HOME/bin/startup.sh`, in the future:

## To start SMART (and Tomcat):

    $ $CATALINA_HOME/bin/startup.sh
    $ python smart_manager.py -v -w

## To stop SMART (and Tomcat):

    $ python smart_manager.py -k
    $ $CATALINA_HOME/bin/shutdown.sh

Nobody is stopping you from putting these two commands in a start- and/or stop
script, of course. :)
