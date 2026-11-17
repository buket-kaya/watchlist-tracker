import tkinter as tk
from tkinter import ttk, messagebox as msg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import database as db_module

#tema ayarlari
BOX_COLOR = "bisque"       
TITLE_COLOR = "black"     
TEXT_COLOR = "midnightblue"      
BTN_ADD_COLOR = "pink" 
BTN_LIST_COLOR = "lightcoral" 
BTN_STAT_COLOR = "salmon"



class EntryFormWindow(tk.Toplevel):
    def __init__(self, parent, db, title="Entry Form"):
        super().__init__(parent)
        self.db = db
        self.title(title)
        self.geometry("450x450")
        self.minsize(400, 480) #pencerenin cok kuculup elemanların kaybolmasını engelliyor
        self.configure(bg=BOX_COLOR)
        self.grab_set()#pencere acıkken arkadaki ana pencereye tıklayamayalım

        self.var_title = tk.StringVar()
        self.var_type = tk.StringVar(value="Select Type...")
        self.var_genre = tk.StringVar(value="Select Genre...")
        self.var_status = tk.StringVar(value="Select Status...")
        self.var_rating = tk.StringVar(value="Select Rating...")

        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Content Details", font=("Helvetica", 14, "bold"), bg=BOX_COLOR, fg=TITLE_COLOR).pack(pady=15)

        self.form_frame = tk.Frame(self, bg=BOX_COLOR)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.form_frame.columnconfigure(0, weight=0)
        self.form_frame.columnconfigure(1, weight=1)
        
        #yukaridan asagi esnemeede satırların orantılı acılması icin
        for i in range(5):
            self.form_frame.rowconfigure(i, weight=1)

        lbl_pad = {"padx": (10, 10), "pady": 12, "sticky": "e"}#e east (saga yasladım)
        ent_pad = {"padx": (0, 10), "pady": 12, "sticky": "ew"}#ew iki yana esne

        tk.Label(self.form_frame, text="Title:", bg=BOX_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, **lbl_pad)
        ttk.Entry(self.form_frame, textvariable=self.var_title).grid(row=0, column=1, **ent_pad)

        tk.Label(self.form_frame, text="Type:", bg=BOX_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, **lbl_pad)
        ttk.Combobox(self.form_frame, textvariable=self.var_type, values=["Movie", "TV Series"], state="readonly").grid(row=1, column=1, **ent_pad)

        tk.Label(self.form_frame, text="Genre:", bg=BOX_COLOR, fg=TEXT_COLOR).grid(row=2, column=0, **lbl_pad)
        genres = ["Action", "Comedy", "Drama", "Sci-Fi", "Horror", "Romance", "Documentary", "Animation"]
        ttk.Combobox(self.form_frame, textvariable=self.var_genre, values=genres, state="readonly").grid(row=2, column=1, **ent_pad)

        tk.Label(self.form_frame, text="Watch Status:", bg=BOX_COLOR, fg=TEXT_COLOR).grid(row=3, column=0, **lbl_pad)
        self.combo_status = ttk.Combobox(self.form_frame, textvariable=self.var_status, values=["Watched", "Plan to Watch"], state="readonly")
        self.combo_status.grid(row=3, column=1, **ent_pad)
        
        #Durum değiştiğinde kilitle/aç
        self.combo_status.bind("<<ComboboxSelected>>", self.on_status_change)

        tk.Label(self.form_frame, text="Your Rating (1-10):", bg=BOX_COLOR, fg=TEXT_COLOR).grid(row=4, column=0, **lbl_pad)
        ratings = ["1 ⭐", "2 ⭐", "3 ⭐", "4 ⭐", "5 ⭐", "6 ⭐", "7 ⭐", "8 ⭐", "9 ⭐", "10 ⭐ ⭐"]
        self.combo_rating = ttk.Combobox(self.form_frame, textvariable=self.var_rating, values=ratings, state="readonly")
        self.combo_rating.grid(row=4, column=1, **ent_pad)

    
    def on_status_change(self, event=None):
        if self.var_status.get() == "Plan to Watch":
            self.var_rating.set("No Rating")
            self.combo_rating.configure(state="disabled") #kilitle
        else:
            if self.var_rating.get() == "No Rating":
                self.var_rating.set("Select Rating...")
            self.combo_rating.configure(state="readonly") #ac

#yeni kayıt ekleme
class AddEntryWindow(EntryFormWindow):#base class ın özelliklerini inheritliyor
    def __init__(self, parent, db):
        super().__init__(parent, db, "Add New Entry")

    def build_ui(self):
        super().build_ui()
        btn_frame = tk.Frame(self, bg=BOX_COLOR)
        btn_frame.pack(side="bottom", fill="x", pady=15)
        
        tk.Button(btn_frame, text="Save Entry", bg=BTN_ADD_COLOR, fg="white", font=("Helvetica", 10, "bold"), command=self.on_save, width=15).pack(expand=True)
        
    def on_save(self):
        try:#once verileri validator sınıfına yolluyoruz hata varsa except e gidiyor
            c_title, c_type, c_genre, c_status, c_rating = db_module.WatchlistValidator.validate(
                self.var_title.get(), self.var_type.get(), self.var_genre.get(), self.var_status.get(), self.var_rating.get()
            )
            
            self.db.insert_entry(c_title, c_type, c_genre, c_status, c_rating)
            msg.showinfo("Success", "Record saved successfully!", parent=self)
            self.destroy()#islem bitince pencereyi kapa
        except db_module.ValidationError as e:
            msg.showwarning("Validation Error", str(e), parent=self)

