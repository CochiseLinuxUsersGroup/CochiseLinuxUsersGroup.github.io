# CochiseLinuxUsersGroup.github.io

> Site for the new Cochise Linux Users Group


```html
   _____         _   _            __    _ 
  |     |___ ___| |_|_|___ ___   |  |  |_|___ _ _ _ _ 
  |   --| . |  _|   | |_ -| -_|  |  |__| |   | | |_'_|
  |_____|___|___|_|_|_|___|___|  |_____|_|_|_|___|_,_|

        A place for Cochise County Arizona Linux Users
  
                /||\     Jake <hippyjake@gmail.com>
                ||||     Paul <paulbsocal@gmail.com>
                ||||     Rex <majb@azloco.com>
                |||| /|\
           /|\  |||| |||
           |||  |||| |||
           |||  |||| |||
           |||  |||| d||
           |||  |||||||/
           ||b._||||~~'
           \||||||||
            `~~~||||
                ||||
                ||||
~~~~~~~~~~~~~~~~||||~~~~~~~~~~~~~~
  \/..__..--  . |||| \/  .  ..
\/         \/ \/    \/
        .  \/              \/    .
. \/             .   \/     .
   __...--..__..__       .     \/
\/  .   .    \/     \/    __..--..
unknown
```
# CLUG in Jekyll

## Installation

Installing Jekyll is easy and straight-forward, but there are a few requirements you’ll need to make sure your system has before you start.

## Requirements
* Git
* Ruby (including development headers) Will be in your distribution Repo.
* RubyGems (The 'gem' command may or may not be included with your Ruby install, make sure)
* NodeJS, or another JavaScript runtime (for CoffeeScript support).

After ruby is installed, you will need to install Bundler. You can do this by running `gem install bundler`.

Run one line at a time
```bash
git clone https://github.com/CochiseLinuxUsersGroup/CochiseLinuxUsersGroup.github.io.git
cd CochiseLinuxUsersGroup.github.io
git checkout jekyll
export PATH=~/.gem/ruby/2.2.0/bin:$PATH
bundle install --path vendor/bundle
bundle exec jekyll serve
```
check https://github.com/guard/listen/wiki/Increasing-the-amount-of-inotify-watchers if you get an error.
You will now have a local installation of Jekyll and jekyll will be serving the site on your computer.

Have a look at the source and get hacking, making posts and pages in markdown. https://guides.github.com/features/mastering-markdown/
For more info on Jekyll go to http://jekyllrb.com