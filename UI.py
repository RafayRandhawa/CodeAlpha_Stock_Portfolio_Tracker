import tkinter as tk
from tkinter import ttk
from StockData import Stock, calc_grand_total
from tkinter import messagebox, simpledialog
from News import get_articles
import webbrowser
import requests

CANVAS_WIDTH = 350
CANVAS_HEIGHT = 280
CANVAS_PADX = 10
CANVAS_PADY = 10

DARK_GREY = "#686D76"
ALMOST_BLACK = "#373A40"
ORANGE = "#DC5F00"
OFF_WHITE = "#EEEEEE"

FONT = ("Times New Roman", 18, "normal")


def canvas_color_reset(canvas: tk.Canvas):
    canvas.config(background="white")


class UI:
    def __init__(self, stockData=None):
        if stockData is None:
            stockData = []
        self.limit = 6
        self.num_of_stocks = 0
        self.window = tk.Tk()
        self.window.title("Stock Tracker Portfolio")
        self.window.config(padx=50, pady=50, background=ALMOST_BLACK)
        self.canvasData = stockData
        self.stockData = stockData
        #News Canvas--------------------------------------------------------------------------------------
        self.newsCanvas = tk.Canvas(self.window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT + 320,
                                    background=ALMOST_BLACK, highlightbackground=ORANGE, highlightthickness=6)

        self.newsCanvas.configure(scrollregion=self.newsCanvas.bbox("all"))
        self.newsCanvas.config(highlightthickness=0, bg=DARK_GREY)

        self.newsCanvas.create_rectangle(0, 0, 349, 299, fill=DARK_GREY, width=0)
        self.newsCanvas.grid(row=2, column=3, rowspan=3)
        vbar = tk.Scrollbar(self.window, orient="vertical", command=self.newsCanvas.yview)
        vbar.focus_set()
        vbar.grid(row=2, column=4, rowspan=2, sticky="ns")

        self.newsCanvas.config(yscrollcommand=vbar.set)

        def enter(tag):
            self.newsCanvas.config(cursor="hand2")

        def leave(tag):
            self.newsCanvas.config(cursor="")

        self.newsCanvas.tag_bind('link', '<Enter>', enter)
        self.newsCanvas.tag_bind('link', '<Leave>', leave)

        # Detecting click
        def on_click(event):
            current = event.widget.find_withtag("current")

            clicked_tags = self.newsCanvas.gettags(current)
            for tag in clicked_tags:
                if tag not in ["link", "current"]:
                    webbrowser.open(tag)

        self.newsCanvas.bind('<ButtonPress-1>', on_click)

        #Canvas--------------------------------------------------------------------------------------------
        canvas1 = tk.Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        canvas1.grid(row=2, column=0, padx=CANVAS_PADX, pady=CANVAS_PADY)

        canvas2 = tk.Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        canvas2.grid(row=2, column=1, padx=CANVAS_PADX, pady=CANVAS_PADY)

        canvas3 = tk.Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        canvas3.grid(row=2, column=2, padx=CANVAS_PADX, pady=CANVAS_PADY)

        canvas4 = tk.Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        canvas4.grid(row=4, column=0, padx=CANVAS_PADX, pady=CANVAS_PADY)

        canvas5 = tk.Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        canvas5.grid(row=4, column=1, padx=CANVAS_PADX, pady=CANVAS_PADY)

        canvas6 = tk.Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        canvas6.grid(row=4, column=2, padx=CANVAS_PADX, pady=CANVAS_PADY)

        self.canvas_list = [canvas1, canvas2, canvas3, canvas4, canvas5, canvas6]
        self.canvas_text = []

        for canvas in self.canvas_list:
            canvas.config(highlightthickness=0, bg=DARK_GREY)
            canvas.create_rectangle(1, 1, 349, 279, outline=ORANGE, width=2, fill=DARK_GREY)

        for j in range(0, len(stockData)):
            if self.num_of_stocks < self.limit:
                text = self.canvas_list[j].create_text(175, 140,
                                                       text=f"Name: {stockData[j].name}\n"
                                                            f"Opening: {stockData[j].opening} {stockData[j].currency}\n"
                                                            f"Closing: {stockData[j].previousClosing} {stockData[j].currency}\n"
                                                            f"Low: {stockData[j].low_price} {stockData[j].currency}\n"
                                                            f"High: {stockData[j].high_price} {stockData[j].currency}\n"
                                                            f"Change: {stockData[j].closing_difference_percent}\n"
                                                            f"Shares: {stockData[j].shares}",
                                                       width=320, font=FONT,
                                                       fill=OFF_WHITE)
                self.canvas_text.append(text)
                self.num_of_stocks += 1

        #Labels--------------------------------------------------------------------------------------------
        header = tk.Label(text="Your Stock Portfolio", background=ALMOST_BLACK, foreground=OFF_WHITE,
                          font=("Times New Roman", 20, "italic"))
        header.grid(row=0, column=0, columnspan=3)

        self.grandTotal = tk.Label(text="Your grand total: ", background=ALMOST_BLACK, foreground=OFF_WHITE,
                                   font=("Times New Roman", 15, "bold"))
        self.grandTotal.grid(row=0, column=2)

        label1 = tk.Label(text="", background=ALMOST_BLACK)
        label1.grid(row=1, column=0)

        label2 = tk.Label(text="", background=ALMOST_BLACK)
        label2.grid(row=1, column=1)

        label3 = tk.Label(text="", background=ALMOST_BLACK)
        label3.grid(row=1, column=2)

        label4 = tk.Label(text="", background=ALMOST_BLACK)
        label4.grid(row=3, column=0)

        label5 = tk.Label(text="", background=ALMOST_BLACK)
        label5.grid(row=3, column=1)

        label6 = tk.Label(text="", background=ALMOST_BLACK)
        label6.grid(row=3, column=2)

        self.label_list = [label1, label2, label3, label4, label5, label6]

        for i in range(0, len(stockData)):
            self.label_list[i].config(font=("Times New Roman", 20, "bold"), text=stockData[i].ticker,
                                      foreground=OFF_WHITE)

        #Buttons-------------------------------------------------------------------------------------------

        add_button = ttk.Button(text="Add Stock", command=self.add_stock)
        add_button.grid(row=5, column=0)

        remove_button = ttk.Button(text="Remove Stock", command=self.remove_stock)
        remove_button.grid(row=5, column=1)

        update_button = ttk.Button(text="Update", command=self.update)
        update_button.grid(row=5, column=2)

        get_news_button = ttk.Button(text="Get News", command=self.display_articles)
        get_news_button.grid(row=5, column=3)

        self.window.mainloop()

    def update(self):
        color = ""
        for j in range(0, len(self.stockData)):
            try:
                stock = Stock(self.stockData[j].ticker, self.stockData[j].shares)
                if stock.closing_difference > 0:
                    color = "#9CDBA6"
                elif stock.closing_difference < 0:
                    color = "#C80036"
                else:
                    color = DARK_GREY
                self.stockData[j] = stock
                self.canvas_list[j].itemconfig(self.canvas_text[j],
                                               text=f"Name: {self.stockData[j].name}\n"
                                                    f"Opening: {self.stockData[j].opening} {self.stockData[j].currency}\n"
                                                    f"Closing: {self.stockData[j].previousClosing} {self.stockData[j].currency}\n"
                                                    f"Low: {self.stockData[j].low_price} {self.stockData[j].currency}\n"
                                                    f"High: {self.stockData[j].high_price} {self.stockData[j].currency}\n"
                                                    f"Change: {self.stockData[j].closing_difference_percent}\n"
                                                    f"Shares: {self.stockData[j].shares} ",
                                               width=320, font=FONT)
            except IndexError:
                self.canvas_text.append(self.canvas_list[j].create_text(175, 150,
                                                                        text=f"Name: {self.stockData[j].name}\n"
                                                                             f"Opening: {self.stockData[j].opening} {self.stockData[j].currency}\n"
                                                                             f"Closing: {self.stockData[j].previousClosing} {self.stockData[j].currency}\n"
                                                                             f"Low: {self.stockData[j].low_price} {self.stockData[j].currency}\n"
                                                                             f"High: {self.stockData[j].high_price} {self.stockData[j].currency}\n"
                                                                             f"Change: {self.stockData[j].closing_difference_percent}%\n"
                                                                             f"Shares: {self.stockData[j].shares} ",
                                                                        width=320,
                                                                        font=FONT,
                                                                        fill=OFF_WHITE)
                                        )
            self.canvas_list[j].config(background=color)
            self.window.after(2000, lambda: canvas_color_reset(self.canvas_list[j]))
        for i in range(0, len(self.stockData)):
            self.label_list[i].config(font=("Times New Roman", 20, "bold"), text=self.stockData[i].ticker,
                                      foreground=OFF_WHITE)
            i += 1
        self.grandTotal.config(text=f"Your grand total is: {calc_grand_total(self.stockData)}")

    def add_stock(self):
        ticker = tk.simpledialog.askstring(title="Add Stock", prompt="Please enter a ticker name:", parent=self.window)

        shares = int(
            tk.simpledialog.askstring(title="Add Stock", prompt="How many shares of this stock do you want to add: ",
                                      parent=self.window))

        try:
            if self.num_of_stocks < self.limit:
                self.stockData.append(Stock(ticker, shares))
                self.num_of_stocks += 1
                self.update()
            else:
                tk.messagebox.showinfo(title="Oops",
                                       message="Sorry you've filled up all the slots on your portfolio, remove some to make space")
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
            tk.messagebox.showwarning(title="Sorry",
                                      message="Sorry we can't retrieve the data for that ticker\nCheck your internet connection and the ticker spelling")
        self.grandTotal.config(text=f"Your grand total is: {calc_grand_total(self.stockData)}")

    def remove_stock(self):
        ticker = tk.simpledialog.askstring(title="Remove Stock", prompt="Please enter a ticker name:",
                                           parent=self.window)
        shares = int(tk.simpledialog.askstring(title="Remove Stock",
                                               prompt="How many shares of this stock do you wish to remove: ",
                                               parent=self.window))
        found = False
        for i in range(0, len(self.stockData)):
            if self.stockData[i].ticker == ticker:
                found = True
                if self.stockData[i].shares <= shares:
                    self.stockData.remove(self.stockData.__getitem__(i))
                    self.canvas_list[i].itemconfig(self.canvas_text[i], text="")
                    self.label_list[i].config(text="")
                else:
                    self.stockData[i].shares -= shares
                self.update()
        if not found:
            tk.messagebox.showinfo(title="Sorry", message="No stock by that ticker name in your portfolio")
        self.grandTotal.config(text=f"Your grand total is: {calc_grand_total(self.stockData)}")

    def display_articles(self):
        y = 0
        for stock in self.stockData:
            news_article = get_articles(stock.ticker)

            for news in news_article:
                self.newsCanvas.create_text(170, y + 100, text=news[0], width=CANVAS_WIDTH - 20,
                                            font=("Ariel", 10, "normal"),
                                            fill=OFF_WHITE, tags=["link", news[1]], activefill=ORANGE)
                y += 210
        self.newsCanvas.configure(scrollregion=self.newsCanvas.bbox("all"))
