#!/bin/bash


#colors
red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
reset=`tput sgr0`

echo "${yellow}Exporting path${reset}"
export PATH=~/.gem/ruby/2.2.0/bin:$PATH

echo "${yellow}Checking Dependencies${reset}"
if [ -f ~/.gem/ruby/2.2.0/bin/bundler ]
then
	echo "${green}Found Bundler${reset}"
else
	echo "${red}Installing Bundler${reset}"
	gem install bundler
fi

echo "${yellow}Checking Dependencies${reset}"
if [ -d vendor ]
then
	echo "${green}Found vendor folder
Statring Jekyll${reset}"
else
	echo "${red}Installing Dependencies${reset}"
	bundle install --path vendor/bundle
	echo "${green}Statring Jekyll${reset}"
fi
xdg-open http://0.0.0.0:4000 &
echo "${red}You Will Need To Refresh Your Browser After The Server Starts${reset}"
bundle exec jekyll serve

