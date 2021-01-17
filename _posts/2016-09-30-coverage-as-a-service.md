---
layout: post
title: Test Coverage as a Service
tags:
- coverage
- api
- restful
- testing
- metrics
---

Measuring coverage is an important, but sometimes forgotten part of running tests. One of the common debates is around how much coverage a project should have: 50%, 80%, 100%?

More important than the actual coverage metrics is ensuring that your coverage metrics don't decrease when adding new code. Coverage metrics don't tell us when a particular section of code has enough tests, but they do help inform us when a section of code has zero tests.

## Tracking Metrics

A few options exist for tracking coverage metrics.

### Version Control

The naive solution is to commit coverage metrics to a file in your project repository. When tests are run, check this file and report an error if coverage decreased. The main disadvantage of this approach is having lots of commits unrelated to functional changes, which adds noise to your repository.

### External Services

Many external services exist to track coverage metrics. One such example is [Coveralls](https://coveralls.io/). This service works great and is highly recommended for open-source projects to track coverage on pull requests. The main disadvantages of this service are the costs for private repositories and the inability to check coverage metrics locally.

## The Coverage Space

[coverage.space](https://coverage.space) is a new RESTful API to track coverage metrics that aims to find a balance between these two options.

### Basic Usage

The easiest way to get started with The Coverage Space is to use an HTTP client. [HTTPie](https://github.com/jkbrzt/httpie) works well for this:

```sh
$ pip install HTTPie
```

Update metrics for your project:

```sh
$ http PUT api.coverage.space/my_owner/my_repo unit=90
```

where `my_owner/my_repo` matches your project.

Check out the full API documentation at [coverage.space/api](https://coverage.space/api/).

### Command-line Client

A command-line client is also available to automate the process of reading and uploading coverage metrics:

```sh
$ pip install --update coverage.space
```

After running your tests with coverage enabled, update metrics for your project:

```sh
$ coverage.space my_owner/my_repo unit
```

where `my_owner/my_repo` matches your project.

Check out the full client documentation at [cli.coverage.space](https://cli.coverage.space).

-----

See a typo? Help me [edit]({{ site.repo }}/edit/main/{{page.path}}) this post.

Interested in seeing the full implementation? Check out the [code]({{ site.author.github }}/coverage-space) on GitHub.

