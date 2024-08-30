def process_urls(links_file):
    with open(links_file, 'r', encoding="utf-8") as f:
        urls = f.readlines()

    seen = set()
    duplicates = []
    for url in urls[:]:
        if '%' in url:
            urls.remove(url)
        elif url in seen:
            duplicates.append(url)
        else:
            seen.add(url)

    if duplicates:
        print("The following urls are duplicated:")
        for url in duplicates:
            print(url)
        for url in duplicates:
            urls.remove(url)

    with open(links_file, 'w', encoding="utf-8") as f:
        f.writelines(urls)
