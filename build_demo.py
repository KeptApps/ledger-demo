#!/usr/bin/env python3
"""
Rebuilds the hosted demo from whatever Ledger.html currently is.

Run this after any change to the app, then upload index.html and sw.js.
Keeps the two builds from drifting apart, which is how the demo ended up
a version behind.

    python3 build_demo.py [path/to/Ledger.html]

The demo is a showroom: it runs on sessionStorage, so everything a visitor
types is gone when the tab closes and the sample month comes back fresh.
"""
import re, sys, pathlib

APP  = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '../app/Ledger.html')
OUT  = pathlib.Path('index.html')
SW   = pathlib.Path('sw.js')
SHOP = 'https://www.etsy.com/shop/KeptApps'

s = APP.read_text()
n = 0

def rep(a, b):
    global s, n
    if s.count(a) != 1:
        sys.exit(f'PATTERN NOT UNIQUE ({s.count(a)}x): {a[:70]}')
    s = s.replace(a, b); n += 1

# ---------- head ----------
rep('<title>Ledger — your money, in one place</title>',
'''<title>Ledger — live demo</title>
<meta name="description" content="Explore the Ledger budget app with sample data. See what is safe to spend after bills, subscriptions and spending. No account, nothing to install.">
<meta name="theme-color" content="#12756F">
<link rel="manifest" href="manifest.json">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Ledger">''')

# ---------- the banner becomes the demo bar: always up, and it sells ----------
rep('''<div id="sampleBar" class="hide">
  <span><b>These are example numbers.</b> Made up, so click anything you like — nothing here is yours yet.</span>
  <button class="btn ghost sm" id="sampleKeep">Keep exploring</button>
  <button class="btn solid sm" id="sampleMine">Start with my own numbers</button>
</div>''',
'''<div id="sampleBar">
  <span><b>Live demo — these are example numbers.</b> Click anything you like. Your changes
  reset when you close the tab.</span>
  <button class="btn solid sm" id="sampleMine">Start with my own numbers</button>
</div>''')

rep("""$('sampleKeep').onclick = () => { try { localStorage.setItem(SAMPLE,'0'); } catch(e){} sampleBar(); };
$('sampleMine').onclick = startFresh;""",
"""$('sampleMine').onclick = () => demoStop('Starting with your own numbers \\u2014 and keeping them \\u2014 '
  + 'is the full version. Same app, your figures, saved on your own machine.');""")

# the bar is the demo's own furniture, so it never hides
rep("""function sampleBar(){
  let on = false;
  try { on = localStorage.getItem(SAMPLE) === '1'; } catch(e){}
  show('sampleBar', on);
}""",
"""function sampleBar(){ show('sampleBar', true); }""")

# ---------- the demo is a showroom, not a copy you keep ----------
rep("""function write(){
  snapshotWorth();""",
"""const DEMO_CAP = 40;
const demoUsed = () => txns.filter(t => t.demoLogged).length;
function demoStop(what){
  if (confirm(what + '\\n\\nThis is the live demo, so it is a showroom rather than a copy you keep. '
    + 'The full version does all of this and saves everything on your own machine.\\n\\nOpen it now?'))
    window.open('SHOPURL', '_blank');
  return false;
}
function demoRoom(){
  if (demoUsed() < DEMO_CAP) return true;
  return demoStop('The demo stops at ' + DEMO_CAP + ' logged spends \\u2014 enough to feel how a real week works.');
}
function write(){
  snapshotWorth();""".replace('SHOPURL', SHOP))

rep("""function quickLog(amount, cat){
  const amt = Math.abs(Number(amount) || 0);
  if (!amt) return;
  txns.push({ id:uid(), date:today(), desc:(cat||'').trim() || 'Spend',
    amount:-amt, category:(cat||'').trim(), account:'', note:'' });""",
"""function quickLog(amount, cat){
  const amt = Math.abs(Number(amount) || 0);
  if (!amt) return;
  if (!demoRoom()) return;
  txns.push({ id:uid(), date:today(), desc:(cat||'').trim() || 'Spend',
    amount:-amt, category:(cat||'').trim(), account:'', note:'', demoLogged:true });""")

