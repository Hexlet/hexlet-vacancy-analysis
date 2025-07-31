from telegram import ReplyKeyboardMarkup

markup_filters = ReplyKeyboardMarkup([
    ["frontend", "backend"],
    ["🔙 back"]
    ], resize_keyboard=True)

markup_front = ReplyKeyboardMarkup([
    ["React", "Vue.js", "Angular"],
    ["JS", "HTML", "CSS"],
    ["👌apply", "❌cancel", "🔙 back"]
    ], resize_keyboard=True)

markup_backend = ReplyKeyboardMarkup([
    ["Python", "Java", "Nodejs"],
    ["Go", "PHP", "C++"],
    ["👌apply", "❌cancel", "🔙 back"]
    ], resize_keyboard=True)

markup_interval = ReplyKeyboardMarkup([
    ["minute", "day", "week"],
    ["❌cancel", "🔙 back"]
    ], resize_keyboard=True)

markup_settings = ReplyKeyboardMarkup([
    ["create/update"],
    ["show"],
    ["delete"],
    ["exit"]
], resize_keyboard=True)
