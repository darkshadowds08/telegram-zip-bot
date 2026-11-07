import os
import zipfile
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# استبدل YOUR_BOT_TOKEN بالتوكن الخاص بك من BotFather
TOKEN = "9022856959:AAG0MIKvmYXivu3Ea7hD6rBgCpyU78f-j78"

# مجلد مؤقت لحفظ الملفات
DOWNLOAD_DIR = "downloads"
OUTPUT_DIR = "output"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    
    # التحقق مما إذا كانت الرسالة تحتوي على مستند أو ملف
    if not message.document and not message.audio and not message.video:
        await message.reply_text("الرجاء إرسال ملف (مستند، صورة، إلخ) لضغطه.")
        return

    await message.reply_text("جاري تحميل الملف وضغطه...")

    # الحصول على الملف
    file_obj = await message.document.get_file()
    file_name = message.document.file_name
    file_path = os.path.join(DOWNLOAD_DIR, file_name)
    
    # تحميل الملف إلى الخادم
    await file_obj.download_to_drive(file_path)

    # تجهيز اسم ملف الـ ZIP
    zip_name = f"{os.path.splitext(file_name)[0]}.zip"
    zip_path = os.path.join(OUTPUT_DIR, zip_name)

    # ضغط الملف بصيغة ZIP
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, arcname=file_name)

    # إرسال الملف المضغوط للمستخدم
    with open(zip_path, 'rb') as zip_file:
        await message.reply_document(document=zip_file, caption="تم ضغط الملف بنجاح!")

    # تنظيف الملفات المؤقتة
    os.remove(file_path)
    os.remove(zip_path)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # استقبال الملفات بمختلف أنواعها
    app.add_handler(MessageHandler(filters.ATTACHMENT, handle_file))

    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()
