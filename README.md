# Email Tidy

An app to tidy up your email inbox :mailbox_with_mail: by unsubscribing from spam for you.

## How does it work?

The app works by scanning through your email inbox for certain keywords to find unsubscribe links and then makes requests to those unsubscribe links. It also checks certain email headers including the infamous List-Unsubscribe email header for unsubscribe links. :link:

## The goal of Email Tidy :heavy_check_mark:

Email Tidy's mission is to keep unwanted spam out of your inbox to save you valuable time and take back your inbox's freedom. :boom:

## Completely Open Source

Other email cleaning apps are closed source, meaning you have no idea what they are doing with your inbox, possibly selling your private data or even spying on you. Email Tidy is fully open source so you know the app is only performing the function that it needs to in order to unsubscribe you from spam. It will **never** sell your data or store the body of your emails in the system.

![freedom](https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExejZjbXhic3piZ3NhY3ZxM211d3c0aGI1bmVvdHBsdHJ5NHZsbjl1aCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6901DbEbbm4o0/giphy.gif)

### What data is stored?

This data is stored on our end in order for you to see which emails are being cleaned out and which ones are not spam:

* The sender or from email address
* The email subject
* Received email timestamp
* Unsubscribe links found per email

Again, Email Tidy will **never** store any of the body of an email.

## Technologies Used :dependabot:

The following technology is used for development of Email Tidy

### Back End

* Python :snake: Fastapi as an API router.
* Postgresql. For database storage.
* Nginx. As a server proxy
* Celery. A taskworker for unsubscribing and scanning.
* Docker and kubernetes for containerization and ease of deployment.

### Front End

* React. For ease of state management and responsive UI/UX.
* CSS. Basic styling, nothing too fancy.
