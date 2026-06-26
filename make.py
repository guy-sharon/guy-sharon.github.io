import time
import os
import folium
import webbrowser
import numpy as np
from docx import Document
import re
import glob

DEBUG = False

place0 = {"name": "Oslo Lufthavn", "hebrew_name": "נמל התעופה אוסלו",
          "location": [60.19285678506807, 11.098836497239045]}

title = "מדריך טיולים"
places = [
    
    ############################## DAY 0 ##############################
    {"name": "Quality Hotel Olavsgaard", "hebrew_name": "מלון קווליטי אולאבסגארד",
     "location": [59.97937318811253, 11.000563373446656], 
     "verify_locations": [
            [60.175314284269675, 11.094582912573745], # 1
            [60.143621944931844, 11.158274886436065], # 2
            [60.08706878105246, 11.143576738621684], # 3
            [60.039391148523656, 11.11418044299292], # 4
            [60.00021956333046, 11.039873140153547]], 
     "verify_dists_km": [4]},
    
    None,
    
    ############################## DAY 1 ##############################
    {"name": "Herstrom Rasteplass", "hebrew_name": "תחנת מנוחה הרסטרום",
     "location": [59.75825102148356, 10.068491295946465], 
     "verify_locations": [
            [59.91028747001133, 10.759149875920937],
            [59.84136536105944, 10.451532708227695],
            [59.76953468860811, 10.20983348823977],
            [59.76953468833935, 9.902216326736134],
            [59.6698211140157, 9.649530779118379],
            [59.59484073364515, 9.391352091948987]], 
     "verify_dists_km": [10,10,10,10,10,11]},
    
    {"name": "Kafe Olea", "hebrew_name": "קפה אוליה בכנסיית העץ העתיקה",
     "location": [59.579631217030496, 9.173712088688937], 
     "verify_locations": [
            [59.91028747001133, 10.759149875920937],
            [59.84136536105944, 10.451532708227695],
            [59.76953468860811, 10.20983348823977],
            [59.76953468833935, 9.902216326736134],
            [59.6698211140157, 9.649530779118379],
            [59.59484073364515, 9.391352091948987]], 
     "verify_dists_km": [10,10,10,10,10,11]},
    
    {"name": "Sjorormen Kro", "hebrew_name": "מסעדת סיורמנן קרו",
     "location": [59.48075676708875, 8.635438953156646], 
     "verify_locations": [ 
            [59.91028747001133, 10.759149875920937]],
     "verify_dists_km": [10]},
    
    {"name": "Dalen Bruggekafé", "hebrew_name": "בית הקפה דאלן ברוגקהפה",
     "location": [59.445073835718375, 8.024244166693663], 
     "verify_locations": [ 
            [59.91028747001133, 10.759149875920937]],
     "verify_dists_km": [10]},
    
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
     "verify_dists_km": [10]},
    
    None,
    
    ############################## DAY 2 ##############################
    {"name": "Låtefossen Waterfall", "hebrew_name": "מפלי לטפוסן",
     "location": [59.94824252336145, 6.58365642803515], 
     "verify_locations": [
            [59.76787559060073, 7.3895109972957815], # 1
            [59.7876269314034, 7.297952525058634], # 2
            [59.82051986619606, 7.203124107384445], # 3
            [59.84735836460373, 7.087586035275664], # 4
            [59.84735836460373, 6.9676880359174955], # 5
            [59.84681085633585, 6.865229745556879], # 6
            [59.81997191650139, 6.77803120056912], # 7
            [59.84845335412083, 6.708272364578912], # 8
            [59.89003626898682, 6.6494133467121745], # 9
            [59.924466914624595, 6.590554328845437], # 10
     ],
     "verify_dists_km": [4]},
    
    {"name": "Fløy Café & Bakery", "hebrew_name": "בית הקפה והמאפייה פלוי" + "&#10;(יש מכולת ממול)",
     "location": [60.32490612151451, 6.65844841798013], 
     "verify_locations": [
            [59.76787559060073, 7.3895109972957815], # 1
            [59.7876269314034, 7.297952525058634], # 2
            [59.82051986619606, 7.203124107384445], # 3
            [59.84735836460373, 7.087586035275664], # 4
            [59.84735836460373, 6.9676880359174955], # 5
            [59.84681085633585, 6.865229745556879], # 6
            [59.81997191650139, 6.77803120056912], # 7
            [59.84845335412083, 6.708272364578912], # 8
            [59.89003626898682, 6.6494133467121745], # 9
            [59.924466914624595, 6.590554328845437], # 10
            [59.95284607423546, 6.582430909902832], # 1
            [59.9975820888222, 6.5623918443092615], # 2
            [60.04456685623816, 6.565474777477503], # 3
            [60.091484863842105, 6.551601578220416], # 4
            [60.13756865818384, 6.567016244061624], # 5
            [60.17438927445983, 6.590138242823436], # 6
            [60.217294554761054, 6.605552908664643], # 7
            [60.25096651156644, 6.613260241585247], # 8
            [60.28307565854426, 6.616343174753489], # 9
            [60.307518630051774, 6.644089573267662], # 10
     ],
     "verify_dists_km": [4]},
    
    {"name": "Vik Café & Restaurant", "hebrew_name": "מסעדת ויק באיידפיורד",
     "location": [60.46689812548009, 7.0702280865386085], 
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
    
    {"name": "YX Eidfjord", "hebrew_name": "תחנת דלק באידפיורד",
     "location": [60.46604481212193, 7.071072694319243], 
     "verify_locations": [
            [59.77074552110632, 7.387719303695958],
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
     "verify_dists_km": [6]},

    {"name": "Thon Hotel Sandven", "hebrew_name": "מלון תון סנדוונן",
     "location": [60.39118163725193, 5.3216444182500835], 
     "verify_locations": [ [60.46444368600508, 7.070500607404774], ],
     "verify_dists_km": [7]},

    None,
    ############################### DAY 3 ##############################
    
    {"name": "Home Hotel Havnekontoret", "hebrew_name": "מלון הום האבנקונטורט בברגן",
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
    
    {"name": "Baker Brun", "hebrew_name": "מאפיית בייקר בראון",
     "location": [60.392346654063516, 5.325385177527572],
     "waze": False},
    
    {"name": "Strandkaien 13", "hebrew_name": "נקודת מפגש לשייט במפרץ מוסטראומן",
     "location": [60.39473469822, 5.323139034997865],
     "waze": False},
    
    None,
    
    ############################### DAY 4 ##############################
    {"name": "Bryggen", "hebrew_name": "מדרחוב בריגן",
     "location": [60.397563989685075, 5.324544119062977],
     "waze": False},
    
    {"name": "Fishmarket in Bergen", "hebrew_name": "שוק הדגים בברגן",
     "location": [60.394751321111414, 5.325181579382361],
     "waze": False},
    
    {"name": "Floibanen", "hebrew_name": "רכבל פלויבנן",
     "location": [60.39635497566565, 5.328403478094899],
     "waze": False},
    
    {"name": "The Unicorn Fish Restaurant", "hebrew_name": "מסעדת יוניקורן פיש",
     "location": [60.39721576580881, 5.323410199767801], 
     "waze": False},
    
    None,
    
    ############################### DAY 5 ##############################
    # {"name": "WC middle of the road", "hebrew_name": "שירותים באמצע הדרך",
    #  "location": [60.64537216627435, 6.058899102161327], 
    #  "verify_locations": [ [60.46444368600508, 7.070500607404774], ],
    #  "verify_dists_km": [7]},
    
    {"name": "VossaBakst AS", "hebrew_name": "מאפיית ווסאבאקט",
     "location": [60.64537216627435, 6.058899102161327], 
     "verify_locations": [ [60.46444368600508, 7.070500607404774], ],
     "verify_dists_km": [7]},
    
    {"name": "Viking Valley", "hebrew_name": "עמק הוויקינגים",
     "location": [60.87871641194426, 6.842783130309827], 
     "verify_locations": [
            [60.40066570873266, 5.323763179332352], # 1
            [60.462177279559754, 5.325596302854006], # 2
            [60.45313875912446, 5.442916208239834], # 3
            [60.42781751490292, 5.5620692371473135], # 4
            [60.45585057942066, 5.734382848182747], # 5
            [60.53168966268797, 5.728883477617786], # 6
            [60.604652344445846, 5.822372777222117], # 7
            [60.63702736803587, 5.9580239178244785], # 8
            [60.64691325641476, 6.148668764076448], # 9
            [60.62623930374835, 6.3338142397634565], # 10
            [60.68463149136252, 6.456633515714244], # 11
            [60.743813781079474, 6.493295986147315], # 12
            [60.78947093617446, 6.561121556448497], # 13
            [60.80735796205203, 6.645445238444559], # 14
            [60.85024607629493, 6.764598267352039], # 15
     ],
     "verify_dists_km": [7]},

    {"name": "Flåm parkering", "hebrew_name": "חניון בפלום",
     "location": [60.86407928930206, 7.111914402379143], 
     "verify_locations": [
            [60.891633364294144, 7.038671207753574], # 1
            [60.88234900079604, 6.896964710116111], # 2
     ],
     "verify_dists_km": [7]},
    
    {"name": "Flåm Ferdaminne AS", "hebrew_name": "מלון פלום פרדמין",
     "location": [60.86334669919673, 7.1162314240336215], 
     "verify_locations": [
            [60.891633364294144, 7.038671207753574], # 1
            [60.88234900079604, 6.896964710116111], # 2
     ],
     "waze": False,
     "verify_dists_km": [7]},
    
    None,
    
    ############################### DAY 6 ##############################
    # {"name": "Undredal", "hebrew_name": "אונדרדל",
    #  "location": [60.95151192075261, 7.104576536199135], 
    #  "verify_locations": [
    #         [60.878391678358604, 7.105231529246835], # 1
    #  ],
    #  "verify_dists_km": [7]},
    
    {"name": "Flåmsbana", "hebrew_name": "רכבת פלם",
     "location": [60.863025494522724, 7.114590114743707],
     "waze": False},
    
    {"name": "Fjord Cruise Aurlandsfjord", "hebrew_name": "שייט במפרץ נארוי",
     "location": [60.86287674667964, 7.114571259500795],
     "waze": False},
    
    None,
    
    ############################### DAY 7 ##############################
    {"name": "Stegastein Parking", "hebrew_name": "חניון סטגסטיין",
     "location": [60.90817847117424, 7.213003197679032],
     "waze": False},
    
    {"name": "Borgund Stave Church", "hebrew_name": "כנסיית העץ בורגונד",
     "location": [61.048663423927174, 7.814260366096567], 
     "verify_locations": [
            [60.88072412246814, 7.151068252896669], # 1
            [60.900098465041886, 7.185400526739893], # 2
            [60.91946104394952, 7.254065072693247], # 3
            [60.93747770275531, 7.2980103832125724], # 4
            [60.962150651335364, 7.346075566593083], # 5
            [60.98813657163624, 7.41062024141834], # 6
            [61.01476673988225, 7.449072388122749], # 7
            [61.04403414117387, 7.483404661965972], # 8
            [61.05467013871214, 7.524603390577839], # 9
            [61.05068205789077, 7.587774774449368], # 10
            [61.05068205789077, 7.653692740228355], # 11
            [61.051346772880436, 7.708624378377511], # 12
            [61.051346772880436, 7.769049180341582], # 13
     ],
     "verify_dists_km": [2.5]},
    
    {"name": "Borgund Servicesenter AS", "hebrew_name": "תחנת דלק בורגונד",
     "location": [61.08029808349784, 7.848186229821723]},
    
    {"name": "Borgund Vedovnsbakeri", "hebrew_name": "מאפיית בורגונד",
     "location": [61.08248842266929, 7.854405871833045],
     "waze": False},
    
    {"name": "China Garden Restaurant Hemsedalsvegen", "hebrew_name": "מסעדת צ'יינה גארדן",
     "location": [60.84962059362721, 8.616923162287812]},
    
    {"name": "Borts Fusion Restaurant", "hebrew_name": "מסעדת בורט פיוזן",
     "location": [60.70080181928564, 8.94925099428799]},
    
    {"name": "Ming Beijing House", "hebrew_name": "מסעדת מינג בייג'ינג האוס",
     "location": [60.700971327282296, 8.951952419923199]},
    
    {"name": "Hallingporten Kro og Asiamat AS", "hebrew_name": "מסעדת האלינגפורטן קרו ואסיאמאט",
     "location": [60.38090060466161, 9.60986817096384]},
    
    {"name": "Sundvolden Hotel", "hebrew_name": "מלון סונדוולדן",
     "location": [60.06328083013986, 10.310203485093925]},
]

TAB = "  "
plots_dir = "plots"

def pop_first_location_indicator(content):
    match = re.search(r"\[(\d+)\]", content)
    if match:
        return content[:match.start()], \
               content[match.end():], \
               int(match.group(1))
    raise Exception("No location indicator found")

def validate_word(docx_filename=None):
    if docx_filename is None:
        docx_filename = glob.glob(os.path.join("C:\\Users\\guysh\\Downloads", "*.docx"))
        docx_filename.sort(key=os.path.getmtime, reverse=True)
        docx_filename = docx_filename[0]
        
    content = docx_to_txt_docx_method(docx_filename).lower()
    last_id = None
    for place in places:
        if place is None:
            continue
        curr_id = place['id']
        if last_id is not None:
            assert curr_id == last_id + 1, f"ID mismatch for '{place['name']}': expected {last_id + 1}, found {curr_id}"
        last_id = curr_id if 'id' in place else last_id
        name = place['name'].lower()
        assert name in content, f"Place name '{name}' (id {place['id']}) not found in {docx_filename}"
        ind = content.index(name)
        
        # Find the last occurrence of [<number>] before this place name
        matches = list(re.finditer(r"\[(\d+)\]", content[:ind]))
        if matches:
            li = int(matches[-1].group(1))
            assert li == place['id'], \
                f"Location indicator mismatch for '{name}': expected {place['id']}, found {li}"
        
def docx_to_txt_docx_method(docx_filename):
    document = Document(docx_filename)
    full_text = []
    for para in document.paragraphs:
        full_text.append(para.text)

    # Join paragraphs with a newline character
    content = '\n'.join(full_text)
    return content


def rhex(a,b):
    return "{:02x}".format(np.random.randint(a, b))

def make_place_map(place, m=None, id=None):
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
    if len(place['verify_locations']) == 0:
        self_radius = 800
        opacity = 0.2
        color = "torquoise"
    else:
        self_radius = 1e3 if DEBUG else 3e3
        opacity = 0.5
        color = "blue"
    
    if id is not None: # print only text id on map
        folium.Marker(
            location=place['location'],
            icon=folium.DivIcon(
                html=f'<div style="font-size: 16pt; color: black; text-align: center;">{id}</div>'
            ),
            popup=place['name']
        ).add_to(m)
    else:
        folium.Circle(
            location=place['location'], radius=self_radius,
            color=color, fill=True, fill_opacity=opacity,
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
    # chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    os.system(f'start chrome "{os.path.abspath(file)}"')
    # webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    # webbrowser.open(f"file://{os.path.abspath(file)}")
    
def plot_places(places, overview_only=False):
    if not overview_only:
        for place in places[:]:
            plotfile = make_place_plot_html(place)
            open_html(plotfile)

    # overview
    m = make_place_map(places[0], id=places[0]['id'])
    for place in places[1:]:
        m = make_place_map(place, m, id=place['id'])

    # connect all overview places with a route line
    route_locations = [place['location'] for place in places]
    folium.PolyLine(
        locations=route_locations,
        color='red',
        weight=3,
        opacity=0.7
    ).add_to(m)

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
        if 'verify_locations' not in places[i]:
            places[i]['verify_locations'] = []
            places[i]['verify_dists_km'] = []
        places[i]["id"] = id
        places[i]["chapter"] = chapter
        if len(places[i]['verify_dists_km']) == 1:
            places[i]['verify_dists_km'] = \
                places[i]['verify_dists_km'] * len(places[i]['verify_locations'])
        id += 1
    places = [p for p in places if p is not None]

def get_template():
    with open("template", "r", encoding="utf-8") as f:
        data = f.read()
    if DEBUG:
        data = data.replace("if (distance <= 1000) { // within 1km", 
                            "if (distance <= 20e3) { // within 20km")
        
    return data
    
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
    s = f"""<button onclick="{make_check_location(place)}">{place["id"]}
        <div style="white-space: pre-wrap; font-size: 0.4em; margin-top: 0.3em;">{place["hebrew_name"]}</div>
        </button>
    """
    # s = f'<button onclick="{make_check_location(place)}">{place["id"]}</button>'
    return s
    
def make_body(places):
    body = f"<h1>{title}</h1>\n"
    chapter = 0
    day = 3
    for place in places:
        if place["chapter"] != chapter:
            chapter = place["chapter"]
            hebrew_chapter = number_to_hebrew_letters(chapter)
            # body += 2*TAB + f"<h2>פרק {hebrew_chapter}</h2>\n"
            # Responsive date header using CSS flexbox for centering
            date_str = f"{day}/08"
            body += 2*TAB + f"""
            <div style="display: flex; justify-content: center; align-items: center; margin: 1em 0;">
                <div style="flex: 1; border-bottom: 1px solid #000; border-top: 1px solid #000;"></div>
                <h2 style="margin: 0; padding: 0 1em; width: fit-content;">{date_str}</h2>
                <div style="flex: 1; border-bottom: 1px solid #000; border-top: 1px solid #000;"></div>
            </div>
            """
            day += 1
        body += 3*TAB + make_button(place) + "\n"
    return body

def norway_to_israel(location):
    # Roughly translate Norway coordinates from Norway to Israel
    lat, lon = location
    new_lat = 31.8483 + (lat - 60.0) * 0.7
    new_lon = 35.1037 + (lon - 10.0) * 0.1
    return [new_lat, new_lon]

def make_debug():
    global title
    title = "מדריך טיולים גרסת פיתוח"
    for i in range(len(places)):
        places[i]['location'] = norway_to_israel(places[i]['location'])
        for j in range(len(places[i]['verify_locations'])):
            places[i]['verify_locations'][j] = norway_to_israel(
                places[i]['verify_locations'][j])
            places[i]['verify_dists_km'][j] /= 3
    places[0]['location'] = [31.77887959177701, 35.20774504578961]
    places[1]['location'] = [31.971300393037957, 34.77591912416341]

def plot_route(places):
    # plots route from each point to the next, on google maps, by car
    
    base_url = "https://www.google.com/maps/dir/"
    urls = []
    _places = [place0] + places
    for i in range(len(_places)-1):
        start = _places[i]['location']
        end = _places[i+1]['location']
        url = f"https://www.google.com/maps/dir/{start[0]},{start[1]}/{end[0]},{end[1]}/" \
               "@60.368077,9.5150572,8z/data=!4m2!4m1!3e0"
        urls.append(url)

    for url in urls[::-1]:
        webbrowser.open(url)
        time.sleep(0.1)
              
def make_html():
    template = get_template()
    body = make_body(places)
    final_html = template.replace("{{BODY}}", body)
    htmlfile = write_index_html(final_html)
    return htmlfile
    
if __name__ == "__main__":
    process_places()
    if DEBUG:
        make_debug()
        
    htmlfile = make_html()

    # validate_word()
    # open_html(htmlfile)
    plot_places(places, overview_only=True)
    # plot_route(places)
    
    print("done")