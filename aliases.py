
import unicodedata

CANONICAL_BRANDS = [
    "Rick Owens","Chrome Hearts","Maison Martin Margiela","Saint Laurent","Saint Laurent Paris",
    "Dior","Dior Homme","Undercover","Balenciaga","Raf Simons","Comme des Garçons",
    "Yohji Yamamoto","Issey Miyake","Bottega Veneta","Givenchy","Gucci","Tom Ford",
    "Jean Paul Gaultier","Chanel","Dolce & Gabbana","Miu Miu","Prada","Celine","Dsquared2",
    "Balmain","Enfants Riches Déprimés","Visvim","Number (N)ine","Ann Demeulemeester","Julius",
    "Guidi","Helmut Lang","Dries Van Noten","Jil Sander","Alexander McQueen","Loewe","Marni",
    "Acne Studios","Lemaire","The Row","Off-White","Vetements","Stone Island","C.P. Company",
    "Acronym","Kapital","Needles","Sacai","Cav Empt","Maison Kitsuné","AMI Paris"
]

BRAND_ALIASES = {
    "Rick Owens": ["rick","ro","drkshdw","geobasket","ramones"],
    "Chrome Hearts": ["ch","chromehearts","クロムハーツ"],
    "Maison Martin Margiela": ["maison margiela","margiela","mmm","mm6"],
    "Saint Laurent": ["saint laurent paris","slp","ysl"],
    "Dior": ["christian dior"],
    "Dior Homme": ["dior","hedi dior","he dior"],
    "Undercover": ["uc","アンダーカバー"],
    "Comme des Garçons": ["comme des garcons","cdg","comme"],
    "Issey Miyake": ["homme plissé","homme plisse","pleats please","apoc","issey"],
    "Alexander McQueen": ["mcqueen"],
    "C.P. Company": ["cp company","cpco"],
    "Acronym": ["acrnm","acronym"],
    "Enfants Riches Déprimés": ["enfants riches deprimes","erd"],
    "Dolce & Gabbana": ["d&g","dolce gabbana","dolce and gabbana"],
    # sensible fallbacks
    "Yohji Yamamoto": ["yohji","yy","ヨウジヤマモト"],
    "Raf Simons": ["rs","raf"],
    "Helmut Lang": ["hl","helmut"],
    "Julius": ["nilø","julius_7","ユリウス"],
    "Guidi": ["guidi 988","guidi boots"],
    "Ann Demeulemeester": ["ann d","ademeulemeester"],
    "Visvim": ["fbt","virgil","vis vim","ヴィズヴィム"],
    "Kapital": ["kountry","k apital","キャピタル"],
    "Needles": ["track pants","蝶","ネペンテス"],
    "Sacai": ["サカイ"],
    "Cav Empt": ["c.e","cev","キャブエンプト"],
    "Maison Kitsuné": ["kitsune","キツネ"],
    "AMI Paris": ["ami","alexandre mattiussi"],
}

def _strip_diacritics(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))

def normalize(text: str) -> str:
    return _strip_diacritics(unicodedata.normalize('NFKC', text)).lower()

def match_brand(text: str):
    t = normalize(text)
    for brand in CANONICAL_BRANDS:
        if normalize(brand) in t:
            return brand
        for alias in BRAND_ALIASES.get(brand, []):
            if normalize(alias) in t:
                return brand
    return None
