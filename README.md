# Corporate Sales Feedback App

## Functions
Submitter: Submit anonymous feedback with an associated SalesForce opportunity link

Manager: Receive and manage feedback

Admin: Add, remove, and edit manager accounts

## Technologies
Front-end: Vue.js, jQuery

Back-end: Django

## Features
Email notifications for managers when feedback is submitted

Password reset and username recovery via email

All forms secured through Django

Encrypted passwords. Passwords cannot be viewed or edited, only reset


## Deployment
Via Apache and mod_wsgi on an Ubuntu 18.04 LTS server on Amazon EC2. SQLite database due to convenience and small user base.

## Challenges
Learning how to use Django

Learning Unix commands and working on a Linux VM for the first time

Building a REST API using Django and integrating this API with Vue.js

Deploying using Apache and mod_wsgi for the first time
