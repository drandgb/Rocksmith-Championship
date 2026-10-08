/**
 * Rocksmith Championship stats site: start the website's quick update when the scoreboard sheet changes.
 *
 * How it works
 *  - Any edit to the sheet marks it as "changed".
 *  - Every 5 minutes a timer checks that mark. If the sheet changed, it asks GitHub to run the
 *    "Quick update (current week)" Action once, so a burst of edits only causes one update.
 *  - The site is usually live 2-3 minutes after the Action starts.
 *  - "Update website now (drand)" and "Full rescan (drand)" live in the sheet's Rocksmith CS menu (see below).
 *
 * Setup (once): see the steps in the README, "Update the site straight from the sheet".
 */

const REPO = 'drandgb/Rocksmith-Championship';
const WORKFLOW = 'quick-update.yml';
const CHECK_EVERY_MINUTES = 5;
let LAST_ERROR = '';
function tryMessage_(s) { try { return JSON.parse(s).message; } catch (e) { return s.slice(0, 120); } }
const TOKEN_PROPERTY = 'drandWebsiteToken';   // name of the script property that holds the GitHub token

// Menu items: add these two lines to the sheet's existing menu (the "Rocksmith CS" menu in its onOpen), before .addToUi():
//   .addItem('Update website now (drand)', 'updateWebsiteNow')
//   .addItem('Full rescan (drand)', 'fullRescanNow')

// Installable trigger "On change": remember that the sheet changed.
function markChanged() {
  PropertiesService.getScriptProperties().setProperty('CHANGED', String(Date.now()));
}

// Time-driven trigger: if the sheet changed since the last update, start one.
function updateIfChanged() {
  const props = PropertiesService.getScriptProperties();
  if (!props.getProperty('CHANGED')) return;
  if (startQuickUpdate_()) props.deleteProperty('CHANGED');
}

// Menu item.
function updateWebsiteNow() {
  const ok = startQuickUpdate_();
  PropertiesService.getScriptProperties().deleteProperty('CHANGED');
  SpreadsheetApp.getActive().toast(ok ? 'Website update started. It should be live in about 2-3 minutes.'
                                      : 'Could not start the update (' + LAST_ERROR + ').',
                                   'Website', 8);
}

// Menu item: re-read every week tab (use after correcting an older week). Takes a few minutes.
function fullRescanNow() {
  const ok = startWorkflow_('full-rescan.yml');
  SpreadsheetApp.getActive().toast(ok ? 'Full rescan started. It should be live in about 5 minutes.'
                                      : 'Could not start the rescan (' + LAST_ERROR + ').',
                                   'Website', 8);
}

// Asks GitHub to run the quick update Action. Returns true if GitHub accepted it.
function startQuickUpdate_() { return startWorkflow_(WORKFLOW); }

// Asks GitHub to run one of the site's Actions. Returns true if GitHub accepted it.
function startWorkflow_(workflow) {
  const token = PropertiesService.getScriptProperties().getProperty(TOKEN_PROPERTY);
  if (!token) { LAST_ERROR = 'no script property named ' + TOKEN_PROPERTY; console.error(LAST_ERROR); return false; }
  const res = UrlFetchApp.fetch(`https://api.github.com/repos/${REPO}/actions/workflows/${workflow}/dispatches`, {
    method: 'post',
    contentType: 'application/json',
    headers: { Authorization: 'Bearer ' + token, Accept: 'application/vnd.github+json' },
    payload: JSON.stringify({ ref: 'main' }),
    muteHttpExceptions: true,
  });
  const ok = res.getResponseCode() === 204;
  if (!ok) { LAST_ERROR = 'GitHub said ' + res.getResponseCode() + ': ' + (tryMessage_(res.getContentText()) || 'no details');
             console.error(LAST_ERROR); }
  return ok;
}

// Another way to save the token: run this from the editor, then switch to the sheet's browser tab and paste
// the token into the box that pops up there. It saves it as the script property and checks it with GitHub.
function setWebsiteToken() {
  const ui = SpreadsheetApp.getUi();
  const r = ui.prompt('Website token', 'Paste the GitHub token (it starts with github_pat_):', ui.ButtonSet.OK_CANCEL);
  if (r.getSelectedButton() !== ui.Button.OK) return;
  const token = r.getResponseText().trim();
  if (!token) { ui.alert('No token entered.'); return; }
  PropertiesService.getScriptProperties().setProperty(TOKEN_PROPERTY, token);
  const res = UrlFetchApp.fetch(`https://api.github.com/repos/${REPO}/actions/workflows/${WORKFLOW}`, {
    headers: { Authorization: 'Bearer ' + token, Accept: 'application/vnd.github+json' }, muteHttpExceptions: true });
  ui.alert(res.getResponseCode() === 200 ? 'Token saved, and GitHub accepted it.'
           : 'Token saved, but GitHub said ' + res.getResponseCode() + ': ' + (tryMessage_(res.getContentText()) || 'no details'));
}

// Run this once from the editor to create the triggers (it removes old copies of its own triggers first).
function installTriggers() {
  // only remove this script's own triggers, never the sheet's other ones
  const mine = ['markChanged', 'updateIfChanged', 'addWebsiteMenu'];
  ScriptApp.getProjectTriggers().filter(t => mine.includes(t.getHandlerFunction())).forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('markChanged').forSpreadsheet(SpreadsheetApp.getActive()).onChange().create();
  ScriptApp.newTrigger('updateIfChanged').timeBased().everyMinutes(CHECK_EVERY_MINUTES).create();
  markChanged();
}
