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

- Open it on a laptop. The sample month loads automatically and the demo bar sits on top.
- Change a bill, then close the tab and open the link again. The sample month should be back.
- Log 40 spends and check the calm message appears.
- Press Start with my own numbers, Import, Back up and Export. Each should offer the shop.
- On an iPhone: Safari → Share → Add to Home Screen. Open it from there.
- On Android: Chrome → menu → Add to Home screen.
- Turn on aeroplane mode and open it again. It should still work.

## 5. Put it in the listing

Near the top of the description, not buried:

> **TRY THE FREE DEMO** — no account, nothing to install.
> https://YOURNAME.github.io/ledger-demo/
>
> That is the real app with sample figures already in it, every screen, no watermark and
> no time limit. Click through it properly before you spend a penny. It is a showroom, so
> what you type there is gone when you close the tab. Saving, backup and bank import are
> in the full version.

## What is different in the demo

- It opens on the sample month, so there is something to look at.
- It runs on sessionStorage, so nothing survives the tab. Close it and the sample month
  comes back untouched.
- Logged spends are capped at 40.
- CSV import, backup, restore, export and Start with my own numbers offer the shop instead
  of running.

Every screen is there, and there is no watermark.

## When you change the app

Run `python3 build_demo.py` against your Ledger.html. It rebuilds index.html and bumps the
service worker version for you, so people with the demo installed pick up the new copy.
Then upload index.html and sw.js.
