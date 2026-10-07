/**
 * Rocksmith Championship stats site: start the website's quick update when the scoreboard sheet changes.
 *
 * How it works
 *  - Any edit to the sheet marks it as "changed".
 *  - Every 5 minutes a timer checks that mark. If the sheet changed, it asks GitHub to run the
 *    "Quick update (current week)" Action once, so a burst of edits only causes one update.
 *  - The site is usually live 2-3 minutes after the Action starts.
 *  - There is also a menu, "Website → Update website now", for an instant update.
 *
 * Setup (once): see the steps in the README, "Update the site straight from the sheet".
 */

const REPO = 'drandgb/Rocksmith-Championship';
const WORKFLOW = 'quick-update.yml';
const CHECK_EVERY_MINUTES = 5;

// Adds the "Website" menu when the sheet is opened.
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Website')
    .addItem('Update website now', 'updateWebsiteNow')
    .addToUi();
}

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
                                      : 'Could not start the update. Check the GITHUB_TOKEN in Project Settings.',
                                   'Website', 8);
}

// Asks GitHub to run the quick update Action. Returns true if GitHub accepted it.
function startQuickUpdate_() {
  const token = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
  if (!token) { console.error('No GITHUB_TOKEN script property.'); return false; }
  const res = UrlFetchApp.fetch(`https://api.github.com/repos/${REPO}/actions/workflows/${WORKFLOW}/dispatches`, {
    method: 'post',
    contentType: 'application/json',
    headers: { Authorization: 'Bearer ' + token, Accept: 'application/vnd.github+json' },
    payload: JSON.stringify({ ref: 'main' }),
    muteHttpExceptions: true,
  });
  const ok = res.getResponseCode() === 204;
  if (!ok) console.error('GitHub said ' + res.getResponseCode() + ': ' + res.getContentText());
  return ok;
}

// Run this once from the editor to create both triggers (it removes old copies first).
function installTriggers() {
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('markChanged').forSpreadsheet(SpreadsheetApp.getActive()).onChange().create();
  ScriptApp.newTrigger('updateIfChanged').timeBased().everyMinutes(CHECK_EVERY_MINUTES).create();
  markChanged();
}
