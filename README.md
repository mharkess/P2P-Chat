# P2P-Chat

For this application, I will use a sqlite3 db to store chats of a user locally. I will use MySQL to store necessary user information needed to discover new users on the application (e.g name).

## Discovery Module

For this module, I have decided to use a MySQL database hosted on a server to facilitate discovering new users. The database will consist of one table that has all users who use the application. It will have one table with a username column, email column, phone number column, IP address column and Port column (could remove this and have 1 port to be used, but on different devices.). The IP address and port column will be updated everytime a user connects to the internet, to make sure that clients will be able to communicate to the user reliably, even if a client switches networks.

## Message Transmission

## Client