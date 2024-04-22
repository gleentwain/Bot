async def cmd_special_buttons(message: Message):
    # Create the button
    github_button = InlineKeyboardButton(text="GitHub", url="https://github.com")
    
    # Define the keyboard layout (a list of lists)
    keyboard = [
        [github_button]
    ]
    
    # Create the InlineKeyboardMarkup with the keyboard layout
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    # Send the message with the keyboard
    await message.answer(
        text="Click the link below:",
        reply_markup=reply_markup,
        #disable_web_page_preview=True
    )