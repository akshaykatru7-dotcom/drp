import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

from models import BrandProfile, get_profile, set_profile
from detection import classify, compare_logos
from brand_generator import generate_social_accounts, generate_apps

app = FastAPI(title="Digital Risk Protection Platform")

OFFICIAL_LOGO_PATH = "logos/official_paypal.png"


class BrandInput(BaseModel):
    brand_name: str
    official_socials: List[str] = []
    official_apps: List[str] = []
    identifiers: List[str] = []


class CustomCandidate(BaseModel):
    name: str
    handle: str = ""
    logo_path: str = ""


@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


@app.get("/api/brand")
def api_get_brand():
    return get_profile().to_dict()


@app.post("/api/brand")
def api_set_brand(payload: BrandInput):
    new_profile = BrandProfile(
        brand_name=payload.brand_name,
        official_socials=[s.strip() for s in payload.official_socials if s.strip()],
        official_apps=[a.strip() for a in payload.official_apps if a.strip()],
        identifiers=[i.strip() for i in payload.identifiers if i.strip()],
    )
    set_profile(new_profile)
    return {"ok": True, "profile": new_profile.to_dict()}


@app.get("/api/scan/social")
def scan_social():
    profile = get_profile()
    brand = profile.brand_name or "brand"
    candidates = generate_social_accounts(brand, count=6)
    brand_handle = brand.lower().replace(" ", "")
    auto_officials = set(profile.official_socials)
    auto_officials.add(f"twitter:{brand_handle}")

    results = []
    for acc in candidates:
        if acc.get("is_official"):
            results.append({
                **acc,
                "is_threat": False, "score": 0.0,
                "name_score": 0.0, "logo_score": 0.0,
                "reason": "Official account",
            })
            continue

        if brand.lower() == "paypal":
            logo_score = compare_logos(OFFICIAL_LOGO_PATH, acc.get("logo_path", ""))
        else:
            logo_score = 0.0

        verdict = classify(
            candidate_name=acc["name"], brand=brand,
            candidate_handle=acc["handle"],
            official_handles=list(auto_officials),
            logo_score=logo_score,
        )
        results.append({**acc, **verdict})

    return sorted(results, key=lambda r: r["score"], reverse=True)


@app.get("/api/scan/apps")
def scan_apps():
    profile = get_profile()
    brand = profile.brand_name or "brand"
    candidates = generate_apps(brand, count=5)
    brand_handle = brand.lower().replace(" ", "")
    auto_officials = set(profile.official_apps)
    auto_officials.add(f"com.{brand_handle}.official")

    results = []
    for app_data in candidates:
        if app_data.get("is_official"):
            results.append({
                **app_data,
                "is_threat": False, "score": 0.0,
                "name_score": 0.0, "logo_score": 0.0,
                "reason": "Official account",
            })
            continue

        if brand.lower() == "paypal":
            logo_score = compare_logos(OFFICIAL_LOGO_PATH, app_data.get("logo_path", ""))
        else:
            logo_score = 0.0

        verdict = classify(
            candidate_name=app_data["name"], brand=brand,
            candidate_handle=app_data["package"],
            official_handles=list(auto_officials),
            logo_score=logo_score,
        )
        if (app_data["publisher"].lower() not in brand.lower()
                and verdict["is_threat"]):
            verdict["reason"] += " + suspicious publisher"
        results.append({**app_data, **verdict})

    return sorted(results, key=lambda r: r["score"], reverse=True)


@app.post("/api/scan/custom")
def scan_custom(payload: CustomCandidate):
    profile = get_profile()
    brand = profile.brand_name or "brand"

    logo_score = 0.0
    if brand.lower() == "paypal":
        logo_score = compare_logos(OFFICIAL_LOGO_PATH, payload.logo_path or "")

    verdict = classify(
        candidate_name=payload.name, brand=brand,
        candidate_handle=payload.handle,
        official_handles=profile.official_socials,
        logo_score=logo_score,
    )
    return {
        "candidate": {
            "name": payload.name,
            "handle": payload.handle,
            "logo_path": payload.logo_path,
        },
        "brand": brand,
        "verdict": verdict,
    }


class AISummaryRequest(BaseModel):
    threats: List[dict] = []
    brand: str = ""


@app.post("/api/ai-summary")
def ai_summary(payload: AISummaryRequest):
    if not groq_client:
        return {"ok": False, "error": "GROQ_API_KEY not configured", "summary": ""}

    if not payload.threats:
        return {"ok": True, "summary": "No threats detected. The brand appears safe across monitored sources."}

    # Build a compact threat description for the prompt
    threat_lines = []
    for t in payload.threats[:15]:  # cap to avoid huge prompts
        line = f"- {t.get('name','?')} (handle: {t.get('handle') or t.get('package','?')}) | score: {t.get('score')} | reason: {t.get('reason','')}"
        threat_lines.append(line)

    threats_text = "\n".join(threat_lines)

    prompt = f"""You are a security analyst assistant. A Digital Risk Protection platform has flagged the following threats against the brand "{payload.brand}":

{threats_text}

Write a concise 3-5 sentence summary for a security analyst. Cover:
1. How many threats and what types (homoglyph, added-word, logo, publisher mismatch, etc.)
2. Which is highest priority and why
3. One recommended next action

Tone: professional, direct, no fluff. Do not use bullet points — write as flowing prose."""

    try:
        completion = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300,
        )
        summary = completion.choices[0].message.content.strip()
        return {"ok": True, "summary": summary}
    except Exception as e:
        return {"ok": False, "error": str(e), "summary": ""}
