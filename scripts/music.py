import os
import re
from urllib.parse import unquote

mashup_songs = [
    ("04 Time In My Head.mp3", "2010"),
    ("02 Your Mom.mp3", "2006"),
    ("08 Billie's Back.mp3", "2023"),
    ("03 Never Watching.mp3", "2006"),
    ("10 Purple.mp3", "2023"),
    ("09 Goodnight Kryptonite.mp3", "2023"),
    ("07 She Said Put Your Loving Hand Out.mp3", "2011"),
    ("01 The Speed of Clocks.mp3", "2006"),
    ("05 Summer's Ending Soon My Old Friend.mp3", "2010"),
    ("06 In a Day or Two I Can't Explain.mp3", "2010"),
]

remix_songs = [
    ("07 Disarm [Remix].mp3", "2007"),
    ("04 Spirited.mp3", "2006"),
    ("06 Snakes on a Plane [Remix].mp3", "2006"),
    ("01 Annie Waits [Remix].mp3", "2006"),
    ("05 Everytime You Touch Me [Remix].mp3", "2006"),
    ("03 Beautiful Day [Remix].mp3", "2006"),
    ("02 Not the Same [Remix].mp3", "2006"),
]

original_songs = [
    ("11 Partition.mp3", "2005"),
    ("12 Nyemix.mp3", "2006"),
    ("07 Comeback.mp3", "2005"),
    ("10 Runner.mp3", "2005"),
    ("09 Cloud.mp3", "2005"),
    ("05 Rise.mp3", "2005"),
    ("01 Hypertrax.mp3", "2003"),
    ("13 Makedown.mp3", "2006"),
]

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
<div class="audio-player" id="{anchor_id}">
  <div class="title-download-container">
    <a href="#{anchor_id}" style="text-decoration: none; color: inherit;"><span>{title}</span></a>
    <a href="{download_link}" class="download-link" download="{download_filename}">Download</a>
  </div>
  <audio controls style="width:100%;">
    <source src="{download_link}" type="audio/mpeg">
  </audio>
</div>
""".lstrip()

def extract_title(url):
    filename = os.path.basename(url)
    title, _ = os.path.splitext(filename)
    title = unquote(title)
    title = re.sub(r'^\d+\s*', '', title)
    return title

def generate_audio_players(songs, category):
    audio_players = []
    for filename, year in songs:
        title = extract_title(filename)

        anchor_id = re.sub(r"[\'\[\]]", '', title.replace(' [Remix]', '').replace(' ', '-').lower())
        download_link = f"/downloads/{category}/{filename.replace(' ', '%20').replace('[', '%5B').replace(']', '%5D')}"
        download_filename = f"Jace Browning - {title}.mp3"

        title = f"{title} ({year})"
        if "[Remix]" in title:
            title = title.replace('[Remix]', '').strip()

        audio_players.append(audio_player_template.format(title=title, download_link=download_link, download_filename=download_filename, anchor_id=anchor_id))
    return "\n".join(audio_players)


mashups = generate_audio_players(mashup_songs, "mashups")
remixes = generate_audio_players(remix_songs, "remixes")
originals = generate_audio_players(original_songs, "originals")

script = """
<script>
  function removeExistingHighlights() {
    const highlightedPlayers = document.querySelectorAll(".highlighted");
    highlightedPlayers.forEach(function(player) {
      player.classList.remove("highlighted");
      adjustScrollPosition();
    });
  }

  function highlightAudioPlayer(anchor) {
    removeExistingHighlights();
    const audioPlayer = document.querySelector(anchor);
    if (audioPlayer) {
      audioPlayer.classList.add("highlighted");
      adjustScrollPosition();
    }
  }

  function adjustScrollPosition() {
    const extraSpace = 15;
    if (window.scrollY > 0) {
      window.scrollTo(window.scrollX, window.scrollY - extraSpace);
    }
  }

  document.addEventListener("DOMContentLoaded", function() {
    const anchor = window.location.hash;
    if (anchor) {
      highlightAudioPlayer(anchor);
    }
  });

  window.addEventListener("hashchange", function() {
    const anchor = window.location.hash;
    if (anchor) {
      highlightAudioPlayer(anchor);
    }
  });
</script>
""".lstrip()

music_md_content = music_md_template.format(mashups=mashups, remixes=remixes, originals=originals) + script

with open("music.md", "w") as f:
    f.write(music_md_content)
