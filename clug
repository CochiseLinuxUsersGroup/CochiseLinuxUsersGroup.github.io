#!/usr/bin/env python2
import os;
import datetime;
import subprocess;

#Set choice as page or post
choice = raw_input("Would you like to generate a new page or create a post? [Page/Post]: ")
td_date = datetime.date.today().strftime("%Y-%m-%d-")

# if page statement
if choice in {'Page', 'page'}:
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
		open_choice = raw_input('Would you like to open the new page to edit it further? [Yes/No] ')
		
		if open_choice in {'Yes', 'yes', 'Y', 'y'}:
			os.system("xdg-open " + pagemd)
		else:
			print 'Ok we are done here'
	
	#if no for generation
	if default_text in {'No', 'no', 'N', 'n'}:
		print 'Ok, your new page can be found here: ' + pagemd
		
# if post statement		
elif choice in {'Post', 'post'}:
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
	
	if default_post in {'No', 'no', 'N', 'n'}:
		print 'Your post can be found here: ' + postmd
	
# else dummy enter invalid	
else:
	print 'invalid choice'
