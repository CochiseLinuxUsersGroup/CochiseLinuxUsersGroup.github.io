#!/bin/bash

export PATH=~/.gem/ruby/2.2.0/bin:$PATH
echo 'exporting path...'
gem install bundler
bundle install --path vendor/bundle
bundle exec jekyll serve
