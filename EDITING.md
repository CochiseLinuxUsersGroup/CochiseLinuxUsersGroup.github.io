# How to Update the CLUG Website

*Plain-English guide for volunteers. No programming needed — if you can edit a document, you can do this.*

---

## The one thing to understand

The website is built from a set of files stored on GitHub (a website that holds files for projects). When you change one of those files and save it, the live website rebuilds itself automatically — usually within a minute or two.

That's the whole system:

> **Find the file → change it → save. The website updates itself.**

You cannot break the website by editing text. Every save is recorded and can be undone (see [Made a mistake?](#made-a-mistake) below).

---

## Editing a file in your web browser (the normal way)

You don't need to install anything. Everything happens on the GitHub website.

1. Go to **github.com/CochiseLinuxUsersGroup/CochiseLinuxUsersGroup.github.io** and sign in.
2. You'll see a list of folders and files. Click through the folders to find the file you want (there's a map in the [File map](#file-map--where-everything-lives) section below).
3. Click the file's name to open it.
4. Click the **pencil icon** (✏️) in the top-right corner, above the file. Now you're editing.
5. Make your changes.
6. Scroll down to the bottom of the page. Click the green **Commit changes…** button.
7. A small window pops up. You can type a short note like "updated RAM count" (or leave it blank), then click the green **Commit changes** button again.
8. Done. Wait a minute or two, then visit **cochiselinuxusergroup.org** to see your change live.

> **"Commit" just means "save."** GitHub records who changed what and when, so nothing is ever truly lost.

---

## Common tasks, step by step

### Update an inventory number

Example: the 2GB laptop RAM sticks went from ×25 to ×24.

1. On the GitHub page, click the **_includes** folder, then the **inventory** folder.
2. Click the file for that section. RAM lives in **storage.html**. (See the file map below for the full list.)
3. Click the pencil icon (✏️).
4. Press **Ctrl+F** on your keyboard (hold Ctrl and tap F). A little search box appears — type what you're looking for, e.g. `Laptop RAM`.
5. Find the pill with the number, e.g. `2GB <strong>×25</strong>`, and change **only the number** after the × — so ×25 becomes ×24.
6. Scroll down, click **Commit changes…**, then **Commit changes** again. Done.

### Add a computer to the inventory

1. Open **_includes/inventory/computers.html** and click the pencil icon.
2. Find the **Laptop Computers** or **Desktop Computers** heading.
3. Copy one whole block starting with `<div class="computer-card">` and ending with `</div>`. Paste it right after the last block in that section.
4. Change the model name and the specs (hard drive, RAM, processor, OS) inside your pasted block. Don't touch anything else.
5. Commit your change.

### Update one of the detailed lists (chargers, monitor cables, USB cables)

1. Open **_includes/inventory/** and pick the detail file: **charger-detail.html**, **monitor-detail.html**, or **usbcables-detail.html**.
2. Click the pencil icon. Each line is one item, e.g. `Dell (output 19.5 volts 3.34 amps) (4 each)`.
3. Change the number in `(X each)`. To add an item, copy a line and change it. To remove one, delete the line.
4. Commit your change.

### Add a new category to the inventory page

1. In the **_includes/inventory** folder, click **Add file → Create new file** (top-right).
2. Name the file something short ending in `.html`, e.g. `audio.html`.
3. Give it a heading and your items, copying the style of the other files:
   ```html
   <h2 id="audio">Audio Gear</h2>
   ```
4. Open **inventory/index.html**, click the pencil, and find the five lines that pull in the sections (each one names a section file). Copy one of those lines, paste it below the others, and change the filename to your new file (e.g. `audio.html`).
5. In the same file, find the navigation area near the top (marked `ANCHOR NAV`) and add a jump link for your new section.
6. Commit.

### Update the install count on the homepage

The homepage shows stats like "425 installs completed." To update the number:

1. Open **index.html** (in the main folder list — not the one inside the inventory folder) and click the pencil icon.
2. Press **Ctrl+F** and type `installs completed`.
3. You'll find a line like `<li><strong>425</strong> installs completed</li>` — change **only the number** between `<strong>` and `</strong>`.
4. The "computers donated" number appears **twice** — once in the paragraph above the stats and once in the stats list itself. Update both so they match.
5. Commit your change.

### Keep the "Upcoming Events" list up to date

The events shown on the homepage come from a simple list — you never edit the homepage itself for this.

1. Open the **_data** folder, then **events.yml**, and click the pencil icon.
2. Each event is a short block like this:
   ```
   - date: 2026-10-08
     time: "18:00:00-07:00"
     time_display: "6pm"
     display: "Oct 08"
     title: "Ubuntu Hour"
     location: "Carl's Jr."
   ```
3. **Remove events that already happened:** delete the whole block (all 6 lines) for any date in the past.
4. **Add the next upcoming event:** copy a whole block, paste it at the bottom, and change the `date` (year-month-day), `display` (like "Dec 10"), `time_display` ("6pm"), and `title`. Keep the blocks in date order, earliest at the top.
5. **Spacing matters — getting this wrong once broke the website.** Each new event's first line must start with `- date:` at the very beginning of the line, with no spaces in front of the dash. The five lines under it each start with exactly two spaces. Line up your dashes with the other events' dashes.
6. **Make the two times agree:** `time` is the technical 24-hour time and `time_display` is what visitors see — `17:00` means 5pm, `18:00` means 6pm. If they disagree, the page shows the wrong time.
7. Commit. The homepage updates itself — no HTML needed.

### Post meeting notes or a blog post

1. Open the **_posts** folder and click **Add file → Create new file**.
2. Name the file like this: `2026-10-15-ubuntu-hour.md` — that's year-month-day, then a short dash-separated title, ending in `.md`. Use today's date.
3. At the very top of the file, paste this block exactly (changing the title and date):
   ```
   ---
   layout: post
   title: "Your Title Here"
   date: 2026-10-15
   categories: meeting
   ---
   ```
4. Write your post below that block. Leave a blank line between paragraphs. Put `**` around words you want **bold**.
5. Commit. The post appears on the blog page automatically.

### Change the top navigation menu

1. Open **_includes/header.html** and click the pencil icon.
2. Find the link you want to change. Each one looks like `<a href="/events">Events</a>` — change the word between the `>` and `<`, or change the address inside the quotes to point somewhere else.
3. Commit. (There's a longer EDIT GUIDE comment at the top of that file if you want more detail.)

### Change the site title or description (what Google shows)

1. Open **_config.yml** and click the pencil icon. There's an EDIT GUIDE comment at the top explaining each setting in plain words.
2. Change the `title:` or `description:` lines. Keep them short.
3. Commit. **Don't** change `url`, `baseurl`, or `lang` unless you know what they do.

---

## File map — where everything lives

| I want to change… | Open this file |
|---|---|
| Inventory: computers (laptops & desktops) | `_includes/inventory/computers.html` |
| Inventory: hard drives, RAM, WiFi chips, adapters | `_includes/inventory/storage.html` |
| Inventory: keyboards, mice | `_includes/inventory/peripherals.html` |
| Inventory: monitor/power/USB/ethernet cables | `_includes/inventory/cables.html` |
| Inventory: routers, switches | `_includes/inventory/networking.html` |
| Inventory: full charger list | `_includes/inventory/charger-detail.html` |
| Inventory: full monitor cable list | `_includes/inventory/monitor-detail.html` |
| Inventory: full USB cable list | `_includes/inventory/usbcables-detail.html` |
| Inventory page title, jump links, "last updated" date | `inventory/index.html` |
| Homepage: install count & donated-computers stats | `index.html` (About Us section) |
| Homepage: Upcoming Events list (keep dates in the future) | `_data/events.yml` |
| Top navigation menu | `_includes/header.html` |
| Bottom of every page (footer) | `_includes/footer.html` |
| Blog and meeting posts | `_posts/` — one file per post |
| Site title, description, social links | `_config.yml` |
| Homepage | `index.html` |

> **About the inventory folder:** the files `inventory/index.html`, `inventory/charger.md`, `inventory/monitor.md`, and `inventory/usbcables.md` are mostly skeletons — the real content lives in `_includes/inventory/`. If you open a file and it looks almost empty except for one odd-looking line, that's a *placeholder*: it pulls in the contents of another file (you'll see that file's name in the line). Go edit the named file instead.

---

## Words you'll see

- **Repository (repo)** — a collection of files stored on GitHub. This website is one repository.
- **Commit** — saving your change. GitHub records every commit with your name, and any commit can be undone.
- **Push** — sending your saved change to GitHub. When you click "Commit changes" on the website, this happens automatically — you don't do anything extra.
- **Jekyll** — the program that turns these files into the website. You never deal with it directly.
- **Include** — a placeholder line that pulls in another file's contents (the other file's name appears in the line). Always edit the named file, not the placeholder.
- **Front matter** — the settings block at the top of a file, between two lines that each say `---`. It holds things like the page title. You usually don't need to touch it.
- **Markdown** — a simple way to format text: a blank line starts a new paragraph, `**words**` makes **bold**, `#` at the start of a line makes a big heading.

---

## Made a mistake?

Nothing is lost — every change is saved in the file's history.

1. Open the file on GitHub.
2. Click **History** near the top-right of the file view.
3. You'll see a list of every change. Click one to see exactly what was different.
4. If you need to undo it, ask on the mailing list or ask Devi — it takes about a minute.

---

## For advanced users (command line)

```bash
git clone https://github.com/CochiseLinuxUsersGroup/CochiseLinuxUsersGroup.github.io.git
# edit files...
git add -A && git commit -m "describe what changed" && git push
```

Push to `master` and GitHub Pages rebuilds the site automatically.

---

*Questions? Ask on the mailing list or on GitHub. This guide lives at `EDITING.md` in the repository root — if something in it is wrong or confusing, please fix it the same way you'd fix anything else.*
