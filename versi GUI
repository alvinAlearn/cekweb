import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def fetch_html(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"[!] Gagal mengakses {url} → {e}"

def detect_cms(html):
    cms_keywords = {
        "WordPress": ["/wp-content/", "wp-json", "wp-"],
        "Joomla": ["/components/com_", "joomla"],
        "Shopify": [".myshopify.com", "cdn.shopify.com"],
        "Drupal": ["/sites/all/", "drupal"],
        "Wix": ["wix.com", "wixstatic.com"],
        "Laravel": ["laravel_session", "X-Powered-By: Laravel"],
    }
    detected = []
    for cms, keywords in cms_keywords.items():
        for keyword in keywords:
            if keyword.lower() in html.lower():
                detected.append(cms)
                break
    return detected or ["Tidak terdeteksi"]

def extract_emails(html):
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", html)
    return list(set(emails)) or ["Tidak ditemukan"]

def detect_errors(html):
    errors_found = []
    error_patterns = {
        "MySQL Error": r"(mysql_fetch|mysql_num_rows|SQL syntax|MySQL server version)",
        "PHP Error": r"(Fatal error|Warning:|Notice:|Undefined variable)",
        "Stack Trace": r"(Traceback \(most recent call last\))",
        "File Path Disclosure": r"(in \/var\/www|C:\\xampp|home\/ubuntu|on line \d+)",
        "Server Errors": r"(500 Internal Server Error|403 Forbidden|502 Bad Gateway|503 Service Unavailable)"
    }
    for name, pattern in error_patterns.items():
        if re.search(pattern, html, re.IGNORECASE):
            errors_found.append(name)
    return errors_found or ["Tidak ditemukan"]

def fetch_meta_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    meta_tags = {}
    for meta in soup.find_all("meta"):
        name = meta.get("name", "").lower()
        property = meta.get("property", "").lower()
        content = meta.get("content")
        if name or property:
            if name:
                meta_tags[name] = content
            elif property:
                meta_tags[property] = content
    return meta_tags

def analyze_website(url):
    result = []
    html = fetch_html(url)
    if html.startswith("[!]"):
        return html
    soup = BeautifulSoup(html, "html.parser")
    result.append(f"\n🌐 URL: {url}")
    result.append(f"📄 Title: {soup.title.string.strip() if soup.title else 'Tidak ditemukan'}")
    
    # Meta tags analysis
    meta_tags = fetch_meta_tags(html)
    result.append(f"🔖 Meta Tags: {', '.join([f'{key}: {value}' for key, value in meta_tags.items()]) if meta_tags else 'Tidak ditemukan'}")

    result.append("🔧 CMS: " + ", ".join(detect_cms(html)))
    result.append("✉️ Email: " + ", ".join(extract_emails(html)))
    result.append("💥 Error: " + ", ".join(detect_errors(html)))
    return "\n".join(result)

def start_scan():
    output.delete(1.0, tk.END)
    urls = url_input.get("1.0", tk.END).strip().splitlines()
    threading.Thread(target=run_scan, args=(urls,)).start()

def run_scan(urls):
    for url in urls:
        if not url.startswith("http"):
            url = "http://" + url
        result = analyze_website(url)
        output.insert(tk.END, result + "\n" + ("-"*60) + "\n")

def load_from_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        with open(filepath, "r") as file:
            url_input.delete(1.0, tk.END)
            url_input.insert(tk.END, file.read())

def save_results():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt")
    if filepath:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(output.get(1.0, tk.END))

# GUI Setup
root = tk.Tk()
root.title("ALVCROZ TOOLS - Web Analyzer GUI Scanner")
root.geometry("800x600")

frame = tk.Frame(root)
frame.pack(pady=10)

url_input = scrolledtext.ScrolledText(frame, width=95, height=6)
url_input.pack()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="🔍 Mulai Scan", command=start_scan).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="📂 Load dari File", command=load_from_file).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="💾 Simpan Hasil", command=save_results).grid(row=0, column=2, padx=5)

output = scrolledtext.ScrolledText(root, width=100, height=25)
output.pack(pady=10)

root.mainloop()
