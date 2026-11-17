import tkinter as tk
from database import DatabaseHelper
from windows import AddEntryWindow, ViewListWindow, StatisticsWindow, AboutWindow

class WatchlistTrackerApp:
    def __init__(self, main_window):
        self.window = main_window
        self.window.title("Watchlist Tracker")
        self.window.geometry("650x550")
        self.window.minsize(600, 550) #alt butonların kesilmesini önler   
        #database helperı cagırıp uygulamanın calısaacagı dosyayı belırlıyoruz
        self.db = DatabaseHelper("watchlist.db")

        #renk paletımız ve renk paletimizi seçtiğimiz link:
        #https://datascientyst-com.translate.goog/full-list-named-colors-pandas-python-matplotlib/?_x_tr_sl=en&_x_tr_tl=tr&_x_tr_hl=tr&_x_tr_pto=tc
        self.BG_COLOR = "papayawhip" 
        self.BOX_COLOR = "thistle"       
        self.TITLE_COLOR = "White"     
        self.TEXT_COLOR = "black"      
        self.BTN_ADD_COLOR = "Pink" 
        self.BTN_LIST_COLOR = "Lightcoral" 
        self.BTN_STAT_COLOR = "Salmon"  
        self.BTN_ALT_COLOR = "Plum"
        
        self.window.configure(bg=self.BG_COLOR)

        self.main_frame = tk.Frame(self.window, bg=self.BOX_COLOR, bd=2, relief="groove")
        self.main_frame.pack(padx=40, pady=40, fill="both", expand=True)

        tk.Label(self.main_frame, text="🎬", font=("Arial", 36), bg=self.BOX_COLOR, fg=self.TITLE_COLOR).pack(pady=(15, 0)) 
        tk.Label(self.main_frame, text="Watchlist Tracker", font=("Helvetica", 30, "bold"), bg=self.BOX_COLOR, fg=self.TITLE_COLOR).pack(pady=5)
        tk.Label(self.main_frame, text="Your Personal Cinema Library", font=("Helvetica", 12, "italic"), bg=self.BOX_COLOR, fg=self.TEXT_COLOR).pack(pady=(0, 15)) 

        #butun butonların aynı boyutta ve fontta olması icin ortak
        button_style = {"font": ("Helvetica", 11, "bold"), "height": 2, "bd": 0, "cursor": "hand2", "fg": "white"}

        tk.Button(self.main_frame, text="🆕 Add New Entry", bg=self.BTN_ADD_COLOR, command=self.on_open_add, **button_style).pack(pady=5, padx=40, fill="x", expand=True)
        tk.Button(self.main_frame, text="🔍 View & Manage My List", bg=self.BTN_LIST_COLOR, command=self.on_open_list, **button_style).pack(pady=5, padx=40, fill="x", expand=True)
        tk.Button(self.main_frame, text="📊 My Watch Statistics (Charts)", bg=self.BTN_STAT_COLOR, command=self.on_open_stats, **button_style).pack(pady=5, padx=40, fill="x", expand=True)
        tk.Button(self.main_frame, text="ℹ️ Application Information", bg=self.BTN_ALT_COLOR,command=self.on_open_about, **button_style).pack(pady=5, padx=40, fill="x", expand=True)

        #footer (alt bilgi) kısmı
        footer_frame = tk.Frame(self.window, bg=self.BG_COLOR)
        footer_frame.pack(side="bottom", fill="x", pady=10)
        tk.Label(footer_frame, text="Watchlist Tracker", font=("Arial", 9), bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack()

    #pencereleri cagırırken ortak verıtabanı baglantımızı (self.db) icibe yazdım ki her pencere aynı dbye baglanabilsin
    def on_open_add(self):
        AddEntryWindow(self.window, self.db)

    def on_open_list(self):
        ViewListWindow(self.window, self.db)

    def on_open_stats(self):
        StatisticsWindow(self.window, self.db)

    def on_open_about(self):
        AboutWindow(self.window)

if __name__ == "__main__":
    root = tk.Tk()
    app = WatchlistTrackerApp(root)
    root.mainloop()