# Publishing the free Ledger demo

Roughly ten minutes, and it costs nothing. This is the single biggest thing you can do
for the listing — TheLittleMachines links a demo like this and sold 167 units in their
first month.

## 1. Make the repo

1. github.com → New repository
2. Name it **ledger-demo**
3. Public. Tick "Add a README".
4. Create.

## 2. Upload these five files

Add file → Upload files → drag in all of:

    index.html      the app, capped at 40 logged spends
    manifest.json   makes it installable on a phone
    sw.js           makes it work with no connection
    icon-192.png    Home Screen icon
    icon-512.png    Home Screen icon

Commit.

## 3. Switch on Pages

Settings → Pages → Source: **Deploy from a branch** → Branch: **main**, folder **/ (root)** → Save.

Wait two or three minutes. Your link will be:

    https://YOURNAME.github.io/ledger-demo/

## 4. Test it before you put it in the listing

- Open it on a laptop. The sample month loads automatically.
- Log 40 spends and check the calm message appears.
- On an iPhone: Safari → Share → Add to Home Screen. Open it from there.
- On Android: Chrome → menu → Add to Home screen.
- Turn on aeroplane mode and open it again. It should still work.

## 5. Put it in the listing

Near the top of the description, not buried:

> **TRY THE FREE DEMO** — no account, nothing to install.
> https://YOURNAME.github.io/ledger-demo/
>
> That is the real app, every screen, no watermark and no time limit. The demo lets you
> log 40 spends, enough to feel how a real week works. After that it says so in one line
> and everything you typed stays readable.
>
> Use it properly before you spend a penny. If you want what you typed in the demo, press
> Back up and the full version opens that file.

## What is different in the demo

Only two things: spends are capped at 40, and it opens on sample data so there is
something to look at. Every screen, every feature, no watermark.

## When you change the app

Re-upload index.html and bump `CACHE = 'ledger-v1'` to `v2` in sw.js, or people with it
installed will keep the old copy.
