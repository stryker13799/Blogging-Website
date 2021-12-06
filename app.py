import streamlit as st
import pandas as pd
from db import *
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
st.set_option('deprecation.showPyplotGlobalUse', False)

##################################################### USER Control #####################################################################


avatar1 ="https://www.w3schools.com/howto/img_avatar1.png"
avatar2 ="https://www.w3schools.com/howto/img_avatar2.png"


def readingTime(mytext):
	total_words = len([ token for token in mytext.split(" ")])
	estimatedTime = total_words/200.0
	return estimatedTime

title_temp ="""
	<div style="background-color:#FF0000;padding:10px;border-radius:10px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
	<h6>Author:{}</h6>
	<br/>
	<br/>	
	<p style="text-align:justify">{}</p>
	</div>
	"""

comment_title ="""
	<div style="background-color:#808080;padding:7px;border-radius:7px;margin:7px;">
	<h1 style ="text-align:left">Name: {}</h5>
	<br/>
	<br/>	
	<p style="text-align:justify">{}</p>
	</div>
	"""

article_temp ="""
	<div style="background-color:#FF0000;padding:10px;border-radius:5px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<h6>Author:{}</h6> 
	<h6>Post Date: {}</h6>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
	<br/>
	<br/>
	<p style="text-align:justify">{}</p>
	</div>
	"""
head_message_temp ="""
	<div style="background-color:#FF0000;padding:10px;border-radius:5px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;">
	<h6>Author:{}</h6> 		
	<h6>Post Date: {}</h6>		
	</div>
	"""
full_message_temp ="""
	<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
		<p style="text-align:justify;color:black;padding:10px">{}</p>
	</div>
	"""

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

def app(username=''):

		

	menu = ["My Articles","Add Post","Delete Post","Add Comment","Add Rating"]
	choice = st.sidebar.selectbox("User Menu",menu)

	if choice == "My Articles":
		st.subheader("My Articles")
		author_posts = get_blog_by_author(username)
		for i in author_posts:
			st.text("Reading Time:{} minutes".format(readingTime(str(i[2]))))
			st.markdown(head_message_temp.format(i[1],i[0],i[3]),unsafe_allow_html=True)
			st.markdown(full_message_temp.format(i[2]),unsafe_allow_html=True)
	
	elif choice == "Add Post":
		st.subheader("Add Your Article")
		create_table()
		blog_title = st.text_input('Enter Post Title')

		blog_article = st.text_area("Enter Your Message",height=200)
		blog_post_date = st.date_input("Post Date")
		if st.button("Add"):
			if len(blog_title)<1 or len(blog_article)<1:
				st.warning("Empty Title or Empty Blog article")
			else:
				add_data(username,blog_title,blog_article,blog_post_date)
				st.success("Post::'{}' Saved".format(blog_title))

	elif choice =="Delete Post":
		st.subheader("Delete Blogposts")
		unique_list = [i[0] for i in view_all_titles_by_author(username)]
		delete_by_title =  st.selectbox("Select Title",unique_list)
		if st.button("Delete Articles"):
			delete_data(delete_by_title)
			st.warning("Deleted: '{}'".format(delete_by_title))

	elif choice == "Add Comment":
		st.subheader("Add Your Comment")
		create_table()
		all_titles = [i[0] for i in view_all_titles()]
		postlist = st.selectbox("Articles",all_titles)
		

		blog_comment = st.text_area("Enter Your Message",height=200)
		blog_post_date = st.date_input("Post Date")
		if st.button("Add"):
			if len(blog_comment)<1:
				st.warning("Empty comment")
			else:
				add_commment(username,postlist,blog_comment,blog_post_date)
				st.success("Comment Added")

	elif choice == "Add Rating":
		st.subheader("Add Your Rating")
		create_table()
		all_titles = [i[0] for i in view_all_titles()]
		postlist = st.selectbox("Articles",all_titles)
		

		rating = st.text_input("Enter Rating")
		if rating:
			rating =int(rating)
		blog_post_date = st.date_input("Post Date")
		if st.button("Add"):
			if rating <0 or rating >10:
				st.warning("Rating should be between 10 and and 0")
			else:
				rate=fetch_rating(postlist)
				if rate:
					rati=rate[0][0]
					num_exp=float(rate[0][2]+1)
					rati=rating

					update_rating_at(postlist,rati,num_exp)
					
				else:
					insert_rating(postlist,rating)

				st.success("Rating Added")
#################################################### Admin Control #################################################################################


