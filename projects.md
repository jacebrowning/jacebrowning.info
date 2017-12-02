---
layout: page
title: Projects
---

I enjoy building command-line utilities to automate developments tasks. Lately, I've been getting into more web development for fun. This projects list is more or less in order of completion date.

## Doorstop

For my masters thesis at [GVSU](http://scholarworks.gvsu.edu/oapsf_articles/32/), I built a tool to help manage engineering requirements using version control:

> [doorstop.readthedocs.io](https://doorstop.readthedocs.io/)

I am no longer actively working on this program, but many people continue to find it useful in their projects.

## GR Parks

A local "civic hacking" group, [Citizen Labs](http://citizenlabs.org/), started a project with the City of Grand Rapids to display parks millage dollars on a map:

> [grparks.citizenlabs.org](https://grparks.citizenlabs.org/)

We hope to be able to produce similar maps for other municipalities and explore additional datasets.

## YORM

Inspired by the pleasant experience of using YAML to store program data when designing Doorstop, I decided to extract some of the core functionality into a library:

> [yorm.readthedocs.io](https://yorm.readthedocs.io/)

I have since used this library as the base for lots of tools. Read more [on the blog]({% post_url 2015-05-17-yorm-v0.4-released %}).

## Mine

Taking advantage of the data storage provide by YORM, I built a tool to synchronize the state of running applications using a YAML file saved in Dropbox:

> [mine.readthedocs.io](https://mine.readthedocs.io/)

I use this program every day to access my music library in iTunes. Read more [on the blog]({% post_url 2015-03-24-syncing-itunes-using-dropbox-with-mine %}).

## GitMan

At several jobs, my team ran into the problem of needing to manage multiple Git repositories and found Git's submodules feature to be lacking. Out of this need, a new command-line utility arose:

> [gitman.readthedocs.io](https://gitman.readthedocs.io/)

I still use this tool nearly every day to simplify the task of cloning lots of Git repositories for work. Read more [on the blog]({% post_url 2015-08-07-replacing-submodules-with-gitman %}).

## MemeGen.link

When using [Slack](https://slack.com/) for communication with colleagues and friends, I found we needed a simple way to create and share memes as links to images. Few of the existing meme generators allowed hot-linking to images, so I build an API to generate memes:

> [memegen.link](https://memegen.link)

Many chat bots have been written to use the API and the service continues to get around 30k image requests per day. Read more [on the blog]({% post_url 2016-01-24-google-analytics-on-image-requests %}).

## The Coverage Space

I try to enable test coverage in all of my projects as a gut check that new functionality has not decreased the overall coverage. To avoid storing the minimum coverage metric in each project's repository, I build a simple API to track code coverage metrics:

> [coverage.space](https://coverage.space/)

I have already started using this in most of my projects to detect when code coverage decreases. Read more [on the blog]({% post_url 2016-09-30-coverage-as-a-service %}).

## Crowd Sorter

I've always been fascinated with how people tend to use ratings as a ranking system. Inspired by other ranking sites, I build a tool to manage lists of arbitrary items  and leverage the public to help sort it:

> [crowdsorter.com](https://crowdsorter.com/)

For an example, help me pick my next blog topic: [crowdsorter.com/nbtyxexqjk](https://crowdsorter.com/nbtyxexqjk)

## Virtual Boombox

I've used [Last.fm](https://www.last.fm/about/trackmymusic) for as long as I've been into music. Connecting scrobbling data to locations, I built an application to discover music playing nearby:

> [virtualboombox.com](https://virtualboombox.com/)

## Meme Complete

Autocomplete for memes via text and speech.

> [memecomplete.com](https://memecomplete.com/)

## MediaVouch

Your playlist for everything.

> [mediavouch.com](https://mediavouch.com/)

-----

See a typo? Help me [edit]({{ site.repo }}/edit/master/{{page.path}}) this page.
