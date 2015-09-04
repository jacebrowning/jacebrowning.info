---
layout: post
title: Deploying Jekyll to GitHub using Travis CI
tags:
- jekyll
- github
- travis-ci
- continuous-deployment
- ruby
- make
---

[Jekyll](http://jekyllrb.com/) is a "blog-aware static site generator" written in [Ruby](https://www.ruby-lang.org/) that will generate a responsive website from [Markdown](https://help.github.com/articles/markdown-basics/) files.

[GitHub Pages](https://pages.github.com/) offers you a free way to host these generated sites. And while GitHub will automatically publish repositories name `<your-github-id>.github.io`, sometime you need a little more control over the process.

## Deployment Tooling

After running `$ jekyll new`, the base project structure will be generated for you. To simplify setup on additional machines and enable continuous deployment, I like to add additional tooling to this project.

### Gemfile

A `Gemfile` is used to specify the Ruby dependencies ("Gems") required to generate the website. In addition to `jekyll`, I'm using:

* `rouge` - to provide syntax highlighting in code examples
* `html-proofer` - to confirm that external links are valid

### Gemfile.lock

The `Gemfile.lock` is automatically generated when installing Gems. It's purpose is to record of the exact version of each dependency the last time the project was successfully deployed.

### Bundler

`bundler` is a tool that can install and run particular versions of Gems for a project. I prefer to store the Gems locally via `$ bundler install --path vendor` so that I'm not polluting my system directories and can completely delete all files a project creates.

### Makefile

A `Makefile` puts everything together. I like using a `Makefile` (rather than a `Rakefile`) because it doesn't depend on Ruby itself, does a good of tracking when files have changed, and provides a standard interface between projects.

I'll highlight a few parts of this file. This reinstalls dependencies whenever they change:

```makefile
VENDOR_DIR := vendor
INSTALLED_FLAG := $(VENDOR_DIR)/.installed

.PHONY: install
install: $(INSTALLED_FLAG)
$(INSTALLED_FLAG): Gemfile* Makefile
    bundle install --path vendor
    @ touch $(INSTALLED_FLAG)  # indicate that dependencies are installed
```

This builds the site and validates the generated HTML:

```makefile
.PHONY: build
build: install
    bundle exec jekyll build --quiet
    bundle exec htmlproof _site --only-4xx
```

And these targets provide a way to run the site locally:

```makefile
.PHONY: run
run: install
    bundle exec jekyll serve --future --drafts

.PHONY: launch
launch: install
    eval "sleep 5; open http://localhost:4000" & make run
```


See the [source code](https://github.com/jacebrowning/info) that generates **this** site as an example of how these files are used in practice.

## Enabling Travis CI

TBD

dns: http://davidensinger.com/2013/03/setting-the-dns-for-github-pages-on-namecheap/



