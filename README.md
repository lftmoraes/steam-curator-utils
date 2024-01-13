
idea for UI:

View 1:
---
Go to curator page you wish to scrape and complete the url...
https://store.steampowered.com/curator/__________    [SCRAPE]
---

View 2:
---
Scraping recommendations for __________
[%%%%..........................................]     100/2000
---

View 3:
---
Scrape complete!
[EXIT]
---

View 4:
---
Scrape failed! Check log file for details.
[EXIT]
---

NOTES:
- total count does not match sum of (recommend, informative, not recommend). probably deleted items?

TODO:
- add better error handling
  - write to log file
  - capture connection errors and retry
- add status bar
- add progress bar to gui (use ttk.ProgressBar widget)
- step-wise operation of scraping function
- add file "save-as" dialog (use tkinter.filedialog.SaveAs)
- pyinstaller bundling for linux
- pyinstaller bundling for windows
- test with different encoding
- how to test???

STRETCH:
- add request for curator info so we can have a picture and name and confirm curator before scraping

