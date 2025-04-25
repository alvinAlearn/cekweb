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
        print(f"[!] Gagal mengakses {url} → {e}")
        return None

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

def analyze_website(url):
    html = fetch_html(url)
    if not html:
        return

    soup = BeautifulSoup(html, "html.parser")
    result = []

    parsed = urlparse(url)
    domain = parsed.netloc.replace(".", "_")

    result.append(f"🌐 URL: {url}")
    result.append(f"\n📄 Title: {soup.title.string.strip() if soup.title else 'Tidak ditemukan'}\n")

    # META
    result.append("🧠 Meta Tags:")
    for tag in soup.find_all("meta"):
        name = tag.get("name") or tag.get("property") or tag.get("http-equiv")
        content = tag.get("content")
        if name and content:
            result.append(f"• {name}: {content}")

    # LINK Tags
    result.append("\n🔗 Link Tags (CSS, Canonical, dll):")
    for tag in soup.find_all("link"):
        rel = ", ".join(tag.get("rel", []))
        href = tag.get("href")
        if rel and href:
            result.append(f"• {rel} → {urljoin(url, href)}")

    # SCRIPT Tags
    result.append("\n🧩 JavaScript Files:")
    for tag in soup.find_all("script"):
        src = tag.get("src")
        if src:
            result.append(f"• {urljoin(url, src)}")

    # Favicon
    favicon = soup.find("link", rel=lambda r: r and "icon" in r)
    if favicon and favicon.get("href"):
        result.append(f"\n🌟 Favicon: {urljoin(url, favicon['href'])}")
    else:
        result.append("\n🌟 Favicon: Tidak ditemukan")

    # robots.txt
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    try:
        res = requests.get(robots_url, timeout=5)
        if res.status_code == 200:
            result.append(f"\n🤖 robots.txt ditemukan → {robots_url}")
        else:
            result.append("\n🤖 robots.txt: Tidak ditemukan")
    except:
        result.append("\n🤖 robots.txt: Gagal mengambil")

    # CMS Detection
    detected_cms = detect_cms(html)
    result.append("\n🔧 CMS Terdeteksi:")
    for cms in detected_cms:
        result.append(f"• {cms}")

    # Email Extraction
    emails = extract_emails(html)
    result.append("\n✉️ Email yang ditemukan:")
    for email in emails:
        result.append(f"• {email}")

    # Error Detection
    errors = detect_errors(html)
    result.append("\n💥 Error/Bug yang ditemukan:")
    for err in errors:
        result.append(f"• {err}")

    # Simpan ke file
    file_name = f"{domain}_analysis.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("\n".join(result))

    print(f"\n✅ Analisis selesai. Hasil disimpan di: {file_name}")

if __name__ == "__main__":
    url = input("🌐 Masukkan URL website (contoh: https://example.com): ").strip()
    analyze_website(url)
