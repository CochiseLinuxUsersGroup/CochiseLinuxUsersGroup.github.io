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
Read this if you want to make a page/post, fix/break something. If it works local it should work on GH Pages
## Installation

Installing Jekyll is easy and straight-forward, but there are a few requirements you’ll need to make sure your system has before you start.

### Requirements
* Git
* Ruby (including development headers) Will be in your distribution Repo.
* RubyGems (The 'gem' command may or may not be included with your Ruby install, make sure)
* NodeJS, or another JavaScript runtime (for CoffeeScript support).

After ruby is installed, you will need to install Bundler(See below). From [bundler.io][bundler]:
> Bundler provides a consistent environment for Ruby projects by tracking and installing the exact gems and versions that are needed. 

>Bundler is an exit from dependency hell, and ensures that the gems you need are present in development, staging, and production. Starting work on a project is as simple as bundle install.

## Run the Site Localy

Run one line at a time
```bash
git clone https://github.com/CochiseLinuxUsersGroup/CochiseLinuxUsersGroup.github.io.git
cd CochiseLinuxUsersGroup.github.io
git checkout jekyll
export PATH=~/.gem/ruby/2.2.0/bin:$PATH
gem install bundler
bundle install --path vendor/bundle
bundle exec jekyll serve
```

check https://github.com/guard/listen/wiki/Increasing-the-amount-of-inotify-watchers if you get an error.
You will now have a local installation of Jekyll and jekyll will be serving the site on your computer.

Have a look at the source and get hacking, making posts and pages in markdown. 

Learn about Markdown here:
[daringfireball.net/projects/markdown][Markdown]
and
[Github][Markdown-gh]

[For more info on Jekyll click here][jekyll]

***

[jekyll]: http://jekyllrb.com

[bundler]: http://bundler.io/

[inotify]: https://github.com/guard/listen/wiki/Increasing-the-amount-of-inotify-watchers "Increasing-the-amount-of-inotify-watchers"

[Markdown-gh]: https://guides.github.com/features/mastering-markdown/

[Markdown]: http://daringfireball.net/projects/markdown