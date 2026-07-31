.:: moyunni homepage ::.

a personal site, typeset in the interface of a static privacy wiki i
cloned and liked: black background, monospace, coral accents, hand-built
pages, no build step. the design (style.css) is borrowed wholesale from
that wiki; everything written here is mine. two languages, one toggle,
one jukebox that actually plays.

live wherever github pages points it. the editorial line: under
construction forever, never finished, and i disclaim all responsibility.

what's in the box

  index.html        the menu, the warning, the jukebox, the contacts
  about.html        the entity called moyunni
  projects.html     terminal utils, cli managers, local-first systems
  links.html        the link locker, socials, linkunlocker
  disclaimer.html   i told you so
  archive.html      stories that happened, or didn't
  404.html          the link rotted
  style.css         the whole design (not mine, borrowed, do not edit)
  moyunni.css       the two things the original had no use for: the
                    language toggle and the jukebox, in its palette
  button.svg        an 88x31 webring-style button
  favicon.ico       the tab icon
  pic/              the signature photo
  music/            four tracks for the jukebox

hosting

  this is plain static html and css. it is built to sit on github pages
  with zero config: the .nojekyll file in the root tells pages not to
  run jekyll over the html, and every link is relative so it works both
  at the root of a user site (moyunni.github.io) and inside a project
  path (username.github.io/repo). push to the branch pages serves from,
  wait a minute, done.

  preview locally the same way the wiki does:

    python3 -m http.server 8080

house voice

  everything lowercase, headings and brand names included. no em dashes,
  no en dashes: commas, colons, periods and parentheses cover everything,
  hyphens in compound words are fine. the jukebox and the language toggle
  are the only javascript on the site, and they are the one deliberate
  break from the wiki's no-js rule, because a jukebox with no script is
  just a list of filenames.

copyright 2012-2026, moyunni. no duplication without written
authorization. the design in style.css belongs to the wiki it came from.

.:: eof ::.