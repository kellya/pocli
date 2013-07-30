pocli
=====

A generic command line interface for PushOver.net.  This should fully support
all the options that pushover.net api allows, and I will try to keep it
updated should the API change.

Requirements
============

You need to have
  * An existing account w/ pushover.net
  * An Application on pushover.net created
  * Python (Tested with v2.7 as packaged with Fedora)

Running
=======

After you have met the requirements, edit the config file and add your specific
data, then you just need to run *pocli.py -f config --message*.  Additinally, 
you may run *pocli.py --help* to see the list of options available.

Warnings
========

This is the first time I have tried to write a python app.  I am doing this
mostly to learn Python.  As such, I am trying to do things correctly, but may
not always do it in the best pyton way, so if you want to modify the code the
way I have done something might be aggravating.  Sorry, I'm learning :)

Contact
=======
If you find any problems, want to contribute code, whatever:  Please channel 
all communications through github (https://github.com/kellya/pocli)

License
=======
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
