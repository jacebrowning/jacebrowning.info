import os
import re
from urllib.parse import unquote

mashup_links = """
04 Time In My Head.mp3
02 Your Mom.mp3
08 Billie's Back.mp3
03 Never Watching.mp3
09 Goodnight Kryptonite.mp3
07 She Said Put Your Loving Hand Out.mp3
01 The Speed of Clocks.mp3
05 Summer's Ending Soon My Old Friend.mp3
06 In a Day or Two I Can't Explain.mp3
""".strip().splitlines()

remix_links = """
07 Disarm [Remix].mp3
04 Spirited.mp3
06 Snakes on a Plane [Remix].mp3
01 Annie Waits [Remix].mp3
05 Everytime You Touch Me [Remix].mp3
03 Beautiful Day [Remix].mp3
02 Not the Same [Remix].mp3
""".strip().splitlines()

original_links = """
11 Partition.mp3
12 Nyemix.mp3
07 Comeback.mp3
09 Cloud.mp3
05 Rise.mp3
10 Runner.mp3
01 Hypertrax.mp3
13 Makedown.mp3
""".strip().splitlines()

mashup_links = [f"/downloads/mashups/{filename.replace(' ', '%20')}" for filename in mashup_links]
remix_links = [f"/downloads/remixes/{filename.replace(' ', '%20').replace('[', '%5B').replace(']', '%5D')}" for filename in remix_links]
original_links = [f"/downloads/originals/{filename.replace(' ', '%20')}" for filename in original_links]

music_md_template = """
---
layout: page
title: Music
---

Here are some of my favorite electronica songs I've created over the years.

## Mashups

{mashups}

## Remixes

{remixes}

## Originals

{originals}
""".lstrip()

audio_player_template = """
<div class="audio-player">
  <div class="title-download-container">
    <span>{title}</span>
    <a href="{download_link}" class="download-link" download="{download_filename}">Download</a>
  </div>
  <audio controls style="width:100%;">
    <source src="{download_link}" type="audio/mpeg">
  </audio>
</div>
""".lstrip()

def extract_title(url):
    filename = os.path.basename(url)
    title = os.path.splitext(filename)[0]
    title = unquote(title)
    title = re.sub(r'^\d+\s*', '', title)
    return title

def generate_audio_players(links, category):
    audio_players = []
    for link in links:
        title = extract_title(link)
        download_link = f"/downloads/{category}/{link.split('/')[-1]}"
        download_filename = f"Jace Browning - {title}.mp3"
        if "[Remix]" in title:
            title = title.replace('[Remix]', '').strip()
        audio_players.append(audio_player_template.format(title=title, download_link=download_link, download_filename=download_filename))
    return "\n".join(audio_players)

mashups = generate_audio_players(mashup_links, "mashups")
remixes = generate_audio_players(remix_links, "remixes")
originals = generate_audio_players(original_links, "originals")

music_md_content = music_md_template.format(mashups=mashups, remixes=remixes, originals=originals)

with open("music.md", "w") as f:
    f.write(music_md_content)
