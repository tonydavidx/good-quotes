import langid

import pyperclip

text = pyperclip.paste()

language, confidence = langid.classify(text)
print(text)
print(f"Detected language: {language}, Confidence: {confidence}")
