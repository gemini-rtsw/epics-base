Gemini EPICS-BASE
=================

`epics-base` vendor project is cloned during built. The ref to be switched to is 
specified in the specfile as `vendor_ref`. It can be a git commit hash or git tag.

Edit `configure/CONFIG_SITE.local` for site-specific (testing) modifications.

Execute the command `./epics-base-setup.sh` to apply patches provided with this repository
and to compile to the location specified in the `configure/CONFIG_SITE.local` file for the 
RTEMS version specified there.

