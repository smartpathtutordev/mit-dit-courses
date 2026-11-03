/* SmartPath Module Review Portal — configuration
   apiKey: a Google Cloud API key with the Google Drive API enabled.
           Restrict it to the Drive API and to this portal's web address. */
self.PORTAL_CONFIG = {
  apiKey: "",
  apiBase: "https://www.googleapis.com/drive/v3/files",
  title: "SmartPath Module Review",
  subjects: [
    { code: "MATH", label: "Math" },
    { code: "ENGLISH", label: "English" }
  ],
  // One entry per Drive folder. Each folder holds GRADE n / QUARTER n / WEEK n / DAY n / <part>/index.html
  languages: [
    { code: "MATH-ENG", label: "English", folderId: "1XeOfF4C-6KkWmkWxdKoJ_0O7KCp6eMbx", subject: "MATH", enabled: true },
    { code: "MATH-TAG", label: "Tagalog", folderId: "1bgfIEq1uHeA3XNpgpKyF4kpOG4Rx7CXW", subject: "MATH", enabled: true },
    { code: "ENGLISH", label: "English", folderId: "1Hq_D4gfTTUrvrSniQ-zH9U576eogUzSC", subject: "ENGLISH", enabled: true, parts: [ { name: "FULL MODULE", label: "Module" }, { name: "ASSESSMENT", label: "Assessment" } ] }
  ],
  // Default folder names inside each DAY folder
  parts: [
    { name: "MODULE", label: "Module" },
    { name: "ASSESSMENT", label: "Assessment" }
  ],
  // How long (seconds) a folder listing is reused before re-reading Drive
  listTtl: 300
};
