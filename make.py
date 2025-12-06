import os
import folium
import webbrowser
import numpy as np

title = "מדריך טיולים"
places = [
    ############################## DAY 1 ##############################
    {"name": "Heddal Stave Church", "hebrew_name": "כנסיית העץ העתיקה",
     "location": [59.579631217030496, 9.173712088688937], 
     "verify_locations": [
            [59.91028747001133, 10.759149875920937],
            [59.84136536105944, 10.451532708227695],
            [59.76953468860811, 10.20983348823977],
            [59.76953468833935, 9.902216326736134],
            [59.6698211140157, 9.649530779118379],
            [59.59484073364515, 9.391352091948987]], 
     "verify_dists_km": [10,10,10,10,10,11]},
    
    {"name": "Vågslidtun Hotell AS", "hebrew_name": "מלון ווגסלידטון",
     "location": [59.76946921278479, 7.389044921790655], 
     "verify_locations": [
            [59.604428973465716, 9.002843569125318],
            [59.601952753759186, 8.714106257699223],
            [59.5213762499024, 8.479201326369518],
            [59.57718052131577, 8.227167910463688],
            [59.64773329594539, 8.016732242814161],
            [59.70826557919452, 7.847894323420936],
            [59.758831062258956, 7.5983078338831245]], 
     "verify_dists_km": [15,15,15,15,15,15,15]},
    
    None,
    
    ############################## DAY 2 ##############################
    {"name": "Eidfjord", "hebrew_name": "איידפיורד",
     "location": [60.46673360531188, 7.068500369061384], 
     "verify_locations": [
            [59.77074552110632, 7.387719303695958],
            [59.84671279436948, 7.041649983356277],
            [59.88256436250444, 6.657128516312186],
            [60.002248481060924, 6.5637447314586215],
            [60.177551313893375, 6.577477640995911],
            [60.33289670959683, 6.64064902486744],
            [60.47126610499866, 6.942773034687797],
     ],
     "verify_dists_km": [13]},
    
    {"name": "Steinsdalsfossen", "hebrew_name": "מפלי שטיינסדלספוסן",
     "location": [60.37024545975006, 6.108024022985264], 
     "verify_locations": [
            [60.4671063415852, 7.071674703857783],
            [60.478164871044946, 6.9549949548774705],
            [60.4925353265063, 6.820364475284801],
            [60.51684005789785, 6.705928567631032],
            [60.46931834894866, 6.607199549263075],
            [60.441657420014856, 6.465837545690771],
            [60.41175714571005, 6.36486468599627],
            [60.3840471817699, 6.248184937015956],
            [60.37295659022326, 6.138236712015276]
     ],
     "verify_dists_km": [7]},

    {"name": "Bergen", "hebrew_name": "ברגן",
     "location": [60.39118163725193, 5.3216444182500835], 
     "verify_locations": [
            [60.46444368600508, 7.070500607404774], # 1
            [60.46997387537984, 6.913431714546659], # 2
            [60.50203039840591, 6.803483489545979], # 3
            [60.53736635829316, 6.729436725770012], # 4
            [60.57597094201803, 6.637439231381687], # 5
            [60.62993998410787, 6.500564910462472], # 6
            [60.62773893200973, 6.312082239032736], # 7
            [60.64534314264172, 6.11462420229682], # 8
            [60.631040453818855, 5.9396045788263505], # 9
            [60.59360340811992, 5.8161933058664035], # 10
            [60.53957357600379, 5.728683494131168], # 11
            [60.4743973485414, 5.7354150181108015], # 12
            [60.44009965749914, 5.643417523722478], # 13
            [60.4998206207743, 6.6733406926063985], # 14
            [60.45669983789584, 6.55890478495263], # 15
            [60.432350003256055, 6.419786622706872], # 16
            [60.390248197799764, 6.27393693648148], # 17
            [60.37149659381248, 6.09943492983304],
            [60.389774219066666, 5.9649563981270255],
            [60.378975043744816, 5.786772343616557],
            [60.39807884063268, 5.647250866971567],
            [60.421320513449416, 5.522858225143504],
            [60.446203886686334, 5.322821409230806],
            [60.30994200690759, 5.519496261850852],
            [60.233194783497025, 5.454281537155975],
            [60.309109392727244, 5.326183372523458],
            [60.39890918628314, 5.395103620022788]
     ],
     "verify_dists_km": [7]},
    
    None,
    None,
    
    ############################### DAY 4 ##############################
    {"name": "Bryggen", "hebrew_name": "מדרחוב בריגן",
     "location": [60.397563989685075, 5.324544119062977], 
     "verify_locations": [
            [60.39701413593635, 5.3249930481642185],
     ],
     "verify_dists_km": [3], 
     "waze": False},
    
]
TAB = "  "
plots_dir = "plots"

