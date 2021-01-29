# TCP Centralized Client-Server Network 

## Description

This is a really cool stealth chat room that runs in your command console. It uses TCP paired with a custom OOP message protocol that is easy to understand.

This project uses the base socket library and enables communication between the server and multiple clients. The main goal of this project is to create a way for multiple clients to exchange messages with each other as well as create and join chat rooms.

## Running

This project was developed using the python 3.8.3

in server folder
  * python server.py
  
in client folder
  * python client.py
  
 NOTE: This requires you have multiple terminal windows open, 1 for server, 1 for each client

* Attach screenshots or videos to this file to illustrate how your program works for all the options in the menu. 

Video of functions: https://youtu.be/oouuf_Crz60

## Notes

My method of implementation was similar to how a 'public' folder works in traditional web development. I use the server to send a python file, 'menu.py' to the client.
The client receives the file in bytes and rewrites it into its own directory. Now that the file is there we can use its function to simplify the clients code. My protocol
is that the client receives a file and an object and then calls the run() method on that object. This makes the project more scaleable as many different files could be sent if necessary. The only real issue I ran into was creating a chat room that can both receive and print messages as well as listen for user input. I achieved this by creating a new thread whos responsibilty is to only receive and print messages. One thing I never figured out was how to keep a input symbol 'username>' at the bottom of the chat room as every time a new message came in it would be write over the input prompt. I decided to just remove the input string as it functioned and looked better when I did.  

