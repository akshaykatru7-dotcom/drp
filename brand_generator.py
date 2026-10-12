"""Generate plausible fake social accounts and apps for any brand."""
import random

HOMOGLYPHS = {
    'a': ['4', '@'], 'e': ['3'], 'i': ['1', 'l'], 'o': ['0'],
    's': ['5', '$'], 'l': ['1', 'i'], 'g': ['9'], 'b': ['8'], 't': ['7'],
    'u': ['v'], 'm': ['rn', 'nn'], 'n': ['m'], 'r': ['n'],
}

# Available demo logo fixtures
LOGO_FIXTURES = [
    "logos/official_paypal.png",           # identical → very high score
    "logos/fake_paypa1_identical.png",     # identical → very high
    "logos/fake_paypal_shade.png",         # slight shade → ~97
    "logos/fake_paypal_pro.png",           # different → ~85
    "logos/fake_paypal_dark.png",          # dark → ~70
    "logos/unrelated_notes.png",           # unrelated → low
]


def _homoglyph_variant(name: str) -> str:
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


def _fuzzy_variant(name: str) -> str:
    """Slight misspelling → triggers fuzzy but not homoglyph."""
    if len(name) < 4:
        return name
    swaps = [("ph", "pp"), ("ll", "l"), ("tt", "t"), ("ss", "s")]
    for old, new in swaps:
        if old in name.lower():
            return name.lower().replace(old, new, 1).title()
    # fallback: swap two adjacent chars
    i = random.randint(0, len(name) - 2)
    return name[:i] + name[i + 1] + name[i] + name[i + 2:]


def generate_social_accounts(brand: str, count: int = 6):
    brand_l = brand.strip() or "brand"
    handle = brand_l.lower().replace(" ", "")

    candidates = [
        {"name": brand_l, "handle": f"twitter:{handle}",
         "logo_path": LOGO_FIXTURES[0], "is_official": True},
        {"name": _homoglyph_variant(brand_l), "handle": f"twitter:{handle}_1",
         "logo_path": LOGO_FIXTURES[1]},                       # homoglyph + identical logo
        {"name": _add_word_variant(brand_l), "handle": f"twitter:{handle}_off",
         "logo_path": LOGO_FIXTURES[2]},                       # added-word + shaded logo
        {"name": _spacing_variant(brand_l), "handle": f"instagram:{handle}_sp",
         "logo_path": LOGO_FIXTURES[3]},                       # spacing + pro logo
        {"name": _fuzzy_variant(brand_l), "handle": f"twitter:{handle}_typo",
         "logo_path": LOGO_FIXTURES[4]},                       # fuzzy + dark logo
        {"name": "Random Tech News", "handle": "twitter:technews",
         "logo_path": LOGO_FIXTURES[5]},                       # unrelated → safe
    ]
    return candidates[:count]


def generate_apps(brand: str, count: int = 5):
    brand_l = brand.strip() or "brand"
    handle = brand_l.lower().replace(" ", "")

    candidates = [
        {"name": brand_l, "package": f"com.{handle}.official",
         "publisher": f"{brand_l} Inc",
         "logo_path": LOGO_FIXTURES[0], "is_official": True},
        {"name": _add_word_variant(brand_l), "package": f"com.fake.{handle}pro",
         "publisher": "UnknownDev", "logo_path": LOGO_FIXTURES[2]},
        {"name": _homoglyph_variant(brand_l) + " Wallet",
         "package": f"com.x.{handle}1", "publisher": "xDev",
         "logo_path": LOGO_FIXTURES[1]},
        {"name": f"{brand_l} Cash Bonus", "package": f"com.scam.{handle}",
         "publisher": "FastMoney", "logo_path": LOGO_FIXTURES[3]},
        {"name": "Notes App", "package": "com.notes.app",
         "publisher": "NiceDev", "logo_path": LOGO_FIXTURES[5]},
    ]
    return candidates[:count]
