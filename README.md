
<p  align="center">

<img  src="https://user-images.githubusercontent.com/30529572/72455010-fb38d400-37e7-11ea-9c1e-8cdeb5f5906e.png"  />

<h2  align="center"> VIT Events - Backend </h2>

<h4  align="center"> The project consists of modules that extract information from VIT Student Welfare Department's Daily Events Emails. <h4>

</p>

  

---

[![DOCS](https://img.shields.io/badge/Documentation-see%20docs-green?style=flat-square&logo=appveyor)](https://documenter.getpostman.com/view/10749950/SzS8um1N?version=latest)



  
  

## Functionalities

- [X] API to crop image to extract informatin
- [X]  API to segment data to proper rows
  

<br>

  
  

## Instructions to run

  

* Pre-requisites:

- googleapiclient

- google_auth_oauthlib

- base64

- email

- apiclient

- PIL

- pickle

- numpy

- opencv

  

* To satisfy the requirements run the command:

```bash

sudo pip install -r requirements.txt

```

  <br/>

* Command to publish on heroku

  

```bash
heroku login
git init
heroku create
git add .
git commit -m "<YOUR MESSAGE>"
git push heroku master
```
* API endpoints
		1.  /crop
		2. /cropb64
		3. /getTable

<br>

  

## Contributors

  

*  [Mayank Kumar](https://github.com/mayankkumar2)

  
  
  

<br>

<br>

  

<p  align="center">

Made with :heart: by DSC VIT

</p>