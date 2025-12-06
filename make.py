title = "מדריך טיולים"
places = [
    {"name": "Heddal Stave Church", "location": [59.579631217030496, 9.173712088688937], 
     "verify_location": [59.579631217030496, 9.173712088688937], "verify_dist_km": 10},
]
TAB = "  "

def number_to_hebrew_letters(n):
    HEBREW_NUMERALS = {
        1: 'א', 2: 'ב', 3: 'ג', 4: 'ד', 5: 'ה', 6: 'ו', 7: 'ז', 8: 'ח', 9: 'ט',
        10: 'י', 20: 'כ', 30: 'ל', 40: 'מ', 50: 'נ', 60: 'ס', 70: 'ע', 80: 'פ', 90: 'צ',
        100: 'ק', 200: 'ר', 300: 'ש', 400: 'ת'
    }
    
    if not isinstance(n, int) or n < 1:
        raise ValueError("Input must be a positive integer.")

    if n == 15:
        return "ט\"ו"  # Tet-Vav
    if n == 16:
        return "ט\"ז"  # Tet-Zayin

    hebrew_output = []
    
    # Handle hundreds
    if n >= 100:
        hundreds = (n // 100) * 100
        hebrew_output.append(HEBREW_NUMERALS.get(hundreds, ''))
        n %= 100

    # Handle tens and units
    if n > 0:
        # Prioritize exact matches for tens and units (e.g., 20, 30, 5)
        if n in HEBREW_NUMERALS:
            hebrew_output.append(HEBREW_NUMERALS[n])
        else:
            tens = (n // 10) * 10
            units = n % 10
            if tens > 0:
                hebrew_output.append(HEBREW_NUMERALS.get(tens, ''))
            if units > 0:
                hebrew_output.append(HEBREW_NUMERALS.get(units, ''))

    return "".join(hebrew_output)

def process_places():
    chapter = 1
    for i in range(len(places)):
        places[i]["id"] = i + 1
        places[i]["chapter"] = chapter

def get_template():
    with open("template", "r", encoding="utf-8") as f:
        return f.read()
    
def write_index_html(txt):
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(txt)

def make_check_location(place):
    params = [32.3913, 34.9221, '1 - כנסיית העץ העתיקה']
    params = [f"'{p}'" if isinstance(p, str) else p for p in params]
    params = [str(p) for p in params]
    s = f"checkLocation({', '.join(params)})"
    return s

def make_button(place):
    s = f'<button onclick="{make_check_location(place)}">{place["id"]}</button>'
    return s
    
def make_body(places):
    body = f"<h1>{title}</h1>\n"
    chapter = 0
    for place in places:
        if place["chapter"] != chapter:
            chapter = place["chapter"]
            hebrew_chapter = number_to_hebrew_letters(chapter)
            body += 2*TAB + f"<h2>פרק {hebrew_chapter}</h2>\n"
        body += 3*TAB + make_button(place) + "\n"
    return body

def main():
    process_places()
    template = get_template()
    body = make_body(places)
    final_html = template.replace("{{BODY}}", body)
    write_index_html(final_html)
    
if __name__ == "__main__":
    main()
    print("done")