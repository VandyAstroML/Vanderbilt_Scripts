# Vanderbilt Scripts - Astro
Repository for storing scripts used by the Vanderbilt Astronomy Department.

**Author**: Victor Calderon ([victor.calderon@vanderbilt.edu](victor.calderon@vanderbilt.edu))

**Date**  : 2017-09-01

## Installing Environment & Dependencies
To use the scripts in this repository, you must have _Anaconda_ installed on the systems that will be running the scripts. This will simplify the process of installing all the dependencies.

For reference, see: [https://conda.io/docs/user-guide/tasks/manage-environments.html](https://conda.io/docs/user-guide/tasks/manage-environments.html)

The package counts with a __Makefile__ with useful functions. You must use this Makefile to ensure that you have all the necessary _dependencies_, as well as the correct _conda environment_. 

* Show all available functions in the _Makefile_

```
$: 	make show-help
	
	Available rules:
	
	clean               Delete all compiled Python files
	environment         Set up python interpreter environment
	lint                Lint using flake8
	remove_environment  Delete python interpreter environment
	update_environment  Update python interpreter environment
```

* __Create__ the environment from the `environment.yml` file:

```
	make environment
```

* __Activate__ the new environment __vandyscripts__.

```
	source activate vandyscripts
```

* To __update__ the `environment.yml` file (when the required packages have changed):

```
  make update_environment
```

* __Deactivate__ the new environment:

```
	source deactivate
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

Make sure to store these in your `~/.bashrc` or `~/.bash_profile` as __environment variables__ for the scripts to work. If you don't know these passwords, contact the former person in charge of *AJC*.

__Example of what to add to your `profile` (.bashrc or .bash_profile) file__:

```
### Vanderbilt Scripts
# AJC
ajc_user='VUnet ID'; export ajc_user
ajc_pswd='Password to your VUnet account'; export ajc_pswd

# Wordpress
wp_username='Username for AJC'; export wp_username
wp_password='Password for AJC'; export wp_password
```

__Note__: Replace the values for __ajc_user__, __ajc_pswd__, __wp_username__, and __wp_password__ with the _real_ values.

### Regular Schedule
These scripts are meant to be run on a daily basis. You can do this by setting up a "crontab job". For further reference, see the "[Crontab - Quick Reference ](http://www.adminschoice.com/crontab-quick-reference)".

The file `run_ajc_scripts.sh` has the necessary commands to run the scripts.
All you have to do is to add the following to your current _crontab_ file:

```
* 7 * * * /path/to/run_ajc_scripts.sh
```

This will run `run_ajc_scripts.sh` every day at 7am.

__Note__: Make sure you have had installed the `vandyscripts` conda environment by running `make environment` _before_ you run this bash script.

You can check this by typing:

```
$: 	conda env list

vandyscripts             /path/to/anaconda/envs/vandyscripts
root                  *  /path/to/anaconda/
```

#### Crontab file
If you don't have a _crontab_ file, you can add the command `* 7 * * * /path/to/run_ajc_scripts.sh` to the crontab file, after you have typed:

```
$: crontab -e
```

## Questions

If you have a questions or feedback, please open an _issue_ on Github.

Thanks!