#kayıt duzenleme
class EditWindow(EntryFormWindow):
    def __init__(self, parent, db, item_data):
        super().__init__(parent, db, "Modify Entry")
        self.item_id = item_data[0]

        #tıklanan filmin mevcut verilerini form kutularına doldur
        self.var_title.set(item_data[1])
        self.var_type.set(item_data[2])
        self.var_genre.set(item_data[3])
        self.var_status.set(item_data[4])
        self.var_rating.set(item_data[5])
        
        
        self.on_status_change()

    def build_ui(self):
        super().build_ui()
        btn_frame = tk.Frame(self, bg=BOX_COLOR)
        btn_frame.pack(side="bottom", fill="x", pady=15)
        #duzenleme ekranına ozel guncelle, sil butonları
        tk.Button(btn_frame, text="💾 Update", bg=BTN_LIST_COLOR, fg="white", font=("Helvetica", 10, "bold"), command=self.on_update, width=12).pack(side="left", padx=30, expand=True)
        tk.Button(btn_frame, text="🗑️ Delete", bg="#e74c3c", fg="white", font=("Helvetica", 10, "bold"), command=self.on_delete, width=12).pack(side="right", padx=30, expand=True)

    def on_update(self):
        try:
            c_title, c_type, c_genre, c_status, c_rating = db_module.WatchlistValidator.validate(
                self.var_title.get(), self.var_type.get(), self.var_genre.get(), self.var_status.get(), self.var_rating.get()
            )
            self.db.update_entry(self.item_id, c_title, c_type, c_genre, c_status, c_rating)
            msg.showinfo("Success", "Record updated successfully!", parent=self)
            self.destroy()
        except db_module.ValidationError as e:
            msg.showwarning("Validation Error", str(e), parent=self)

    def on_delete(self):
        #yanlıslıkla silinmesini engellemek icin onay istiyor
        if msg.askyesno("Confirm Delete", "Are you sure you want to delete this record?", parent=self):
            self.db.delete_entry(self.item_id)
            msg.showinfo("Deleted", "Record removed from database.", parent=self)
            self.destroy()

#izleme listesi ve tablo
class ViewListWindow(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.title("My Watchlist")
        self.geometry("780x450")
        self.minsize(650, 400)#pencerenin içindekilerinin kaybolmaması için
        self.configure(bg=BOX_COLOR)
        self.grab_set()

        self.build_ui()
        self.refresh_table()

    def build_ui(self):
        tk.Label(self, text="Your Movie & Series Library", font=("Helvetica", 14, "bold"), bg=BOX_COLOR, fg=TITLE_COLOR).pack(pady=10)

        ctrl_frame = tk.Frame(self, bg=BOX_COLOR)
        ctrl_frame.pack(fill="x", padx=20, pady=5)

        tk.Button(ctrl_frame, text="🔍 Open Filter Tool", bg=BTN_STAT_COLOR, fg="white", font=("Helvetica", 9, "bold"), command=self.on_show_filter).pack(side="left", padx=5)
        
        #klavye ve fare kısayollarını gosteren etiket
        lbl_info = tk.Label(self, text="F1: Statistics | Ctrl+i: Add New | Delete: Remove | Double Click: Edit", bg=BOX_COLOR, fg="gray")
        lbl_info.pack(side="bottom", pady=5)

        #tablo olusturma
        cols = ("ID", "Title", "Type", "Genre", "Status", "Rating")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        for col in cols:
            self.tree.heading(col, text=col)
        
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Title", width=180, anchor="w")
        self.tree.column("Type", width=100, anchor="center")
        self.tree.column("Genre", width=110, anchor="center")
        self.tree.column("Status", width=110, anchor="center")
        self.tree.column("Rating", width=90, anchor="center")
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)

        self.bind("<F1>", self.on_show_statistics)
        self.bind("<Control-i>", self.on_show_add_window)
        self.tree.bind("<Delete>", self.on_item_delete)
        self.tree.bind("<Double-1>", self.on_show_edit_window)

    #tabloyu guncelleme(filtreleme yapıldıgında kullanılıyor)
    def refresh_table(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)#once mevcut tabloyu temizliyor
        records = data if data is not None else self.db.get_all_entries()#veritabanından verileri cekiyor
        for row in records:
            self.tree.insert("", tk.END, iid=row[0], values=row)

    def on_show_add_window(self, event=None):
        add_win = AddEntryWindow(self, self.db)
        self.wait_window(add_win)#yeni pencere kapanana kadar kodu duraklatır
        self.refresh_table()#pencere kapanınca tabloyu yeni verilerle yeniler

    def on_show_edit_window(self, event=None):
        #bosluga cift tıklanırsa kodun cokmesını onlemek icin bolge kontrolu yapıyor
        region = self.tree.identify("region", event.x, event.y) if event else "cell"
        if region != "cell": return

        selected = self.tree.selection()
        if not selected: return #tablodan oge secilmediyse islemi iptal eder
        
        item_data = self.tree.item(selected[0])['values']
        edit_win = EditWindow(self, self.db, item_data)
        self.wait_window(edit_win)
        self.refresh_table()

    def on_item_delete(self, event=None):
        selected = self.tree.selection()
        if not selected: return
        if msg.askyesno("Confirm Delete", "Are you sure you want to delete?", parent=self):
            for iid in selected:
                self.db.delete_entry(iid)
                self.tree.delete(iid) #secili satırı Treeview dan siler

    def on_show_filter(self):
        fw = FilterWindow(self, self.db, self.refresh_table)
        self.wait_window(fw)

    def on_show_statistics(self, event=None):
        StatisticsWindow(self, self.db)

