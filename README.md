# Vanderbilt Scripts - Astro
Repository for storing scripts used by the Vanderbilt Astronomy Department.

**Author**: Victor Calderon ([victor.calderon@vanderbilt.edu](victor.calderon@vanderbilt.edu))

**Date**  : 2017-09-01

## Installing Environment
To use the scripts in this repository, you should have _Anaconda_ installed. This will simplify the process of installing all the dependencies.

### Installing
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

## Notes
To use the scripts in this repository, you __must__ save the following environment variables:

1. `AJC_Reminders`
  * `ajc_user`: Vanderbilt VUnet ID. This is used as the _user_ for sending email addresses.
  * `ajc_pswd`: Password for you vanderbilt email address.
2. `Astroweb_updates_xmlrpc`
  * `wp_username`: _Username_ for the Astro Wordpress page.
  * `wp_password`: _Password_ for the Astro Wordpress page.

Make sure to store this in your `~/.bashrc` or `~/.bash_profile` as __environment variables__ for the scripts to work.