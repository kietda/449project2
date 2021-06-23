# Overview

This is the project we’re going to build services for a web application
similar to reddit.

For this project you will build four microservices for specific functionality of this site and automation test suites for these services.

# SERVICES
# POSTING MICROSERVICE
Each post should have a title, text, a community (subreddit), an optional URL linking to a resource (e.g. a news article or picture), a username, and a date the post was made.

The following operations should be exposed:
- Create a new post
- Delete an existing post
- Retrieve an existing post
- List the n most recent posts to a particular community
- List the n most recent posts to any community

When retrieving lists of posts, do not include the text or resource URL for the post.

# VOTING MICROSERVICE
Each post maintained by the posting microservice can be voted up or down. This service should maintain the number of upvotes and downvotes for each post. A post’s score can be computed by subtracting the number of downvotes from the number of upvotes.

The following operations should be exposed:
- Upvote a post
- Downvote a post
- Report the number of upvotes and downvotes for a post
- List the n top-scoring posts to any community
- Given a list of post identifiers, return the list sorted by score.

Each upvote or downvote should include a unique identifier (e.g., a URL or database key) for the post that can be used to match votes with the posts maintained by the posting microservice.

If this service is implemented with a database separate from the posting microservice, it is not responsible for verifying the existence of a post before recording or reporting votes.

# USER ACCOUNT MICROSERVICE
Each user who registers should have the following data associated with them:
- Username
- Email
- Karma

The following operations will be exposed:
- Create user
- Update email
- Increment Karma
- Decrement Karma
- Deactivate account

The data for the user can be in the same database or different database as the other services.

# USER MESSAGING MICROSERVICE

Users can send and receive messages to each other. Messages will consist of the following data associated with them:
- Message ID
- User from
- User to
- Message timestamp
- Message contents
- Message flag

The following operations will be exposed:
- Send message
- Delete message
- Favorite message

Messaging data can be in the same database as other services or a separate one.




