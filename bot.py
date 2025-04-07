async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    text = update.message.text.lower()

    # Обработка ввода ворот
    if context.user_data.get("awaiting_gates"):
        context.user_data["awaiting_gates"] = False
        if user_id in used_ids:
            await update.message.reply_text("Вы уже использовали возможность бесплатной расшифровки.")
            return
        try:
            gates = [int(x.strip()) for x in text.split(",")][:5]
            result = get_gate_description(gates)
            used_ids.add(user_id)
            await update.message.reply_text(result)
        except:
            await update.message.reply_text("Ошибка. Введите до 5 чисел через запятую, например: 10, 34, 57, 20, 16")
        return

    if "бесплатный" in text:
        await update.message.reply_text("Вы выбрали бесплатный разбор.")
        for fname in ["pic1.png", "pic2.png", "pic3.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
            except:
                pass

        try:
            with open("pic7.png", "rb") as img:
                await context.bot.send_photo(chat_id, img)
        except:
            pass

        try:
            with open("x1.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except:
            pass

        await update.message.reply_text("👇", reply_markup=get_form_buttons())

    elif "платный" in text:
        await update.message.reply_text("💸 Платный разбор. Информация ниже.")
        for fname in ["pic4.png", "pic4-1.png", "pic5.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
            except:
                pass
        try:
            with open("x2.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except:
            pass
        await update.message.reply_text("👇", reply_markup=get_contact_button())

    elif "vip" in text:
        await update.message.reply_text("👑 Пакет VIP: смотрите материалы ниже.")
        for fname in ["pic6.png", "pic5.png", "Voprosi.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
            except:
                pass
        try:
            with open("x3.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except:
            pass
        await update.message.reply_text("👇", reply_markup=get_contact_button())

    elif "обо мне" in text or "отзывы" in text:
        await update.message.reply_text(
            "Здесь вы можете прочитать про отзывы и систему — мой Instagram:\n"
            "https://www.instagram.com/vikram_hd_2027\n"
            "Ниже — примеры реальных сессий:"
        )
        for fname in ["p1.ogg", "primer_razbora.ogg"]:
            try:
                with open(fname, "rb") as audio:
                    await context.bot.send_audio(chat_id, audio)
            except:
                pass
        await update.message.reply_text("👇", reply_markup=get_contact_button())
