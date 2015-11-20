#!/usr/bin/env bash


#colors
red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
reset=`tput sgr0`

echo "${green} _____ __    _____ _____"
echo "|     |  |  |  |  |   __|"
echo "|   --|  |__|  |  |  |  |"
echo "|_____|_____|_____|_____|${reset}"

echo "${yellow}Exporting path${reset}"

rversion=`ruby --version | awk {'print substr($2, 0, 3)'}`
case "$rversion" in
	
	2.2)
	echo "2.2.0 path set"
	export PATH=~/.gem/ruby/2.2.0/bin:$PATH
	;;
	1.9)
	echo "1.9 path set"
	export PATH=~/.gem/ruby/1.9.0/bin:$PATH
	;;
	*)
	echo {$rversion}
	;;

esac

echo "${yellow}Checking Dependencies${reset}"
if [ -f ~/.gem/ruby/2.2.0/bin/bundler ]
	then
	echo "${green}Found Bundler${reset}"

elif [ -f ~/.gem/ruby/1.9.0/bin/bundler ]
	then
	echo "${green}Found Bundler${reset}"

else
	echo "${red}Installing Bundler${reset}"
	gem install bundler --user-install
fi


echo "${yellow}Checking Dependencies${reset}"
if [ -d vendor ]
	then
	echo "${green}Found vendor folder${reset}"
else
	echo "${red}Installing Dependencies${reset}"
	bundle install --path vendor
fi

echo "${green}Opening Browser Tab...${reset}"

xdg-open http://0.0.0.0:4000 &

echo "${yellow}You Will Need To Refresh Your Browser After The Server Starts${reset}"
echo "${green}Statring Jekyll${reset}"
notify-send "Starting Server"
bundle exec jekyll serve
echo "Bye!"
exit