#filtreleme
class FilterWindow(tk.Toplevel):
    def __init__(self, parent, db, refresh_callback):
        super().__init__(parent)
        self.db = db
        #filtreleme işlemi bittikten sonra ana tablonun guncellenmesi icin callback fonksiyonunu saklar
        self.refresh_callback = refresh_callback
        self.title("Filter Library")
        self.geometry("350x220")
        self.configure(bg=BOX_COLOR)
        self.grab_set()

        tk.Label(self, text="Search & Filter Controls", font=("Helvetica", 12, "bold"), bg=BOX_COLOR, fg=TITLE_COLOR).pack(pady=15)
        
        self.filter_combo = ttk.Combobox(self, values=["All", "Watched", "Plan to Watch"], state="readonly", width=30)
        self.filter_combo.set("All")
        self.filter_combo.pack(pady=5, padx=30, fill="x") 

        tk.Button(self, text="Apply Filter", bg=BTN_STAT_COLOR, fg="white", font=("Helvetica", 10, "bold"), command=self.on_apply).pack(pady=20)

#secilen verilere gore db e sql sorgusu atıp ana tabloyu tetikler
    def on_apply(self):
        val = self.filter_combo.get()
        if val == "All":
            self.refresh_callback(self.db.get_all_entries())
        else:
            self.refresh_callback(self.db.get_entries_by_status(val))
        self.destroy()

#analiz ve grafik penceresi(matplotlib)
class StatisticsWindow(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.title("Library Analytics")
        self.geometry("550x500")
        self.configure(bg=BOX_COLOR)
        self.grab_set()

        tk.Label(self, text="Genre Distribution Analysis", font=("Helvetica", 14, "bold"), bg=BOX_COLOR, fg=TITLE_COLOR).pack(pady=15)

        data = db.get_statistics()
        #eger veritabani boşsa programın hata vermemesi için uyarı çıkartıp pencereyi kapatır
        if not data:
            msg.showinfo("No Data", "No data available yet to plot.", parent=self)
            self.destroy()
            return
        #veritabanından gelen listeyi iki farklı diziye (turler ve sayıları) ayrıstırır
        genres = [row[0] for row in data]
        counts = [row[1] for row in data]

        #matplotlib ile yeni bir cizim alanı olusturur ve arka plan rengini temaya uyarlar
        fig, ax = plt.subplots(figsize=(5, 3.5), dpi=100)
        fig.patch.set_facecolor('#2e2e3e')
        ax.set_facecolor('#2e2e3e')

        #çizgi grafigi çizme
        ax.bar(genres, counts, color='#3399FF')
        ax.set_title("Number of Titles per Genre", color='white', fontsize=12, fontweight='bold')
        ax.tick_params(colors='white')
        #cerceve cizgilerini kaldırma
        for spine in ['top', 'right']: ax.spines[spine].set_visible(False)
        for spine in ['bottom', 'left']: ax.spines[spine].set_color('white')
        ax.yaxis.get_major_locator().set_params(integer=True) # y eksenindeki sayıların ondalıklı olmasını engeller

    #çizilen grafigi ayrı pop up olarak acmak yerine tkinter arayuzunun icine gomer
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10, padx=20, fill="both", expand=True)


#hakkında
class AboutWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("About Application")
        self.geometry("400x250")
        self.configure(bg=BOX_COLOR)
        self.grab_set()

        tk.Label(self, text="Watchlist Tracker", font=("Helvetica", 14, "bold"), bg=BOX_COLOR, fg=TITLE_COLOR).pack(pady=20)
        info_text = "Watchlist Tracker\n\nA personal movie and TV series tracking application developed using Python, Tkinter, and SQLite."
        tk.Label(self, text=info_text, font=("Helvetica", 10), bg=BOX_COLOR, fg=TEXT_COLOR, justify="center").pack(pady=10, fill="x", expand=True)
        tk.Button(self, text="Close", bg="#e74c3c", fg="white", command=self.destroy, width=12).pack(pady=15)