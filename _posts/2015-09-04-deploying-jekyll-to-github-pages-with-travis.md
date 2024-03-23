---
layout: post
title: Deploying a Jekyll Blog to GitHub Pages using Travis CI
tags:
- jekyll
- github
- github-pages
- travis-ci
- continuous-deployment
- ruby
- make
- markdown
- yaml
---

[Jekyll](https://jekyllrb.com/) is a "blog-aware static site generator" written in [Ruby](https://www.ruby-lang.org/) that will generate a responsive website from [Markdown](https://help.github.com/articles/markdown-basics/) and [YAML](https://yaml.org/) files.

[GitHub Pages](https://pages.github.com/) offers you a free way to host static websites. And while they will automatically publish files in a repository named `<your-github-id>.github.io`, sometimes you need a little more control over the process.

## Project Tooling

After running `$ jekyll new`, the base project structure will be generated for you. To simplify setup on additional machines and enable continuous deployment, I like to add additional tooling to this project.

### Gemfile

A [`Gemfile`](https://raw.githubusercontent.com/jacebrowning/info/main/Gemfile) is used to specify the Ruby dependencies ("Gems") required to generate the website. In addition to `jekyll`, I'm using:

* `rouge` - to provide syntax highlighting in code examples
* `html-proofer` - to confirm that external links are valid

### Gemfile.lock

The [`Gemfile.lock`](https://raw.githubusercontent.com/jacebrowning/info/main/Gemfile.lock) is automatically generated when installing Gems. It's purpose is to record of the exact version of each dependency the last time the project was successfully deployed.

### Bundler

`bundler` is a tool that can install and run particular versions of Gems for a project. I prefer to store the Gems locally via `$ bundler install --path vendor` so that I'm not polluting my system directories and can completely delete all files a project creates.

### Makefile

A [`Makefile`](https://raw.githubusercontent.com/jacebrowning/info/main/Makefile) puts everything together. I like using `make` (rather than `rake`) because it doesn't depend on Ruby itself, does a good of tracking when files have changed, and provides a standard interface between projects.

I'll highlight the important parts of this file. This reinstalls the dependencies whenever they change:

```makefile
VENDOR_DIR := vendor
INSTALLED_FLAG := $(VENDOR_DIR)/.installed

.PHONY: install
install: $(INSTALLED_FLAG)
$(INSTALLED_FLAG): Gemfile* Makefile
    bundle install --path vendor
    @ touch $(INSTALLED_FLAG)
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


See the [source code]({{ site.repo }}) that generates **this** site as an example of how these files are used together in practice.

## Developing Locally

Using the above tooling, my only system dependencies are `ruby`, `bundler`, and `make`. To work on a new blog entry, I simply run:

```shell
$ make launch
```

to bring up a local instance of the site that is regenerated whenever I edit content.

When I am done editing, running `$ make ci` will confirm that the site is ready to be published.

## Deploying with Travis CI

[Travis CI](https://travis-ci.org/) offers free continuous integration for open source projects that can be used to deploy software after running a number of checks.

Adding a [`.travis.yml`](https://github.com/jacebrowning/jacebrowning.info/blob/55c13120f6aac2ddff4aa6eeead106fb547b8998/.travis.yml) to your project tells Travis CI how to build and deploy your site. This specifies which commands to run to install and validate each commit:

```yaml
install:
- make install

script:
- make ci
```

If a new commit passes those checks, the following shell script is run:

```shell
# Generate HTML
make build ;
# Configure Git with Travis CI information
git config --global user.email "travis@travis-ci.org" ;
git config --global user.name "travis-ci" ;
# Delete the current repository
rm -rf .git ;
# Rebuild the repository from the generated files and push to GitHub pages
cd _site ;
git init ;
git add . ;
git commit -m "Deploy Travis CI build $TRAVIS_BUILD_NUMBER to GitHub pages" ;
git push -f https://${GH_TOKEN}@github.com/${TRAVIS_REPO_SLUG} main:gh-pages ;
```

which will publish the generated files to the `gh-pages` branch on GitHub.

`GH_TOKEN` is an encrypted access token to grant Travis CI permissions to modify files in your repository. [This site](https://benlimmer.com/2013/12/26/automatically-publish-javadoc-to-gh-pages-with-travis-ci/) provides a good overview on generating these tokens.

After deployment, you should now see your Jekyll blog live at:

`https://<your-github-id>.github.io/<your-repository-name>`

-----

See a typo? Help me [edit]({{ site.repo }}/edit/main/{{page.path}}) this post.
