# swiftequipment.ca

Holding page for **Swift Equipment Ltd.** One page that says the site is coming,
carries the logo, and gives people a way to make contact.

Plain HTML and CSS. No build step, no framework, no package manager.

## Run it locally

```bash
python -m http.server 8127
```

Then open `http://localhost:8127`.

## What is on the page

The company name, the contact details and the address. Nothing about what the
company sells, where it operates or what it charges. When there is a line to add,
it goes in `index.html` under `<p class="lede">`.

| | |
|---|---|
| Company | Swift Equipment Ltd. |
| Contact | an enquiry form, posting to FormSubmit |
| Address | 482 South Service Road East, Unit 202, Oakville, Ontario L6J 2X6 |

No email address or phone number is published on the site, by request. The form
in `index.html` posts to FormSubmit, which relays to the mailbox, and sends the
visitor to `thanks.html` afterwards. A hidden `_honey` field traps bots.

The unit number is **201**. If anything here ever shows 202, that is the error.

## Deploying it

The whole folder is the site. Any static host serves it as it is.

- **Cloudflare Pages.** Connect the repo, no build command, output directory `/`.
- **Netlify.** Same, publish directory `.`.
- **Render.** New, Static Site, build command empty, publish directory `.`.
- **GitHub Pages.** Serve from the branch root.

Each of those picks up `404.html` on its own. The local Python server does not,
so a bad URL looks like a Python error page in development only.

### Pointing the domain

DNS is managed at Namecheap. In Domain List, Manage, Advanced DNS: delete the
two parking records, then add the four GitHub Pages A records on the bare domain
and a CNAME on `www` pointing at `themrmana.github.io`. Set the custom domain in
the repo's Pages settings once those resolve.

`index.html` and `sitemap.xml` currently name **`https://www.swiftequipment.ca/`**
as the canonical address. If you decide the bare domain is the real one, change
it in both files.

## Regenerating the logo assets

`assets/img/Swift_Equipment_Ltd_Logo.pdf` is the original supplied artwork and is
the source for everything else in that folder. It is vector, so the script only
crops and recolours it, never redraws it.

```bash
python tools/make_logo_assets.py
```

That writes `logo.svg`, `logo-white.svg`, `logo-inline.svg`, `favicon.svg`,
`icon-180.png`, `icon-512.png` and `og.png`. The two full colour SVGs are also
worth keeping for an email signature or a letterhead.

## Layout

```
index.html              The holding page
404.html                Not found, same design
robots.txt              Indexing allowed
sitemap.xml             One URL
assets/css/site.css     All of the styling
assets/img/             Logo, icons, social card, original PDF
tools/make_logo_assets.py
```
