# config.py
import os  # os modülünü içe aktar (ortam değişkenlerini okumak için)

# Ortam değişkenlerinden API anahtarlarını oku
TOKEN = os.getenv("TELEGRAM_TOKEN", "your-telegram-bot-token")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY", "your-unsplash-api-key")

# Veritabanı yolu
DB_PATH = "tgbot.db"

# OpenAI API
OPENAI_MODEL = "gpt-4o-mini"

# Unsplash API
UNSPLASH_API_URL = "https://api.unsplash.com/search/photos"

# Admin
ADMIN_CODE = "ADMIN-12345"
ADMIN_CHAT_ID = "6120131340"

# RSS
DEFAULT_RSS_URL = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"

# Limits
MAX_CHANNELS = 20
MAX_PROMPT_LENGTH = 100

# Image Settings
IMAGE_SIZE = (1280, 720)

# Scheduler
SCHEDULE_INTERVAL_MINUTES = 60  # Varsayılan paylaşım sıklığı (dakika cinsinden), artık kullanılmayabilir

# Messages
WELCOME_MESSAGE = "Merhaba! Haber botuna hoş geldin. Aşağıdaki butonlarla botu kullanabilirsin."
INVALID_CODE_MESSAGE = "Geçersiz kod!"
CODE_USED_MESSAGE = "Bu kod zaten kullanılmış!"
ACTIVATED_CODE_MESSAGE = "Kod aktif edildi! Yeni bakiyeniz: {balance} paylaşım"
BALANCE_MESSAGE = "Kalan bakiyeniz: {balance} paylaşım"
SELECT_MODE_MESSAGE = "Paylaşım türünü seçin:"
RSS_MODE_MESSAGE = "RSS ile içerik çekme moduna geçtiniz. Ne yapmak istersiniz?"
ADD_SOURCE_MESSAGE = "Lütfen bir RSS URL’si girin (örneğin: https://example.com/feed)."
SET_TEMPLATE_MESSAGE = "Paylaşım şablonunu seçin:"
TEMPLATE_1_MESSAGE = "Şablon ayarlandı: Başlık + Özet + Kaynak"
TEMPLATE_2_MESSAGE = "Şablon ayarlandı: Başlık + 100 Karakter Özet"
AI_MODE_MESSAGE = "Yapay zeka ile içerik üretme moduna geçtiniz. Ne yapmak istersiniz?"
SINGLE_PROMPT_MESSAGE = "Lütfen paylaşım için bir prompt yazın (örneğin: Beden dilinin önemi). Maksimum 100 karakter."
CONCEPT_MODE_MESSAGE = "Kanalınızın konseptini açıklayın (örneğin: Kişisel gelişim ve motivasyon)."
NO_PROMPTS_MESSAGE = "Henüz prompt yazmadınız."
SETTINGS_MESSAGE = "Onay özelliği: {approval}\nGörsel ekleme: {images}"
APPROVAL_TOGGLED_MESSAGE = "Onay özelliği: {status}"
IMAGES_TOGGLED_MESSAGE = "Görsel ekleme: {status}"
APPROVE_MESSAGE = "Bu paylaşımı onaylıyor musunuz?\n{content}"
APPROVED_MESSAGE = "Paylaşım onaylandı ve kanala gönderildi!"
REJECTED_MESSAGE = "Paylaşım reddedildi."
NO_PENDING_MESSAGE = "Onay bekleyen paylaşım yok."
STATS_MESSAGE = "Toplam paylaşımlar: {total}\nKanal bazlı paylaşımlar:\n{channels}"
HELP_MESSAGE = "Botu nasıl kullanacağınızı öğrenmek için aşağıdaki butonlara tıklayın:"
HELP_MODES_MESSAGE = "Paylaşım Türleri:\n- RSS ile İçerik Çekme: RSS kaynaklarından haber çeker ve özetler.\n- Yapay Zeka ile İçerik Üretme: İki mod var:\n  - Tek Seferlik Prompt: Her paylaşım için prompt yazarsınız.\n  - Kanal Konsepti Modu: Bir konsept belirlersiniz, bot otomatik içerik üretir."
HELP_APPROVAL_MESSAGE = "Onay Özelliği:\nAyarlar menüsünden onay özelliğini açabilirsiniz. Açıkken, tüm paylaşımlar önce size gönderilir. Onaylarsanız kanala paylaşılır, reddederseniz silinir."
HELP_IMAGES_MESSAGE = "Görsel Ekleme:\nAyarlar menüsünden görsel eklemeyi açabilirsiniz. Açıkken, paylaşımlara konuyla alakalı görseller eklenir (Unsplash’tan çekilir)."
HELP_COMMANDS_MESSAGE = "Komutlar ve İpuçları:\n- /start: Botu başlatır.\n- /admin <kod>: Yönetici paneline girer.\n- Prompt yazarken kısa ve net olun (örneğin: Beden dilinin önemi)."
NO_CHANNEL_MESSAGE = "Önce bir kanal ekleyin!"
POST_SENT_MESSAGE = "Paylaşım kanala gönderildi!"
BALANCE_EXPIRED_MESSAGE = "Bakiyeniz bitti, yeni bir kod alın!"

# Yeni Eklenen Mesajlar
CHANNEL_ADDED_MESSAGE = "{channel_id} eklendi. Ayarları yapabilirsiniz:"
SOURCE_SET_MESSAGE = "{channel_id} için kaynak '{source}' olarak ayarlandı."
FREQUENCY_SET_MESSAGE = "{channel_id} için sıklık '{frequency}' olarak ayarlandı."
TYPE_SET_MESSAGE = "{channel_id} için paylaşım türü '{type}' olarak ayarlandı."
NO_CHANNELS_MESSAGE = "Henüz eklenmiş kanal yok."
