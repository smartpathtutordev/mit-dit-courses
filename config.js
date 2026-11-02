/* SmartPath Module Review Portal — configuration
   apiKey: a Google Cloud API key with the Google Drive API enabled.
           Restrict it to the Drive API and to this portal's web address. */
self.PORTAL_CONFIG = {
  apiKey: "",
  apiBase: "https://www.googleapis.com/drive/v3/files",
  title: "SmartPath MATH Module Review",
  subject: "MATH",
  languages: [
    { code: "ENGLISH", label: "English", folderId: "1XeOfF4C-6KkWmkWxdKoJ_0O7KCp6eMbx", enabled: true },
    { code: "TAGALOG", label: "Tagalog", folderId: "1bgfIEq1uHeA3XNpgpKyF4kpOG4Rx7CXW", enabled: false }
  ],
  // Folder names inside each DAY folder
  parts: [
    { name: "MODULE", label: "Module" },
    { name: "ASSESSMENT", label: "Assessment" }
  ],
  // How long (seconds) a folder listing is reused before re-reading Drive
  listTtl: 300
};
