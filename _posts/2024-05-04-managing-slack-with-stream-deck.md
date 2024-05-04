---
layout: post
title: Managing Slack with Stream Deck
tags:
- slack
- slackoff
- stream-deck
- macos
---

If you're in multiple Slack workspaces, you know it can get distracting to see unread message notifications. [Slackoff](https://github.com/jacebrowning/slackoff) is a tool to help you automatically sign out of Slack workspaces (on macOS) to improve focus. This guide will show you how to connect Slack to a [Stream Deck](https://www.elgato.com/us/en/p/stream-deck-mk2-black) to toggle workspaces with the push of a button.

## Slackoff

### Installation

Slackoff is easiest to install with [pipx](https://pipx.pypa.io/), a tool to run Python applications in isolated environments. To install that on macOS:

```shell
$ brew install pipx
```

Add this line to your shell config (e.g. `~/.zshrc`):

```
export PATH="${HOME}/.local/bin:${PATH}"
```

Then in a new terminal window you should be able to install Slackoff:

```
$ pipx install slackoff
$ slackoff --version
```

### Usage

To test that it's working, try toggling one of your Slack workspaces:

```
$ slackoff --signout My Company Workspace
$ slackoff --signin My Company Workspace
```

where "My Company Workspace" is the name of one of your Slack workspaces. You may need to grand accessibility permissions to your terminal application.

Slackoff will also remember the last used workspace so you can toggle it with a single command:

```
$ slackoff
```

## Stream Deck

## Setup

To call Slackoff from a Stream Deck action, we first need to create a wrapper script. Open the Script Editor application on macOS and paste the following:

```applescript
do shell script "/Users/Browning/.local/bin/slackoff"
```

where "Browning" is your user name. Save that file somewhere that Stream Deck can find it.

Next, add the **System > Open** action to a button:

![](https://cdn.zappy.app/912d066cbd607bb9205f547b53b98945.png)

Then, configure that action to call the AppleScript you created:

![](https://cdn.zappy.app/f3c781c2d318b623f32684b0d1acdde9.png)

## Usage

At the start and end of each day, simply press that Stream Deck button to toggle Slack workspaces. Enjoy your improved work-life balance! 🎉

-----

See a typo? Help me [edit]({{ site.repo }}/edit/main/{{page.path}}) this post.
