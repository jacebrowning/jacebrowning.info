import os
import re
from urllib.parse import unquote

mashup_links = """
https://www.dropbox.com/s/8sxv5hv29jibzkn/04%20Time%20In%20My%20Head.mp3?dl=0
https://www.dropbox.com/s/bmaz7s355zgj7di/02%20Your%20Mom.mp3?dl=0
https://www.dropbox.com/s/d3i8x66tn44q6qo/Billie%27s%20Back.mp3?dl=0
https://www.dropbox.com/s/9t6ho7ksab5q5hj/03%20Never%20Watching.mp3?dl=0
https://www.dropbox.com/s/phm9xqnf3p3j5zu/Goodnight%20Kryptonite.mp3?dl=0
https://www.dropbox.com/s/264dxi260kjv7xd/01%20The%20Speed%20of%20Clocks.mp3?dl=0
https://www.dropbox.com/s/ox59wg6333i0ea1/07%20She%20Said%20Put%20Your%20Loving%20Hand%20Out.mp3?dl=0
https://www.dropbox.com/s/kp32d9l8c38u1a0/05%20Summer%27s%20Ending%20Soon%20My%20Old%20Friend.mp3?dl=0
https://www.dropbox.com/s/xk28vvwjgbdioff/06%20In%20a%20Day%20or%20Two%20I%20Can%27t%20Explain.mp3?dl=0
""".strip().splitlines()

remix_links = """
https://www.dropbox.com/s/rototplfeuclcic/07%20Disarm%20%5BRemix%5D.mp3?dl=0
https://www.dropbox.com/s/fflbvvs4hvkvsi1/03%20Beautiful%20Day%20%5BRemix%5D.mp3?dl=0
https://www.dropbox.com/s/90omy1lj4gahj4f/04%20Spirited.mp3?dl=0
https://www.dropbox.com/s/3hmathh09awmath/01%20Annie%20Waits%20%5BRemix%5D.mp3?dl=0
https://www.dropbox.com/s/hw0hjx14imlxhum/06%20Snakes%20on%20a%20Plane%20%5BRemix%5D.mp3?dl=0
https://www.dropbox.com/s/tekppvfags3eu8n/05%20Everytime%20You%20Touch%20Me%20%5BRemix%5D.mp3?dl=0
https://www.dropbox.com/s/x6ogus8815qqx19/02%20Not%20the%20Same%20%5BRemix%5D.mp3?dl=0
""".strip().splitlines()

original_links = """
https://www.dropbox.com/s/a3epf05uubl6w87/11%20Partition.mp3?dl=0
https://www.dropbox.com/s/061imz0n7swqxp1/12%20Nyemix.mp3?dl=0w
https://www.dropbox.com/s/tum5ambc1uhcsqc/07%20Comeback.mp3?dl=0
https://www.dropbox.com/s/nvp52sq0lmur3el/05%20Rise.mp3?dl=0
https://www.dropbox.com/s/9nequ6x8v769zd0/09%20Cloud.mp3?dl=0
https://www.dropbox.com/s/pt74wcg98ci02jy/01%20Hypertrax.mp3?dl=0
https://www.dropbox.com/s/3z5isd90twgj0pm/10%20Runner.mp3?dl=0
https://www.dropbox.com/s/snezt8boh0h0b90/04%20Paraphaze.mp3?dl=0
https://www.dropbox.com/s/vawrmc0qulofaav/13%20Makedown.mp3?dl=0
https://www.dropbox.com/s/rem8vmypvkjzvjt/14%20Green.mp3?dl=0
https://www.dropbox.com/s/09e0t74bim0y9bc/15%20A%20Way.mp3?dl=0
""".strip().splitlines()

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
    <a href="{download_link}" class="download-link">Download</a>
  </div>
  <audio controls style="width:100%;">
    <source src="{download_link}" type="audio/mpeg">
  </audio>
</div>
"""

def extract_title(url):
    filename = os.path.basename(url)
    title = os.path.splitext(filename)[0]
    title = unquote(title)
    title = re.sub(r'^\d+\s*', '', title)
    title = re.sub(r'\s*\[Remix\]', '', title, flags=re.IGNORECASE)
    return title

def convert_dl_0_to_dl_1(url):
    return url.replace('?dl=0', '?dl=1')

def generate_audio_players(links):
    audio_players = []
    for link in links:
        title = extract_title(link)
        download_link = convert_dl_0_to_dl_1(link)
        audio_players.append(audio_player_template.format(title=title, download_link=download_link))
    return "\n".join(audio_players)

mashups = generate_audio_players(mashup_links)
remixes = generate_audio_players(remix_links)
originals = generate_audio_players(original_links)

music_md_content = music_md_template.format(mashups=mashups, remixes=remixes, originals=originals)

with open("music.md", "w") as f:
    f.write(music_md_content)
