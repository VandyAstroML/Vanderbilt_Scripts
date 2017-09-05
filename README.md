# Vanderbilt Scripts - Astro
Repository for storing scripts used by the Vanderbilt Astronomy Department.

**Author**: Victor Calderon ([victor.calderon@vanderbilt.edu](victor.calderon@vanderbilt.edu))

**Date**  : 2017-09-01

## Installing Environment & Dependencies
To use the scripts in this repository, you should have _Anaconda_ installed. This will simplify the process of installing all the dependencies.

For reference, see: [https://conda.io/docs/user-guide/tasks/manage-environments.html](https://conda.io/docs/user-guide/tasks/manage-environments.html)

* Create the environment from the environment.yml file:

```
	make create_environment
```

* Activate the new environment:

```
	source activate vandyscripts
```
* Deactivate the new environment:

```
	source deactivate
```
* To update the `environment.yml` file (when the required packages have changed):

```
  make update_environment
```

## Notes
### Environment Variables
To use the scripts in this repository, you __must__ save the following environment variables:

1. `AJC_Reminders`
  * `ajc_user`: Vanderbilt VUnet ID. This is used as the _user_ for sending email addresses.
  * `ajc_pswd`: Password for you vanderbilt email address.
2. `Astroweb_updates_xmlrpc`
  * `wp_username`: _Username_ for the Astro Wordpress page.
  * `wp_password`: _Password_ for the Astro Wordpress page.

Make sure to store this in your `~/.bashrc` or `~/.bash_profile` as __environment variables__ for the scripts to work. If you don't know these passwords, contact the former person in charge of *AJC*.

### Makefile
The package counts with a _Makefile_ with useful functions. To see all the functions and their descriptions, type:

```
$: 	make show-help
	
	Available rules:
	
	clean               Delete all compiled Python files
	create_environment  Set up python interpreter environment
	crontab_clean       Cleans the Crontab
	crontab_create      Create crontab file to attach
	crontab_dir         Checks if CRONTAB folder exits
	crontab_file        Checks if CRONTAB file exists
	lint                Lint using flake8
	update_environment  Update python interpreter environment
```

### Regular Schedule
These scripts are meant to be run on a daily basis. You can do this by setting up a "crontab job". For further reference, see the "[Crontab - Quick Reference ](http://www.adminschoice.com/crontab-quick-reference)".

You can use the `make` functions to _create_ or _remove_ crontab jobs.

__Examples__:

* Using the Makefile functions
  * `make crontab_create`: Writes `crontab` commands to current `crontab` file to be run at 7am and 8am.
  * `make crontab_clean`: Cleans the `crontab` file and deletes the `crontab` tasks for the user.

1. `Astroweb_updates_xmlrpc.py`:
  * The code will run every day at 7am, and it will save the output to the file `updatelog2`.
```
	0 7 * * * python /path/to/Astroweb_updates_xmlrpc.py >> /path/to/updatelog2 2>&1
```
2. `AJC_Reminder`
  * The code will run twice daily, one at 8am and another one at 5pm. It calls the project environment `vandyscripts`, and runs the commands.

```
    0 8 * * * source activate vandyscripts; python /path/to/AJC_Reminders.py >> /path/to/ajc_log 2>&1; source deactivate;
    0 17 * * * source activate vandyscripts; python /path/to/AJC_Reminders.py >> /path/to/ajc_log 2>&1; source deactivate;
```