"""
Gardio Constants & Configuration
"""
import re

VERSION = "2.3.0"
DEBUG = False

# Stop Words for Frequency Analysis
STOP_WORDS = {
    "the", "and", "a", "to", "of", "in", "it", "is", "i", "that", 
    "on", "for", "was", "with", "as", "be", "at", "by", "this"
}

# Regex Patterns
RE_NUMBERS = re.compile(r'-?\d+\.?\d*')
RE_URLS = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')

# Fun Data
JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
    "There are 10 types of people: those who understand binary and those who don't. 💻",
    "A SQL query walks into a bar and asks two tables: 'Can I join you?' 🍺",
    "Why do Java developers wear glasses? Because they can't C#! 👓",
    "What's a programmer's favorite hangout? Foo Bar! 🍸",
    "How do you comfort a JavaScript bug? You console it! 🖥️",
    "Why was the JavaScript developer sad? Because he didn't Node how to Express himself! 😢",
    "What's a programmer's favorite snack? Chips and dip... into the codebase! 🍟",
    "Why did the programmer quit? Because he didn't get arrays (a raise)! 💰",
    "What do you call 8 hobbits? A hobbyte! 🧙"
]

QUOTES = [
    "'Code is like humor. When you have to explain it, it's bad.' - Cory House 📝",
    "'First, solve the problem. Then, write the code.' - John Johnson 💡",
    "'Simplicity is the soul of efficiency.' - Austin Freeman ✨",
    "'Programs must be written for people to read.' - Harold Abelson 📖",
    "'Good programmers write code that humans can understand.' - Martin Fowler 🧠",
    "'The best code is no code at all.' - Jeff Atwood 🎯",
    "'It works on my machine.' - Every Developer 😅",
    "'Talk is cheap. Show me the code.' - Linus Torvalds 💬",
    "'Any fool can write code that a computer can understand.' - Martin Fowler 🤖",
    "'Measuring progress by lines of code is like measuring aircraft by weight.' - Bill Gates ✈️"
]
