# HW5: Flask Webpage (Twitter clone)
 #### For this assignment  I've used Python (flask), SQL, CSS, HTML and Jinja2 to create a WEBPAGE that acts as a social network very similar to Twitter. Users can create accounts and post messages, which will be seen by everyone.<br />

## [Visit The Website](http://ohorban.pythonanywhere.com/home)
 ### Functionality:
 1. Log In
    1. Presents a from to a user to enter their username and password
    1. Displays an appropriate ERROR message if credentials are incorrect
    1. Only visible if the user is NOT logged in
1. Log Out
    1. Logs a user out
    1. Only visible if the user is logged in
1. Sign Up
    1. Presents a from to a user to enter their username, password and repeated password
    1. If the account already exists, an appropriate ERROR message will appear
    1. If 2 password don't match, an appropriate ERROR message will appear
1. Home
    1. Visible to anyone when logged in or logged out
    1. Displays all the messages in the system
    1. Messages are ordered chronologically with the most recent messages at the top
    1. Each message includes a username, a text, and the time the message was posted
    1. Has an option to delete and edit messages that were posted by the logged in user
    1. Has a button that outputs all messages in json format
1. Create a message
    1. Presents a from to a user to enter the message they want to post
1. Search
    1. Presents a from to a user to enter what messages are they looking for
    1. Outputs messages tat contain the entered word or phrase
    1. Has an option to delete and edit messages that were posted by the logged in user
1. Your Account
    1. Displays all messages that the user has posted
    1. Has an option to delete and edit messages that were posted by the logged in user
    1. Gives an option to change your password
    1. Gives an option to delete your account
1. Change Password
    1. Presents a from to a user to enter the old password, new password and repeat new password
    1. Displays appropriate message if old password is wrong
    1. If 2 new password don't match, an appropriate ERROR message will appear
1. Delete your account
    1. Deletes your username and password
    1. Keeps the messages you've posted

The website was populated with 20 accounts that posted 20 posts each. I used my propaganda generator from previous assignments to do that.
I connected my Flask app to Python Anywhere, so you can visit [The Website](http://ohorban.pythonanywhere.com/home)

### Score: 35/25