def admin_control():

		

	menu = ["View Post","Add Post","Search","Manage Blogposts","Manage Users"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "View Post":
		st.subheader("View Post")

		all_titles = [i[0] for i in view_all_titles()]
		postlist = st.sidebar.selectbox("Posts",all_titles)
		post_result = get_blog_by_title(postlist)
		for i in post_result:
			st.text("Reading Time:{} minutes".format(readingTime(str(i[2]))))
			st.markdown(head_message_temp.format(i[1],i[0],i[3]),unsafe_allow_html=True)
			st.markdown(full_message_temp.format(i[2]),unsafe_allow_html=True)

	elif choice == "Add Post":
		st.subheader("Add Your Article")
		create_table()
		blog_title = st.text_input('Enter Post Title')
		blog_author = st.text_input("Enter Author Name",max_chars=50)
		blog_article = st.text_area("Enter Your Message",height=200)
		blog_post_date = st.date_input("Post Date")
		if st.button("Add"):
			add_data(blog_author,blog_title,blog_article,blog_post_date)
			st.success("Post::'{}' Saved".format(blog_title))


	elif choice == "Search":
		st.subheader("Search Articles")
		search_term = st.text_input("Enter Term")
		search_choice = st.radio("Field to Search",("title","author"))
		if st.button('Search'):
			if search_choice == "title":
				article_result = get_blog_by_title(search_term)
			elif search_choice =="author":
				article_result = get_blog_by_author(search_term)
			
			for i in article_result:
				st.text("Reading Time:{} minutes".format(readingTime(str(i[2]))))
				st.write(head_message_temp.format(i[1],i[0],i[3]),unsafe_allow_html=True)
				st.write(full_message_temp.format(i[2]),unsafe_allow_html=True)
			

	elif choice == "Manage Blogposts":
		st.subheader("Managing Blogposts")
		result = view_all_notes()
		clean_db = pd.DataFrame(result,columns=["Author","Title","Article","Date","Index"])
		unique_list = [i[0] for i in view_all_titles()]
		delete_by_title =  st.selectbox("Select Title",unique_list)
		if st.button("Delete Articles"):
			delete_data(delete_by_title)
			st.warning("Deleted: '{}'".format(delete_by_title))

		if st.checkbox("WordCloud"):
			
			st.subheader("Word Cloud")
			text = ', '.join(clean_db['Article'])
			wordcloud = WordCloud().generate(text)
			plt.imshow(wordcloud, interpolation='bilinear')
			plt.axis("off")
			st.pyplot()

		if st.checkbox("Barh Plot"):
				st.subheader("Length of Articles")
				new_df = clean_db
				new_df['Length'] = new_df['Article'].str.len() 
				barh_plot = new_df.plot.barh(x='Author',y='Length',figsize=(10,10))
				st.write(barh_plot)
				st.pyplot()


	elif choice =="Manage Users":
		st.subheader("Delete Users")
		unique_list = [i[0] for i in view_all_users()]
		delete_users =  st.selectbox("Select Users",unique_list)
		if st.button("Delete User"):
			delete_user(delete_users)
			st.warning("Deleted: '{}'".format(delete_users))






############################################# LOGIN ##############################################################################################

def main():
	

	html_temp = """
		<div style="background-color:{};padding:10px;border-radius:10px">
		<h1 style="color:{};text-align:center;">BIRGI BLOGGING </h1>
		</div>
		"""
	st.markdown(html_temp.format('Purple','white'),unsafe_allow_html=True)

	menu = ["Home","Login","SignUp","View Articles","Search"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")		
		result = view_all_notes()
		for i in result:
			short_article = str(i[2])[0:50]
			st.write(title_temp.format(i[1],i[0],short_article),unsafe_allow_html=True)

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
	
		if st.sidebar.checkbox("Login"):
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))

			if username =='admin' and password=='admin':
				st.success("Logged In as {}".format(username))
				admin_control()


			elif result:

				st.success("Logged In as {}".format(username))

				app(username=username)
			else:
				st.warning("Incorrect Username/Password")
		if st.sidebar.checkbox("Forget Password"):
			create_usertable()
			username = st.text_input("User Name",key="unique")
			keyword=st.text_input("hidden keyword")
			new_password = st.text_input("New Password",type='password',key="unique1")
			if st.button("change password"):
				data=search_user(username,keyword)
				if data:
					if len(new_password)<8:
						st.warning("Password should be atleast of 8 length")
					else:
						change_password(username,make_hashes(new_password))
						st.success("Your password has been updated")
						st.info("Go to Login Menu to login")

				else:
					st.warning("Username doesn't exists or keyword is incorrect")




			



	elif choice =='View Articles':
		st.subheader("Articles")

		all_titles = [i[0] for i in view_all_titles()]
		postlist = st.sidebar.selectbox("Articles",all_titles)
		post_result = get_blog_by_title(postlist)
		for i in post_result:
			st.text("Reading Time:{} minutes".format(readingTime(str(i[2]))))
			st.markdown(head_message_temp.format(i[1],i[0],i[3]),unsafe_allow_html=True)
			st.markdown(full_message_temp.format(i[2]),unsafe_allow_html=True)

		st.write("Ratings: ")
		rating=fetch_rating(postlist)
		# st.write(rating)
		if rating:
			st.write(rating[0][0])

		st.write("Comments")
		result = fetch_comments(postlist)
		for i in result:
			short_article = str(i[2])
			st.write(comment_title.format(i[0],short_article),unsafe_allow_html=True)


	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		number=st.text_input("hidden keyword")
		new_password = st.text_input("Password",type='password')
		


		if st.button("Signup"):
			create_usertable()
			if len(new_password)<8:
				st.warning("Password should be atleast of 8 length")
			else:
				add_userdata(new_user,make_hashes(new_password),number)
				st.success("You have successfully created a valid Account")
				st.info("Go to Login Menu to login")

	elif choice == "Search":
		st.subheader("Search Articles")
		search_term = st.text_input("Enter Term")
		search_choice = st.radio("Field to Search",("title","author"))
		if st.button('Search'):
			if search_choice == "title":
				article_result = get_blog_by_title(search_term)
			elif search_choice =="author":
				article_result = get_blog_by_author(search_term)
			
			for i in article_result:
				st.text("Reading Time:{} minutes".format(readingTime(str(i[2]))))
				st.write(head_message_temp.format(i[1],i[0],i[3]),unsafe_allow_html=True)
				st.write(full_message_temp.format(i[2]),unsafe_allow_html=True)
			


if __name__ == '__main__':
	main()