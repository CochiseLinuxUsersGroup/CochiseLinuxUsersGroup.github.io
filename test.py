#!/usr/bin/env python2
import os;
import datetime;

choice_list = ["1. New Page", "2. New Post", "3. New Talk (un-stable option)", "4. List Posts", "5. List Talks", "6. Run Test Environment", "7. Update Test Environment"]

for line in choice_list:
	print line

choice = raw_input("Please select what you want to do. ")


if choice in {'1', 'New Page'}:
	new_page = raw_input("What is the title of the new page? ") #name of page
	new_page_formatted = new_page.replace(" ", "_")
	os.system("mkdir " + new_page_formatted) # create new directory for page
	print 'Creating directory: ' + new_page_formatted 
	os.system("touch " + new_page_formatted + "/" + "index.md") # create default index.md in dir
	print 'Creating file: ' + new_page_formatted + '/' + 'index.md'
	default_text = raw_input("Would you like to generate the default page config? [Yes/No]: ") # generate info into index.md y/n
	pagemd = new_page_formatted + '/index.md' # set pagemd equal to newdir/index.md

	#if yes for generation
	if default_text in {'Yes', 'yes', 'Y', 'y'}:
		os.system("echo '---' > " + pagemd)
		os.system("echo 'layout: page' >> " + pagemd)
		os.system("echo 'title: ' " + new_page + ">> " + pagemd)
		os.system("echo 'permalink: /" + new_page_formatted + "/' >> " + pagemd)
		os.system("echo 'post-image: /img/clug_banner_1-compressor.jpg' >> " + pagemd)
		os.system("echo '---' >> " + pagemd)
		os.system("cat " + pagemd)
		print 'Your new page can be found here: ' + pagemd
		open_choice = raw_input('Would you like to edit the new page further? [Yes/No] ')
	
	
		# open in default text editor
		if open_choice in {'Yes', 'yes', 'Y', 'y'}:
			os.system("xdg-open " + pagemd)
		else:
			print 'Ok we are done here'

	#if no for generation
	if default_text in {'No', 'no', 'N', 'n'}:
		print 'Ok, your new page can be found here: ' + pagemd
	
if choice in {'2', "New Post"}:
	td_date = datetime.date.today().strftime("%Y-%m-%d-")
	new_post = raw_input("Enter the new post title: ")
	new_post_formatted = new_post.replace(" ", "-")
	os.system("touch _posts/" + td_date + new_post_formatted + ".md") 
	postmd = '_posts/' + td_date + new_post_formatted + '.md'
	default_post = raw_input("Would you like to generate the default page config? [Yes/No]: ")
	
	if default_post in {'Yes', 'yes', 'Y', 'y'}:
		post_content = raw_input("Enter the post content: ")
		os.system("echo '---' > " + postmd)
		os.system("echo 'layout: post' >> " + postmd)
		os.system("echo 'title: " + '"' + new_post + '"' + "' >> " + postmd)
		os.system("echo 'author: python' >> " + postmd)
		os.system("echo 'category: test' >> " + postmd)
		os.system("echo '---' >> " + postmd)
		os.system("echo '" + post_content + "' >> " + postmd)
		print 'Your post can be found here: ' + postmd
		open_choice = raw_input('Would you like to edit the new post further? [Yes/No] ')
		
		
		# open in default text editor
		if open_choice in {'Yes', 'yes', 'Y', 'y'}:
			os.system("xdg-open " + postmd)
		else:
			print 'Ok we are done here'
	
	if default_post in {'No', 'no', 'N', 'n'}:
		print 'Your post can be found here: ' + postmd
	
if choice in {'3', 'New Talk'}:
	td_date = datetime.date.today().strftime("%Y-%m-%d")
	os.system("head -n -2 talks/talks.json > talks/temp.json")
	os.system("mv talks/temp.json talks/talks.json")
		
	name = raw_input("Please enter the name of your talk. [Required] ")
	while not name:
		print "You didnt enter a name for the talk."
		name = raw_input("Please enter the name of your talk. [Required] ")
	
	title = raw_input("Please add a title for the talk. [Required] ")
	while not title:
		print "You didnt enter a title for the talk."
		title = raw_input("Please add a title for the talk. [Required] ")
		
	talk_date = raw_input("Please enter the date the talk will take place. [yyyy-mm-dd] ")
	while not talk_date:
		print "You didn't enter a date, using today's date."
		talk_date = td_date
		
	os.system("echo -e '\t''}, {' >> talks/talks.json")
	os.system("echo -e '\t''\t''\"'name'\"': '\"'" + name + "'\"'',' >> talks/talks.json")
	os.system("echo -e '\t''\t''\"'title'\"': '\"'" + title + "'\"'',' >> talks/talks.json")
	os.system("echo -e '\t''\t''\"'date'\"': '\"'" + talk_date + "'\"'',' >> talks/talks.json")
	
	url = raw_input("Enter the url for the talk: [Optional] ")
	if not url:
		os.system("echo -e '\t''\t''\"'url'\"': '\"''\"'',' >> talks/talks.json")
	else:
		os.system("echo -e '\t''\t''\"'url'\"': '\"'" + url + "'\"'',' >> talks/talks.json")
	
	os.system("echo -e '\t''\t''\"'country'\"': '\"'us'\"'',' >> talks/talks.json")
	os.system("echo -e '\t''\t''\"'city'\"': '\"'Sierra Vista, AZ'\"' >> talks/talks.json")
	os.system("echo -e '\t''}' >> talks/talks.json")
	os.system("echo -e ] >> talks/talks.json")

if choice in {'4', 'List Posts'}:
	list_posts = os.system("ls -l _posts/ | awk '{print $9}' | sed -r 's/.{11}//' | sed -r 's/.{3}$//' | nl")
	
if choice in {'5', 'List Talks'}:
	print "Here are a list of existing talks. "
	os.system("less talks/talks.json | grep title | awk '{print $2, $3, $4}' | sed 's/,//' | sed 's/\"//g' |  nl")

if choice in {'6', 'Run Test Environment'}:
	os.system("bash install.sh")

if choice in {'7', 'Update Test Environment'}:
	os.system("bundle update")


