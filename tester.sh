#!/usr/bin/env bash


#colors
red=$(tput setaf 1)
green=$(tput setaf 2)
yellow=$(tput setaf 3)
reset=$(tput sgr0)

echo "${green} _____ __    _____ _____"
echo "|     |  |  |  |  |   __|"
echo "|   --|  |__|  |  |  |  |"
echo "|_____|_____|_____|_____|${reset}"

echo "${yellow}Exporting path${reset}"

rbversion=$(ruby --version | awk '{print substr($2, 0, 4)}' | awk '$1=$1"0"')
case "$rbversion" in

	$rbversion)
	echo "${yellow}Setting path For${reset}${green} $rbversion${reset}"
	export PATH=~/.gem/ruby/$rbversion/bin:$PATH
	;;
	$rbversion)
	echo "$rbversion path set"
	export PATH=~/.gem/ruby/"$rbversion"/bin:$PATH
	;;
	*)
	echo "$rbversion"
	;;

esac

echo "${yellow}Checking Dependencies${reset}"
if [ -f ~/.gem/ruby/"$rbversion"/bin/bundler ]
	then
	echo "${green}Found Bundler${reset}"

elif [ -f ~/.gem/ruby/"$rbversion"/bin/bundler ]
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
	echo "${green}Updating Dependencies${reset}"
	bundle install --path vendor
else
	echo "${red}Installing Dependencies${reset}"
	bundle install --path vendor
fi

echo "${yellow}Checking for old _site${reset}"
if [ -d _site ]
	then
	echo "${red}Cleaning up site cache${reset}"
	rm -rf _site
	echo "${green}Done${reset}"
else
	echo "${green}All set${reset}"
fi

echo "${green}Opening Browser Tab...${reset}"
echo "${yellow}You Will Need To Refresh Your Browser After The Server Starts${reset}"
sleep 5
xdg-open http://0.0.0.0:4000 &


echo "${green}Statring Jekyll${reset}"

bundle exec jekyll serve

#jekyll=$! if jekyll is forked to the background this grabs the pid
#kill $jekyll This kill the grabbed pid
#trap '{ echo " Time to quit." 'kill $jekyll' }' Its a TRAP


echo ""
echo "Bye!"
exit
