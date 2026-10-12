"""Generate plausible fake social accounts and apps for any brand."""
import random

HOMOGLYPHS = {
    'a': ['4', '@'], 'e': ['3'], 'i': ['1', 'l'], 'o': ['0'],
    's': ['5', '$'], 'l': ['1', 'i'], 'g': ['9'], 'b': ['8'], 't': ['7'],
    'u': ['v'], 'm': ['rn', 'nn'], 'n': ['m'], 'r': ['n'],
}


def _homoglyph_variant(name: str) -> str:
    """Swap one character with a look-alike."""
    if not name:
        return name
    idxs = [i for i, c in enumerate(name.lower()) if c in HOMOGLYPHS]
    if not idxs:
        return name
    i = random.choice(idxs)
    c = name[i].lower()
    sub = random.choice(HOMOGLYPHS[c])
    return name[:i] + sub + name[i + 1:]


def _add_word_variant(name: str) -> str:
    suffixes = ["Official", "Support", "Help", "Team", "Care", "Service",
                "Deals", "Offers", "Rewards", "Bonus", "India", "Global"]
    return f"{name} {random.choice(suffixes)}"


def _spacing_variant(name: str) -> str:
    if len(name) < 4:
        return name
    i = random.randint(1, len(name) - 2)
    return name[:i] + " " + name[i:]


def _typo_variant(name: str) -> str:
    if len(name) < 3:
        return name
    i = random.randint(0, len(name) - 1)
    return name[:i] + name[i + 1:]


def generate_social_accounts(brand: str, count: int = 6):
    """Generate a list of fake social accounts mixing good and bad ones."""
    brand_l = brand.strip()
    if not brand_l:
        brand_l = "brand"
    handle = brand_l.lower().replace(" ", "")

    candidates = [
        # Official (should NOT be flagged)
        {"name": brand_l, "handle": f"twitter:{handle}",
         "logo_path": "", "is_official": True},
        # Homoglyph
        {"name": _homoglyph_variant(brand_l), "handle": f"twitter:{handle}_1",
         "logo_path": ""},
        # Added word
        {"name": _add_word_variant(brand_l), "handle": f"twitter:{handle}_off",
         "logo_path": ""},
        # Spacing
        {"name": _spacing_variant(brand_l), "handle": f"instagram:{handle}_sp",
         "logo_path": ""},
        # Typo
        {"name": _typo_variant(brand_l), "handle": f"twitter:{handle}_typo",
         "logo_path": ""},
        # Unrelated (should NOT be flagged)
        {"name": "Random Tech News", "handle": "twitter:technews",
         "logo_path": ""},
    ]
    return candidates[:count]


def generate_apps(brand: str, count: int = 5):
    brand_l = brand.strip()
    if not brand_l:
        brand_l = "brand"
    handle = brand_l.lower().replace(" ", "")

    candidates = [
        {"name": brand_l, "package": f"com.{handle}.official",
         "publisher": f"{brand_l} Inc", "logo_path": "", "is_official": True},
        {"name": _add_word_variant(brand_l), "package": f"com.fake.{handle}pro",
         "publisher": "UnknownDev", "logo_path": ""},
        {"name": _homoglyph_variant(brand_l) + " Wallet",
         "package": f"com.x.{handle}1", "publisher": "xDev", "logo_path": ""},
        {"name": f"{brand_l} Cash Bonus", "package": f"com.scam.{handle}",
         "publisher": "FastMoney", "logo_path": ""},
        {"name": "Notes App", "package": "com.notes.app",
         "publisher": "NiceDev", "logo_path": ""},
    ]
    return candidates[:count]
