import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ChatMemberHandler, ContextTypes
)

TOKEN          = os.environ.get("BOT_TOKEN")
FOTO_FILE_ID   = "AgACAgEAAxkBAAMyakOb4_hn_JgOCb0Gtm0MwI4gbRoAAmgMaxtzGRhGrwJAtAABhm02AQADAgADeQADPAQ"

# Testo di benvenuto
TESTO_BENVENUTO = "{user_tag} this group is locked for new members because we value the privacy of our members. in order to see all content, you are required to share the group link to 1 group in 3 minutes."

# Bottoni con i link esatti
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


async def approva_membro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Approva automaticamente i nuovi membri e manda il messaggio di benvenuto."""
    my_chat_member = update.my_chat_member
    
    # Controlla se è un nuovo membro
    if my_chat_member.new_chat_member.status == "restricted":
        # Il bot è stato aggiunto al gruppo (ignore questo evento)
        return
    
    # Controlla se un nuovo membro è entrato
    if update.chat_member:
        member = update.chat_member.new_chat_member
        user = member.user
        chat_id = update.effective_chat.id
        
        # Se il membro ha lo status "restricted" (in attesa di approvazione)
        if member.status == "restricted" and not member.is_member:
            logger.info(f"Nuovo membro: {user.first_name} (ID: {user.id})")
            
            # Approva il membro
            try:
                await context.bot.approve_chat_join_request(chat_id=chat_id, user_id=user.id)
                logger.info(f"Membro {user.id} approvato")
            except Exception as e:
                logger.warning(f"Errore nell'approvazione: {e}")
            
            # Manda il messaggio di benvenuto
            keyboard = InlineKeyboardMarkup(BOTTONI)
            try:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=FOTO_FILE_ID,
                    caption=TESTO_BENVENUTO,
                    reply_markup=keyboard,
                )
                logger.info(f"Messaggio di benvenuto inviato per {user.first_name}")
            except Exception as e:
                logger.warning(f"Errore nell'invio del messaggio: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando start nel gruppo."""
    await update.message.reply_text("Bot di benvenuto attivo! ✅")


def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Handler per i nuovi membri
    app.add_handler(ChatMemberHandler(approva_membro, ChatMemberHandler.CHAT_MEMBER))
    
    # Handler per il comando /start
    app.add_handler(CommandHandler("start", start))
    
    logger.info("Bot di benvenuto avviato — in ascolto...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
