import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ChatMemberHandler, ContextTypes, MessageHandler, filters
)
from telegram.constants import ChatMemberStatus

TOKEN          = os.environ.get("BOT_TOKEN")
FOTO_FILE_ID   = "AgACAgEAAxkBAAMyakOb4_hn_JgOCb0Gtm0MwI4gbRoAAmgMaxtzGRhGrwJAtAABhm02AQADAgADeQADPAQ"

TESTO_BENVENUTO_TEMPLATE = "{user_tag} this group is locked for new members because we value the privacy of our members. in order to see all content, you are required to share the group link to 1 group in 3 minutes."

BOTTONI = [
    [
        InlineKeyboardButton("Share group 1 ↗️", url="https://t.me/share/url?url=https%3A%2F%2Ft.me%2F%2B82p9HZFXSG03NjUx"),
        InlineKeyboardButton("JOIN ↗️", url="https://t.me/+mCTWqtXc0Ls0ZTkx"),
    ],
    [
        InlineKeyboardButton("Share group 2 ↗️", url="https://t.me/share/url?url=https%3A%2F%2Ft.me%2F%2BmYOjuMgybWYxYTFh"),
        InlineKeyboardButton("JOIN ↗️", url="https://t.me/+mYOjuMgybWYxYTFh"),
    ],
    [InlineKeyboardButton("✅ Check ✅", url="http://t.me/tomocobbot?start=start")],
    [InlineKeyboardButton("⭐ FAST ACCESS ⭐", url="http://t.me/tomocobbot?start=start")],
]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def track_chats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Traccia i nuovi membri del gruppo."""
    result = await context.bot.get_chat(update.effective_chat.id)
    logger.info(f"Chat type: {result.type}, Title: {result.title}")


async def greet_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Invia il messaggio di benvenuto ai nuovi membri."""
    result = update.chat_member
    
    # Se il nuovo status è "member" (l'utente è entrato nel gruppo)
    if result.new_chat_member.status == ChatMemberStatus.MEMBER:
        user = result.new_chat_member.user
        chat_id = update.effective_chat.id
        
        logger.info(f"✅ Nuovo membro: {user.first_name} (ID: {user.id})")
        
        # Approva se necessario
        try:
            await context.bot.approve_chat_join_request(chat_id=chat_id, user_id=user.id)
            logger.info(f"Membro {user.id} approvato")
        except Exception as e:
            logger.info(f"Approvazione non necessaria: {e}")
        
        # Manda il benvenuto
        keyboard = InlineKeyboardMarkup(BOTTONI)
        user_tag = f"@{user.username}" if user.username else f"@{user.first_name}"
        testo = TESTO_BENVENUTO_TEMPLATE.format(user_tag=user_tag)
        
        try:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=FOTO_FILE_ID,
                caption=testo,
                reply_markup=keyboard,
            )
            logger.info(f"Benvenuto inviato a {user.first_name}")
        except Exception as e:
            logger.error(f"Errore invio benvenuto: {e}")


async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Estrae il file_id da una foto."""
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        await update.message.reply_text(f"file_id:\n{file_id}")
    else:
        await update.message.reply_text("Mandami una foto per ottenere il file_id.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bot attivo ✅")


def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(ChatMemberHandler(track_chats, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.PHOTO, get_file_id))
    app.add_handler(CommandHandler("start", start))
    
    logger.info("Bot avviato — in ascolto...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
