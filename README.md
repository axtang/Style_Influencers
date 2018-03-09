# Styles-Influencers

This is a project for Udacity's Full Stack Web Developer Nanodegree. 

In this application, users are presented with two lists, one of styles and the other of influencers.

Prior to log in, users can only view the styels or influencers.

Once users log into the application, they can create their own type of styles or influencers under the respective
list. Logged-in Users can also edit or delete these styles or influencers, but the range of actions are only limited to the registered owners 
of these creations.

"Styles Influencers" is a RESTful web application written in Python 3.0, HTML5, and CSS3 and Javascript. It is built on a web-app framework called Flask and utilizes Google OAuth2.0 to authenticate and authorize users. A PostgreSQL database is created to provide contents for this application.

## Prerequisities/ Preparations to set up this application

1. [Download and install the VirtualBox package](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
2. [Download and install Vagrant](https://www.vagrantup.com/downloads.html)
3. [Python 3.0](https://www.python.org/download/releases/3.0/ )
4. [Download or clone the virtual machine from Udacity's GitHub account into your Vagrant directory](https://github.com/udacity/fullstack-nanodegree-vm)
5. Note that there is no need to download and install SQLALchemy to setup the database in this project, because SQLAlchemy is already installed in the virtual machine.
6. On the command line, `cd` to the Vagrant directory and run `vagrant up` to set up the virtual machine.
7. Then, run `vagrant ssh` to log into the virtual machine.
8. Then, `cd /vagrant` to the vagrant file, which is shared by your local and host machines.
9. To run the application, run `python3 views.py` on the command line. Note that this is run on Python 3.0, so check the version of Python in your computer.
10. To access the application, go to `http://localhost`.
