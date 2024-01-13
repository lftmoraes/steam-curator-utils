from tkinter import *
from tkinter import ttk
import scraper

class SteamRecommendationScraper:

  def __init__ (self, root):

    self.root = root
    self.root.title("Steam Recommendation Scraper")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, stick=(N, W, E, S))
    self.root.columnconfigure(0, weight=1)
    self.root.rowconfigure(0, weight=1)

    self.instructions = ttk.Label(mainframe, text="Go to the curator page you wish to scrape and complete the url...").grid(column=0, row=0, columnspan=3, sticky=(W, E))

    self.partial_url = ttk.Label(mainframe, text="https://store.steampowered.com/curator/").grid(column=0, row=1, sticky=E)

    self.curator = StringVar()
    self.curator_entry = ttk.Entry(mainframe, width=40, textvariable=self.curator)
    self.curator_entry.grid(column=1, row=1, sticky=W)

    self.scrape_button = ttk.Button(mainframe, text="Scrape", command=self.scrape)
    self.scrape_button.grid(column=2, row=1, sticky=W)

    for child in mainframe.winfo_children():
      child.grid_configure(padx=5, pady=5)
    self.curator_entry.focus()
    self.root.bind("<Return>", self.scrape)


  def scrape(self, *args):

    self.curator_entry.state(["disabled"])
    self.scrape_button.state(["disabled"])
    self.root.update_idletasks()

    try:
      scraper.run(self.curator.get())
    except Exception as ex:
        raise RuntimeError("Something went wrong") from ex

    self.scrape_button.state(["!disabled"])
    self.curator_entry.state(["!disabled"])


root = Tk()
SteamRecommendationScraper(root)
root.mainloop()

