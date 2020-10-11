# There Is No WoeUSB

Well there _was_ one, but it is now moved to the new home <https://github.com/WoeUSB>.

## What happened

WoeUSB is moving to a new GitHub organization to fulfill new needs and expectations, refer [The future of WoeUSB · Issue #209 · slacka/WoeUSB](https://github.com/slacka/WoeUSB/issues/209) for more info.

* The self-sustaining `woeusb` program has been splitted from the current source to <https://github.com/WoeUSB/WoeUSB>, and the development will continue as usual.
* The current repository that comprises mostly the wxWidgets wrapper code for `woeusb`, is _forked_ to <https://github.com/WoeUSB/WoeUSB-frontend-wxgtk>, in its unmaintained form.
* @WaxyMocha implemented an independent, Python port of WoeUSB which is named WoeUSB-ng, and the project is located at <https://github.com/WoeUSB/WoeUSB-ng>.

## What should I do

### I'm a user of WoeUSB

Please refer to <https://github.com/WoeUSB/WoeUSB> for new software releases, the wxWidgets GUI is no longer well-maintained thus not recommended for usage.

### I've filed an unresolved issue to WoeUSB

Unfortunately due to technical difficulties we are unable to migrate old issues to the new project, please kindly file a new issue and link it to the old counterpart.

This is also a good time to ensure the issue is still reproducible/relavent.

### I've filed an unresolved pull request to WoeUSB

Please kindly file it again to the corresponding WoeUSB project, thank you!

### I'm a package maintainer of WoeUSB

* Please refer to the new GitHub projects for the source code and contacts.
* It is recommended to use `woeusb` as the package name of the `woeusb` Bash core utility, and a separate package of `woeusb-frontend-wxgtk` for the wxWidgets wrapper.  The `woeusb-frontend-wxgtk` package should not ship the `woeusb` program and relies on a dependency for the `woeusb` package.
* If you want to package the current source feel free to do so, after the descretion of the namespace conflict problem.

## Credits

We would like to thank @slacka and countless contributors for making the project alive, and thrive through these years.

The new title is inspired from [the There Is No Game : Wrong Dimension non-game](https://store.steampowered.com/app/1240210/There_Is_No_Game__Wrong_Dimension/)
