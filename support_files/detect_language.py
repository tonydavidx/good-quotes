def check_char_lang(s):
    for char in s:
        if not char.isascii():
            return False
    return True


# print(check_english_chars("spending-money"))
