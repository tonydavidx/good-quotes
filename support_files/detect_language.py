def check_english_chars(s):
    non_english_count = 0
    for char in s:
        if not char.isascii():
            non_english_count += 1
            if non_english_count > 5:
                return False
    return True
