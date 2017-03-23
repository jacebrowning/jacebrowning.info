---
layout: post
title: Using Heroku to Review Static Websites
tags:
- heroku
- github
- sappy
- process
- quality-assurance
- spa
---

[Heroku](https://devcenter.heroku.com/start) is a great platform to deploy your full-stack application. While not the appropriate place to deploy a production frontend application, Heroku's [Review Apps](https://devcenter.heroku.com/articles/github-integration-review-apps) offer an automated mechanism to create a temporary deployment of your application to a unique, predictable URL.

## Review Apps

After creating a Heroku account, create a ["Pipeline"](https://devcenter.heroku.com/articles/pipelines) for your project and connect it to a repository on GitHub. Heroku's Pipelines allow your application code to be deployed multiple times, from different branches.

Regardless of the technology your application uses, you will need to tell Heroku about your application's dependencies in a [manifest file](https://devcenter.heroku.com/articles/app-json-schema). The most basic `app.json` will look similar to the following:

```json
{
  "name": "grwifi",
  "scripts": {},
  "env": {},
  "formation": {},
  "addons": [],
  "buildpacks": []
}
```

## Web Server

In order to serve up our static site, we'll need to run a web server on Heroku. I developed [sappy](https://github.com/jacebrowning/sappy) specifically for the purpose of serving up single-page applications (SPAs) and static websites.

To run our application on Heroku using Sappy, we'll need to add a few files:

**`runtime.txt`** indicates that Heroku should use a Python [buildpack](https://devcenter.heroku.com/articles/buildpacks) (because Sappy is written in Python):

```
python-3.6.0
```

**`requrements.txt`** tells Heroku to install Sappy using [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)) (the package manager for Python):

```
sappy==1.1
```

**`Procfile`** specifies `sappy` as the command to run our application:

```
web: sappy --port=${PORT}
```

## Automated Deployment

After adding the above files to your repository, enable Review Apps on the pipeline we created earlier:

![enable review apps]({{ site.assets }}/enable-review-apps.png)

When new pull requests are created on GitHub, Heroku will automatically deploy the code in that branch to a separate Heroku instance:

![review app deployment]({{ site.assets }}/review-app-deployment.png)

Because the temporary application deployment performs virtually identical to production, the end-to-end testing and design review that might occur later in our quality assurance process can now be performed before the code is even merged.

-----

A working example can be found at: [github.com/jacebrowning/grwifi](https://github.com/jacebrowning/grwifi)

See a typo? Help me [edit]({{ site.repo }}/edit/master/{{page.path}}) this post.
