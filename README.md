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

Only what Ali supplied on 17 September 2026. Nothing about what the company
sells, where it operates or what it charges, because none of that was given.
When there is a line to add, it goes in `index.html` under `<p class="lede">`.

| | |
|---|---|
| Company | Swift Equipment Ltd. |
| Email | Hussein@swiftequipment.ca |
| Phone | +1 647 455 0532 |
| Address | 482 South Service Road East, Unit 201, Oakville, Ontario L6J 2X6 |

**The unit number is 201.** Same address as Swift Shipping, taken from the
standing instruction that settled it against Corporations Canada and the Cogeco
invoice. If anything ever shows 202 here, that is the error, not this.

## Deploying it

The whole folder is the site. Any static host serves it as it is.

- **Cloudflare Pages.** Connect the repo, no build command, output directory `/`.
- **Netlify.** Same, publish directory `.`.
- **Render.** New, Static Site, build command empty, publish directory `.`.
- **GitHub Pages.** Serve from the branch root.

Each of those picks up `404.html` on its own. The local Python server does not,
so a bad URL looks like a Python error page in development only.

### Pointing the domain

The domain sits on **Hussein's Namecheap account**, so the DNS change needs his
login. As of 17 September 2026 it still resolves to the Namecheap parking page
(`swiftequipment.ca` to 192.64.119.60, `www` to parkingpage.namecheap.com).

In Namecheap, Domain List, Manage, Advanced DNS: delete the two parking records,
then add whatever the host gives you. Usually a CNAME on `www` and either an
ALIAS or an A record on the bare domain. Serve both, and make one redirect to
the other so there is a single address.

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
