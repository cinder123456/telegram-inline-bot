import os
import uuid
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, InlineQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

PRESETS = {
    "sunset": "A cinematic sunset over mountains, ultra realistic, 4k, golden hour lighting",
    "anime": "Anime style portrait, soft lighting, detailed eyes, studio quality illustration",
    "cyberpunk": "Cyberpunk city at night, neon lights, rain, ultra detailed, futuristic",
    "forest": "Mystical forest with fog, glowing lights, fantasy atmosphere, highly detailed",
    "portrait": "Professional portrait photo, 85mm lens, shallow depth of field, soft lighting"
}

async def inline_query(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.lower().strip()

    results = []

    if not query:
        for key, prompt in PRESETS.items():
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=f"🌟 {key}",
                    description=prompt[:60],
                    input_message_content=InputTextMessageContent(
                        message_text=prompt
                    )
                )
            )
    else:
        words = query.split()
        expanded = [PRESETS.get(w, w) for w in words]
        final_prompt = " ".join(expanded)

        results.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="✨ Generated Prompt",
                description=final_prompt[:60],
                input_message_content=InputTextMessageContent(
                    message_text=final_prompt
                )
            )
        )

    await update.inline_query.answer(results, cache_time=0)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(InlineQueryHandler(inline_query))

app.run_polling()

