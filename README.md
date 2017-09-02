# Vanderbilt Scripts - Astro
Repository for storing scripts used by the Vanderbilt Astronomy Department.

**Author**: Victor Calderon ([victor.calderon@vanderbilt.edu](victor.calderon@vanderbilt.edu))

**Date**  : 2017-09-01

## Installing Environment
To use the scripts in this repository, you should have _Anaconda_ installed. This will simplify the process of installing all the dependencies.

For reference, see: [https://conda.io/docs/user-guide/tasks/manage-environments.html](https://conda.io/docs/user-guide/tasks/manage-environments.html)

1. Create the environment from the environment.yml file:

```
	conda env create -f environment.yml
```

2. Activate the new environment:

```
	source activate vandyscripts
```
3. Deactivate the new environment:

```
	source deactivate
```
4. To update the `environment.yml` file:
```
  conda env update -f environment.yml
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

### Regular Schedule
These scripts are meant to be run on a daily basis. You can do this by setting up a "crontab job". For further reference, see the "[Crontab - Quick Reference ](http://www.adminschoice.com/crontab-quick-reference)".

__Examples__:

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