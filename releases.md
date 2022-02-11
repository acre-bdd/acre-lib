v0.2.7
=======
> 2021-02-08

-   support for project specific options extensions:

    Within a project, you can extend the list of supported
    settings by adding an 'option' file similar to the greenhouse
    option file in ~/.greenhouse/options. Any option listed
    there will be mapped to the docker container via a
    environment variable.
-   Fix `gh hooks check` syntax error on linux
-   Fix `gh hooks check` wrong check result

v0.2.6
=======
> 2021-12-01

-   gh log: don't abort started jobs.
-   gh log: allow filtering for priority with --priority

v0.2.5
=======
> 2021-11-18

-   gh feed: set default priority for user feeded jobs to 100
-   gh feed: support "-B ." for current branch of current directory
-   support: `gh node pause <nodename>`
-   support: `gh node resume <nodename>`
-   support: `gh node shutdown <nodename>`

v0.2.4
=======
> 2021-11-16

-   `gh node bash`: support passing further commands to bash.
-   `gh run`: fix 'RESOURCES' mapping target directory to /tmp/node/resources,
    which is default for decentralized nodes and local docker runs.
-   `gh feed`: support --plan=PAUSE, --plan=RESUME
-   use correct user name when feeding jobs

v0.2.3
=======
> 2021-11-04

-   fix `gh log` argument error.

v0.2.2
=======
> 2021-11-04

-   don't delete greenhouse image on 'gh update'.

v0.2.1
=======
> 2021-11-04

-   fix `gh log` error when calling `gh -v`

v0.2.0
=======
> 2021-11-03

-   `gh log`: command added.
    check `gh help log` for more details. 
  
v0.1.13
=======
> 2021-11-03

-   gh run: support RESOURCES options for mapping a resources directory to the docker container.
-   gh run: always use current working directory as PROJECT\_PATH
-   gh update: automatically remove and prune exising docker images after `gh update`

v0.1.12
=======
> 2021-09-29

- updated repository URLs for move to HQV-Gardena organisation.

v0.1.11
=======
> 2021-08-03

-   remove unused 'options' file
-   gh-feed: use $USER for feeding jobs
-   fix SGST-3343 'gh update stable' problem.

v0.1.10
=======
> 2021-04-28

-   fix local environment settings readout order.

v0.1.9
=======
> 2021-04-22

-   `gh node start` will automatically read `~/schedules/<nodename>`
-   fix local environment settings got overwritten by settings files.
-   SGST-3262 `gh node start` reads settings file from ~/schedules/<node>/settings.

v0.1.8
=======
> 2021-03-31

-   improved documentation.

v0.1.7
=======
> 2021-03-18

-   always load the testproject's 'etc/settings.DEFAULT' or 'etc/settings/DEFAULT'
-   fix bug in settings evaluation (prevented some settings file to load)
-   fix installer script: `gh upgrade invalidbranch` uninstalls gh

v0.1.6
=======
> 2021-03-17

-   Support of local test project
    -   +`gh node start --testproject ~/smartgarden` will map the local test project
        instead of using the default definition.
    -   --local will search for the testproject under ../testproject (instead of ../smartgarden)

v0.1.5
=======
> 2021-03-15

-   fix: use dynamic names for feeder nodes
-   update installer script, support BRANCHES:
        gh upgrade latest

v0.1.4
=======
> 2021-03-15

-   `gh feed`: support merges and plan.
-   support `gh upgrade [branch]`
-   `gh node start --portmap` will map the node ports to the local machine for VNC monitoring

v0.1.3
=======
> released @2021-03-11

-   improve `gh help node` and `gh help feed`
-   fix argument handling for `gh feed --direct`

v0.1.2
=======
> released @2021-03-10

-   support for `gh feed`
-   support for `gh node`

v0.1.1
=======
> released @2021-03-10

-   fixed USER\_ID handling for docker containers
-   basic support of decentralized testing, addig commands:
    -  `gh node` for starting/stopping greenhouse nodes
    -  WIP: `gh feed` for feeding greenhouse nodes with test jobs
-   fix `gh update` not recognizing new branches

v0.0.14
=======
> released @2021-02-13

-   support `etc/settings/<name>` setting files
-   forward exit code from docker run to caller
-   + option `--noportmap`
-   gh run: fixed option handling
-   automatically build depending docker containers
-   handle 'private' directory

v0.0.13
=======
> released @2021-02-09

-   SGST-2986 add command `gh tid` for creating random tid
-   SGST-2983 gh run: support `--keep`
-   SGST-2999 allow multiple `-s` arguments (`gh -s WEB -s DEVOPS`)

v0.0.12
=======
> released @2021-02-02

-   SGST-2973 support `DOCKEROPTS` option by greenhouse-cli, e.g.:

        DOCKEROPTS="-v /tmp/data:/home/tester/data" gh idock
-   alternatively, you can specify DOCKEROPTS in the greenhouse-cli settings file (`--settings`)
-   fix installer script for linux usage

v0.0.11
=======
> released @2021-01-09

-   fix: abort testrun when docker build fails (SGST-2892)

v0.0.10
=======
> released @2021-01-08

-   fix: codecheck did not return exit code properly
-   fix: codecheck failed when invoked from script
-   +`gh hooks [enable, disable, check]` command

v0.0.9
======
> released @2021-01-08

-   create junit-xml files on pytests
-   pass TRID to pytests
-   support `NO_IT` for docker run (`NO_IT=1 gh2 ...` will omit `-it` on docker  run)
-   support inline bash in settings file, e.g. `SIM_HOST=$(HOSTNAME)`
-   fix `--vpn` runs (missing docker vpn options)
-   fix resource mapping not working
-   fix `gh run <maketarget>` not working


v0.0.8
======
> released @2020-12-31

-   optimize argument handling
-   `run` is now default command, if ommitted
-   docker containers have the name of the reference system
-   docker container is terminated, when gh is teerminated (ctrl-c)
-   added `gh stop` for stopping running images. Check `gh help stop`

v0.0.7
======
> released @2020-12-09

-   fix runtimeerror on `--ssh` argument (also affects `gh mapssh`)

v0.0.6
======
> released @2020-12-09

-   use [pytest]{https://docs.pytest.org/en/latest/} for unit testing. ('gh help pytest')
-   `gh codecheck` does not occupy port 5901 (for screensharing).

v0.0.5
======
> @2020-12-06

-   add installer script. Check [REAMDE](README.md) for installation details.
-   add --vpn option for `gh ut` and `gh run`
-   +`gh upgrade` command

v0.0.4
======
> released @2020-12-06

-   ut: cd to `/tmp/ttt` before testurn.
-   Fix `ssh` mapping for `gh mapssh`.
-   +`gh ut` (unittest).
-   add documentation.
-   support `-S` and `--ssh` settings.
-   warn if no `TAG` was specified.
-   print error when no `profile` was specified. (mandatory).
-   release `greenhouse-cli` `v0.0.3`
-   fix `gh update`.

v0.0.3
======
> released @2020-12-04 

