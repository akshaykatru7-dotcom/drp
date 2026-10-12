from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class BrandProfile:
    brand_name: str
    official_logo_path: str = ""
    official_socials: List[str] = field(default_factory=list)
    official_apps: List[str] = field(default_factory=list)
    identifiers: List[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


CURRENT_PROFILE = BrandProfile(
    brand_name="PayPal",
    official_logo_path="logos/official_paypal.png",
    official_socials=["twitter:paypal", "instagram:paypal", "facebook:paypal"],
    official_apps=["com.paypal.android.p2pmobile"],
    identifiers=["paypal.com", "paypal.me"],
)


def get_profile() -> BrandProfile:
    return CURRENT_PROFILE


def set_profile(new_profile: BrandProfile) -> None:
    global CURRENT_PROFILE
    CURRENT_PROFILE = new_profile
