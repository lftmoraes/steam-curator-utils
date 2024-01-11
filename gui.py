from tkinter import *
from tkinter import ttk
import scraper

class SteamRecommendationScraper:

  def __init__ (self, root):

    root.title("Steam Recommendation Scraper")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, stick=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # instructions
    ttk.Label(mainframe, text="Go to the curator page you wish to scrape and complete the url...").grid(column=0, row=0, columnspan=3, sticky=(W, E))

    # partial url
    ttk.Label(mainframe, text="https://store.steampowered.com/curator/").grid(column=0, row=1, sticky=E)

    # curator entry
    self.curator = StringVar()
    self.curator_entry = ttk.Entry(mainframe, width=40, textvariable=self.curator)
    self.curator_entry.grid(column=1, row=1, sticky=W)

    # scrape button
    self.button = ttk.Button(mainframe, text="Scrape", command=self.scrape)
    self.button.grid(column=2, row=1, sticky=W)

    for child in mainframe.winfo_children():
      child.grid_configure(padx=5, pady=5)
    self.curator_entry.focus()
    root.bind("<Return>", self.scrape)


  def scrape(self, *args):

    self.curator_entry.state(["disabled"])
    self.button.state(["disabled"])

    try:
      scraper.run(self.curator.get())
    except Exception as ex:
        raise RuntimeError("Something went wrong") from ex

    self.button.state(["!disabled"])
    self.curator_entry.state(["!disabled"])


root = Tk()
SteamRecommendationScraper(root)
root.mainloop()