def rhex(a,b):
    return "{:02x}".format(np.random.randint(a, b))

def make_place_map(place, m=None):
    locs = [place['location'][1]] + [loc[1] for loc in place['verify_locations']]
    lats = [place['location'][0]] + [loc[0] for loc in place['verify_locations']]
    center_lat = float(np.mean(lats))
    center_lon = float(np.mean(locs))
    
    if m is None:
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=8,
            tiles="OpenStreetMap"  # Default map with names
        )
    
     # location itself
    folium.Circle(
        location=place['location'], radius=3*1e3,
        color="blue", fill=True, fill_opacity=0.5,
        popup=place['name']
    ).add_to(m)

    # verification locations
    # random green color
    green = f"#{rhex(0,100)}{rhex(150,200)}{rhex(0,100)}"
    for i, loc in enumerate(place['verify_locations']):
        folium.Circle(
            location=loc, radius=place['verify_dists_km'][i] * 1000,
            color=green, fill=True, fill_opacity=0.2,
            popup=f"Verification Location {i+1}"
        ).add_to(m)
    return m

def make_place_plot_html(place):
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    m = make_place_map(place)
        
    # Save output to HTML
    plotfile = os.path.join(plots_dir, place['name'].replace(" ", "_") + "_map.html")
    m.save(plotfile)
    return os.path.abspath(plotfile)

def open_html(file):
    webbrowser.open(f"file://{file}")
    
def plot_places(places):
    for place in places:
        plotfile = make_place_plot_html(place)
        webbrowser.open(f"file://{plotfile}")

    m = make_place_map(places[0])
    for place in places[1:]:
        m = make_place_map(place, m)
    overview_plotfile = os.path.join(plots_dir, "overview_map.html")
    m.save(overview_plotfile)
    open_html(overview_plotfile)
    
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
    global places
    chapter = 1
    id = 1
    for i in range(len(places)):
        if places[i] is None:
            chapter += 1
            continue
        if "waze" not in places[i]:
            places[i]["waze"] = True
        places[i]["id"] = id
        places[i]["chapter"] = chapter
        if len(places[i]['verify_dists_km']) == 1:
            places[i]['verify_dists_km'] = \
                places[i]['verify_dists_km'] * len(places[i]['verify_locations'])
        id += 1
    places = [p for p in places if p is not None]

def get_template():
    with open("template", "r", encoding="utf-8") as f:
        return f.read()
    
def write_index_html(txt):
    file = "index.html"
    with open(file, "w", encoding="utf-8") as f:
        f.write(txt)
    return os.path.abspath(file)

def make_check_location(place):
    # destLat, destLng, placeName, verified_locations, verify_dists_km, waze
    params = place['location'] + [place['hebrew_name']] + \
             [place['verify_locations'], place['verify_dists_km'], 
              1 if place['waze'] else 0]
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
    htmlfile = write_index_html(final_html)
    open_html(htmlfile)
    # plot_places(places)
    
    
if __name__ == "__main__":
    main()
    print("done")