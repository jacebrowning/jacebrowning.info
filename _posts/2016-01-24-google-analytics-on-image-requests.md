---
layout: post
title: Tracking Direct Image Requests with Google Analytics
tags:
- google-analytics
- html
- javascript
- python
- flask
---

[memegen.link](https://memegen.link/) is an open source meme generator. It renders meme images based on the requested URL.

For example, `memegen.link/oprah/you-get-a-meme/and-you-get-a-meme.jpg` produces this image:

![oprah](https://memegen.link/oprah/you-get-a-meme/and-you-get-a-meme.jpg)

The site also provides an [API](https://api.memegen.link) to generate memes. This article is about the [legacy implementation](https://github.com/jacebrowning/memegen-flask) written using [Flask](https://flask.palletsprojects.com/) and [Flask API](https://www.flaskapi.org/).

## Client-side Analytics

I have added [Google Analytics](https://www.google.com/analytics/) to the index and API documentation pages using the standard approach of [embedding](https://developers.google.com/analytics/devguides/collection/analyticsjs/) JavaScript on the page:

```html
...
<body>

  <script>
    ... '//www.google-analytics.com/analytics.js','ga');
    ga('create', '<Google Analytics ID>', 'auto');
    ga('send', 'pageview');
  </script>

</body>
...
```

And while this works great for HTML rendered in the browser, direct images requests (like the meme image above) go untracked.

## Server-side Analytics

One solution is to track file downloads on the backend by posting to the Google Analytics API directly using an HTTP library like [requests](https://requests.readthedocs.io/):

```python
logging.info("Sending image: %s", path)

data = dict(
    v=1,
    tid='<Google Analytics ID>',
    cid=request.remote_addr,

    t='pageview',
    dh='memegen.link',
    dp=request.path,
    dt=title,

    uip=request.remote_addr,
    ua=request.user_agent.string,
    dr=request.referrer,
)
requests.post("https://www.google-analytics.com/collect", data=data)

return send_file(path)
```

While this will track page views for an image, much of the client's information is still unavailable using this method:

- geographic location
- language setting
- device properties

## Tricking Clients

My complete solution involves a bit of hack to return HTML instead of an image for clients that can handle it and the normal image for those that can't.

Visit [memegen.link/fry/not-sure-if-image/or-webpage.jpg](https://memegen.link/fry/not-sure-if-image/or-webpage.jpg) in your browser:

![browser]({{ site.assets }}/memegen-in-browser.png)

It appears to be an image that can be downloaded:

```sh
$ wget https://memegen.link/fry/not-sure-if-image/or-webpage.jpg
Length: 27809 (27K) [image/jpeg]
Saving to: 'or-webpage.jpg'
or-webpage.jpg 100%[============================>]  27.16K  70.7KB/s
2016-01-24 20:51:46 (70.7 KB/s) - 'or-webpage.jpg' saved [27809/27809]
```

But if you view the network tab in [Chrome's developer tools](https://developer.chrome.com/devtools), you'll see that it actually loaded a small webpage to run the same client-side Google Analytics JavaScript as above:

![network]({{ site.assets }}/memegen-network.png)

This was accomplished by detecting what content types the client can accept:

```python
mimetypes = request.headers.get('Accept', "").split(',')

if 'text/html' in mimetypes:
    send_html()
else:
    send_image()
```

If the client can handle HTML, the following is returned:

```html
<!DOCTYPE html>
<html>
<head>

  <title>NOT SURE IF IMAGE / OR WEBPAGE</title>

  <style>
    body {
      background-image: url("/fry/not-sure-if-image/or-webpage.jpg");
      background-repeat: no-repeat;
    }
  </style>

</head>
<body>

  <script>
    ...
    ga('create', '<Google Analytics ID>', 'auto');
    ga('send', 'pageview');
  </script>

</body>
</html>
```

This causes the browser to render the image as expected, but also run a bit of JavaScript to recored additional information about the client.

-----

See a typo? Help me [edit]({{ site.repo }}/edit/master/{{page.path}}) this post.

Interested in seeing the full implementation? Check out the [code]({{ site.author.github }}/memegen) on GitHub.
