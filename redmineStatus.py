import json
import os
from redminelib import Redmine
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, Entry, StringVar, messagebox

# Config dosyası yolu
CONFIG_FILE = "config.json"

# Config dosyasını yükleme veya oluşturma
def load_or_create_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"url": "", "api_key": ""}, f)
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

# Config dosyasını güncelleme
def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

# Redmine verilerini getirme ve görselleştirme
def fetch_and_plot_data(url, api_key):
    try:
        redmine = Redmine(url, key=api_key)
        issues = redmine.issue.all()

        statuses = {}
        trackers = {}

        for issue in issues:
            status_name = issue.status.name
            statuses[status_name] = statuses.get(status_name, 0) + 1

            tracker_name = issue.tracker.name
            trackers[tracker_name] = trackers.get(tracker_name, 0) + 1

        # Grafik çizme
        fig, axs = plt.subplots(1, 2, figsize=(12, 6))
        axs[0].pie(statuses.values(), labels=statuses.keys(), autopct='%1.1f%%', startangle=140)
        axs[0].set_title("Issue Status Distribution")
        axs[1].bar(trackers.keys(), trackers.values(), color='skyblue')
        axs[1].set_title("Issue Tracker Distribution")
        axs[1].set_ylabel("Count")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Data fetch failed: {e}")

# Giriş ekranı
def login_screen(config):
    def save_and_continue():
        url = url_var.get()
        api_key = api_key_var.get()

        # Eksik bilgi kontrolü
        if not url or not api_key:
            missing_fields = []
            if not url:
                missing_fields.append("Redmine URL")
            if not api_key:
                missing_fields.append("API Key")
            messagebox.showwarning("Missing Information", f"The following fields are missing: {', '.join(missing_fields)}")
            return

        # Bilgileri kaydet ve devam et
        config['url'] = url
        config['api_key'] = api_key
        save_config(config)
        root.destroy()
        fetch_and_plot_data(config['url'], config['api_key'])

    root = Tk()
    root.title("Login")

    Label(root, text="Redmine URL:").grid(row=0, column=0, padx=10, pady=10)
    Label(root, text="API Key:").grid(row=1, column=0, padx=10, pady=10)

    url_var = StringVar(value=config.get('url', ''))
    api_key_var = StringVar(value=config.get('api_key', ''))

    Entry(root, textvariable=url_var, width=30).grid(row=0, column=1, padx=10, pady=10)
    Entry(root, textvariable=api_key_var, width=30).grid(row=1, column=1, padx=10, pady=10)

    Button(root, text="Save and Continue", command=save_and_continue).grid(row=2, column=0, columnspan=2, pady=20)

    root.mainloop()

# Ana ekran
def main():
    config = load_or_create_config()

    root = Tk()
    root.title("Welcome")

    def use_existing():
        root.destroy()
        fetch_and_plot_data(config['url'], config['api_key'])

    def new_user():
        root.destroy()
        login_screen(config)

    Label(root, text="Choose login method:").pack(pady=10)
    Button(root, text="Use Existing User", command=use_existing).pack(pady=5)
    Button(root, text="New User", command=new_user).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
