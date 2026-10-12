import os
import re
from rapidfuzz import fuzz

# ---------- Homoglyph / look-alike mapping ----------
HOMOGLYPHS = {
    'a': ['a', '4', '@'],
    'e': ['e', '3'],
    'i': ['i', '1', 'l', '!'],
    'o': ['o', '0'],
    's': ['s', '5', '$'],
    'l': ['l', '1', 'i'],
    'g': ['g', '9'],
    'b': ['b', '8'],
    't': ['t', '7'],
}

THREAT_THRESHOLD = 80.0

# ---------- Optional image hashing ----------
try:
    import imagehash
    from PIL import Image
    HAS_IMAGEHASH = True
except ImportError:
    HAS_IMAGEHASH = False


def normalize(text: str) -> str:
    return re.sub(r'[^a-z0-9]', '', (text or '').lower())


def generate_lookalikes(name: str) -> set:
    n = normalize(name)
    variants = {n}
    for i, ch in enumerate(n):
        if ch in HOMOGLYPHS:
            for sub in HOMOGLYPHS[ch]:
                variants.add(n[:i] + sub + n[i + 1:])
    return variants


def name_similarity(candidate: str, brand: str) -> float:
    c, b = normalize(candidate), normalize(brand)
    if not c or not b:
        return 0.0
    if c == b:
        return 100.0
    if b in c:
        return 90.0
    if c in generate_lookalikes(brand):
        return 95.0
    return float(fuzz.ratio(c, b))


def compute_phash(image_path: str):
    if not HAS_IMAGEHASH or not image_path or not os.path.exists(image_path):
        return None
    try:
        with Image.open(image_path) as img:
            return imagehash.phash(img)
    except Exception:
        return None


def compare_logos(path1: str, path2: str) -> float:
    """Return 0-100 similarity between two logo files via pHash."""
    h1 = compute_phash(path1)
    h2 = compute_phash(path2)
    if h1 is None or h2 is None:
        return 0.0
    distance = int(h1 - h2)
    max_bits = 64.0
    return float(max(0.0, (1 - distance / max_bits) * 100))


def classify(candidate_name: str,
             brand: str,
             candidate_handle: str = "",
             official_handles: list = None,
             logo_score: float = 0.0) -> dict:
    official_handles = official_handles or []

    if candidate_handle and candidate_handle in official_handles:
        return {
            "is_threat": False,
            "reason": "Official account",
            "score": 0.0,
            "name_score": 0.0,
            "logo_score": 0.0,
        }

    name_score = float(name_similarity(candidate_name, brand))
    logo_score = float(logo_score)
    combined = float(max(name_score, logo_score))
    is_threat = bool(combined >= THREAT_THRESHOLD)

    if name_score >= 95:
        reason = "Homoglyph / look-alike name"
    elif name_score >= 90:
        reason = "Similar name (added words / partial match)"
    elif name_score >= THREAT_THRESHOLD:
        reason = "Fuzzy name match"
    elif logo_score >= THREAT_THRESHOLD:
        reason = "Logo impersonation"
    else:
        reason = "Below threshold"

    return {
        "is_threat": is_threat,
        "name_score": float(round(name_score, 1)),
        "logo_score": float(round(logo_score, 1)),
        "score": float(round(combined, 1)),
        "reason": reason,
    }