rep("""  if (ex) Object.assign(ex, payload); else txns.push(Object.assign({id:uid()}, payload));
  write(); render(); show('txnVeil', false);""",
"""  if (ex) Object.assign(ex, payload);
  else { if (!demoRoom()) return; txns.push(Object.assign({id:uid(), demoLogged:true}, payload)); }
  write(); render(); show('txnVeil', false);""")

# the four things that are the reason to buy: shown, explained, not run
rep("""$('importBtn').onclick = () => {
  staged=null; say('impMsg',''); show('impPreview',false); show('impGo',false); show('impVeil');
};""",
"""$('importBtn').onclick = () => demoStop('Bank CSV import reads your real statement and sorts every '
  + 'transaction into a category for you. It is the fastest way to fill Ledger in, and it is in the '
  + 'full version.');""")

rep("""$('backupBtn').onclick = () => {
  download('ledger-backup-'+today()+'.json',""",
"""$('backupBtn').onclick = () => demoStop('Backup keeps a copy of everything you have entered, and it '
  + 'is how you move Ledger to another computer.');
function unusedBackup(){
  download('ledger-backup-'+today()+'.json',""")

rep("$('restoreBtn').onclick = () => $('restoreFile').click();",
    "$('restoreBtn').onclick = () => demoStop('Restore brings a backup file back into Ledger.');")

rep("""$('exportBtn').onclick = () => {
  const q = v => '"'+String(v==null?'':v).replace(/"/g,'""')+'"';""",
"""$('exportBtn').onclick = () => demoStop('Export gives you a clean CSV of every transaction, so your '
  + 'figures are never locked in.');
function unusedExport(){
  const q = v => '"'+String(v==null?'':v).replace(/"/g,'""')+'"';""")

rep("""  $('wipeBtn').onclick = () => {
    if (!confirm('Erase every transaction, bill, subscription, goal, debt and account? This cannot be undone.')) return;
    if (!confirm('Really sure? Press Back up first if you have not.')) return;
    txns=[];bills=[];subs=[];goals=[];debts=[];accts=[];budgets={};worthLog=[];alloc=[];
    incomes=[]; buffer=0;
    write(); render(); toast('Everything erased');
  };""",
"""  $('wipeBtn').onclick = () => {
    if (!confirm('Reset the demo back to its sample figures?')) return;
    localStorage.removeItem('ledger.demoseeded');
    txns=[];bills=[];subs=[];goals=[];debts=[];accts=[];budgets={};worthLog=[];alloc=[];
    incomes=[]; buffer=0;
    loadSample(); toast('Demo reset');
  };""")

# ---------- boot: service worker, and open on the sample month ----------
rep("""if (CAN_STORE){
  readAll(); applyTheme(); write(); setTab('home'); sampleBar();""",
"""if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(()=>{}));
}
if (CAN_STORE){
  readAll(); applyTheme();
  if (!txns.length && !localStorage.getItem('ledger.demoseeded')){
    localStorage.setItem('ledger.demoseeded','1');
    loadSample();
  }
  write(); setTab('home'); sampleBar();""")

rep("""  if (!txns.length && !localStorage.getItem('ledger.seen')){
    localStorage.setItem('ledger.seen','1'); show('helpVeil');
  }
  if (!txns.length) $('sampleBtn').classList.add('solid');""",
"""  $('sampleBtn').textContent = 'Reset the demo';""")

# ---------- nothing survives the tab ----------
# Every store in the app becomes sessionStorage, so the banner's promise is true:
# close the tab and the sample month comes back untouched.
swaps = s.count('localStorage')
s = s.replace('localStorage', 'sessionStorage')
n += 1

OUT.write_text(s)

# bump the cache so installed copies pick up the new build
sw = SW.read_text()
v = int(re.search(r"ledger-v(\d+)", sw).group(1))
SW.write_text(re.sub(r"ledger-v\d+", f"ledger-v{v+1}", sw))

print(f"demo rebuilt from {APP} — {n} patches ({swaps} stores moved to sessionStorage), "
      f"service worker now ledger-v{v+1}")
print("upload index.html and sw.js to the repo")
