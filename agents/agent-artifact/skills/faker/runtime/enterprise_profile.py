"""
Enterprise profile — declarative demographic and product configuration
for tailoring synthetic data to a specific enterprise's characteristics.

Pass an EnterpriseProfile to any factory or DatasetBuilder to weight
geographic, demographic, and product-catalogue fields toward the
enterprise's actual distribution rather than uniform-random values.

Dependencies: Python stdlib only (random, dataclasses, typing)
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import date
from typing import Optional


# ─── Core data classes ────────────────────────────────────────────────────────

@dataclass
class AgeBand:
    """A contiguous age bracket with a relative sampling weight."""
    min_age: int
    max_age: int
    weight: float


@dataclass
class ProductSpec:
    """
    A single product in the enterprise catalogue.

    weight:                  relative probability of selecting this product
    value_range:             (low, high) for balance / premium / limit fields
    currency:                ISO 4217 code for monetary fields on this product
    eligible_customer_types: empty list means all types are eligible
    """
    name: str
    code: str
    weight: float
    value_range: tuple[float, float] = (0.0, 10_000.0)
    currency: str = "USD"
    eligible_customer_types: list[str] = field(default_factory=list)


@dataclass
class EnterpriseProfile:
    """
    Declarative configuration that shapes synthetic data to match an
    enterprise's actual demographic mix and product portfolio.

    All weight values are relative — they do not need to sum to 1.0.
    You may express them as percentages, ratios, or raw counts.

    geo_weights:            {faker_locale: weight}
                            Faker locale codes, e.g. "en_GB", "ja_JP", "es_MX".
                            Drives per-record Faker locale and country/region fields.

    age_bands:              Weighted list of AgeBand objects.
                            Drives date_of_birth / age fields.

    customer_type_weights:  {type_value: weight}
                            Drives customer_type / party_type / entity_type fields.
                            Values should match domain enum entries.

    products:               Ordered catalogue of ProductSpec objects.
                            Drives product_code, product_name, amount, balance,
                            premium, limit, and currency fields.

    sector_weights:         {sector_value: weight}
                            Optional — B2B / commercial domains only.
                            Drives industry / sector fields.
    """

    geo_weights: dict[str, float] = field(
        default_factory=lambda: {"en_US": 1.0}
    )
    age_bands: list[AgeBand] = field(
        default_factory=lambda: [
            AgeBand(18, 34, 1.0),
            AgeBand(35, 54, 1.0),
            AgeBand(55, 80, 1.0),
        ]
    )
    customer_type_weights: dict[str, float] = field(
        default_factory=lambda: {"Individual": 1.0}
    )
    products: list[ProductSpec] = field(default_factory=list)
    sector_weights: dict[str, float] = field(default_factory=dict)

    # ── Sampling helpers ──────────────────────────────────────────────────────

    def sample_locale(self) -> str:
        """Return a Faker locale sampled from geo_weights."""
        return _weighted_choice(self.geo_weights)

    def sample_country(self) -> str:
        """
        Return an ISO 3166-1 alpha-2 country code derived from the sampled locale.
        For locales like 'en_GB' the suffix is used; for bare codes like 'es' a
        best-effort mapping is applied.
        """
        locale = self.sample_locale()
        parts = locale.split("_")
        if len(parts) >= 2:
            return parts[-1].upper()
        # bare locale codes — map to primary country
        _bare = {"en": "US", "es": "ES", "fr": "FR", "de": "DE",
                 "zh": "CN", "ja": "JP", "ko": "KR", "pt": "BR"}
        return _bare.get(parts[0], parts[0].upper())

    def sample_age(self) -> int:
        """Return an age (integer years) sampled from age_bands."""
        band: AgeBand = _weighted_choice_list(
            [(b, b.weight) for b in self.age_bands]
        )
        return random.randint(band.min_age, band.max_age)

    def sample_date_of_birth(self) -> date:
        """Return a date-of-birth derived from sample_age()."""
        age = self.sample_age()
        today = date.today()
        try:
            dob = today.replace(year=today.year - age)
        except ValueError:
            # 29 Feb edge case
            dob = today.replace(year=today.year - age, day=28)
        return dob

    def sample_customer_type(self) -> str:
        """Return a customer / party type sampled from customer_type_weights."""
        return _weighted_choice(self.customer_type_weights)

    def sample_sector(self) -> Optional[str]:
        """Return a sector / industry value, or None if sector_weights is empty."""
        if not self.sector_weights:
            return None
        return _weighted_choice(self.sector_weights)

    def sample_product(
        self, customer_type: Optional[str] = None
    ) -> Optional[ProductSpec]:
        """
        Return a ProductSpec sampled from the catalogue.

        When customer_type is supplied, only products whose
        eligible_customer_types list is empty (all types) or contains
        the supplied type are considered.
        """
        if not self.products:
            return None
        eligible = [
            p for p in self.products
            if not p.eligible_customer_types
            or (customer_type and customer_type in p.eligible_customer_types)
        ]
        if not eligible:
            eligible = self.products  # fall back to full catalogue
        return _weighted_choice_list([(p, p.weight) for p in eligible])

    def sample_amount(
        self,
        product: Optional[ProductSpec] = None,
        fallback_range: tuple[float, float] = (1.0, 50_000.0),
    ) -> float:
        """Return a monetary amount within the product's value_range, or fallback."""
        lo, hi = product.value_range if product else fallback_range
        return round(random.uniform(lo, hi), 2)

    def sample_currency(
        self,
        product: Optional[ProductSpec] = None,
        fallback: str = "USD",
    ) -> str:
        """Return the currency from the product spec, or fallback."""
        return product.currency if product else fallback


# ─── Internal helpers ──────────────────────────────────────────────────────────

def _weighted_choice(weights: dict[str, float]) -> str:
    keys = list(weights)
    w = [weights[k] for k in keys]
    total = sum(w)
    r = random.uniform(0, total)
    cumulative = 0.0
    for key, weight in zip(keys, w):
        cumulative += weight
        if r <= cumulative:
            return key
    return keys[-1]


def _weighted_choice_list(items: list[tuple]) -> object:
    total = sum(w for _, w in items)
    r = random.uniform(0, total)
    cumulative = 0.0
    for item, weight in items:
        cumulative += weight
        if r <= cumulative:
            return item
    return items[-1][0]


# ─── Pre-built enterprise profiles ────────────────────────────────────────────
# Use the closest profile as a starting point, then copy and adjust weights
# and product specs to match the actual enterprise.


def uk_retail_bank_profile() -> EnterpriseProfile:
    """
    Mid-size UK retail bank.

    Demographics: predominantly UK customers, broad age range, mostly
    individual accounts with a small sole-trader and SME book.
    Products: GBP-denominated; current account, savings, mortgage,
    personal loan, credit card, and business current account.
    """
    return EnterpriseProfile(
        geo_weights={
            "en_GB": 75,
            "en_IE": 10,
            "fr_FR":  8,
            "de_DE":  7,
        },
        age_bands=[
            AgeBand(18, 24,  8),
            AgeBand(25, 34, 20),
            AgeBand(35, 44, 22),
            AgeBand(45, 54, 22),
            AgeBand(55, 64, 18),
            AgeBand(65, 80, 10),
        ],
        customer_type_weights={
            "Individual":   82,
            "Sole Trader":  10,
            "SME":           8,
        },
        products=[
            ProductSpec(
                "Current Account", "CA",
                weight=60, value_range=(0, 15_000), currency="GBP",
            ),
            ProductSpec(
                "Savings Account", "SA",
                weight=35, value_range=(500, 80_000), currency="GBP",
            ),
            ProductSpec(
                "Mortgage", "MTG",
                weight=20, value_range=(50_000, 500_000), currency="GBP",
                eligible_customer_types=["Individual", "Sole Trader"],
            ),
            ProductSpec(
                "Personal Loan", "PL",
                weight=15, value_range=(1_000, 25_000), currency="GBP",
                eligible_customer_types=["Individual"],
            ),
            ProductSpec(
                "Credit Card", "CC",
                weight=25, value_range=(0, 10_000), currency="GBP",
            ),
            ProductSpec(
                "Business Current Account", "BCA",
                weight=100, value_range=(1_000, 200_000), currency="GBP",
                eligible_customer_types=["Sole Trader", "SME"],
            ),
        ],
    )


def us_fintech_profile() -> EnterpriseProfile:
    """
    US digital-first fintech (neobank / BNPL).

    Demographics: young urban skew, predominantly US with a Spanish-speaking
    and Chinese-American segment; almost entirely individual accounts with a
    small small-business cohort.
    Products: USD-denominated; checking, savings, BNPL credit, and debit card.
    """
    return EnterpriseProfile(
        geo_weights={
            "en_US": 88,
            "es_US":  8,
            "zh_CN":  4,
        },
        age_bands=[
            AgeBand(18, 24, 25),
            AgeBand(25, 34, 40),
            AgeBand(35, 44, 25),
            AgeBand(45, 54,  8),
            AgeBand(55, 70,  2),
        ],
        customer_type_weights={
            "Individual":     95,
            "Small Business":  5,
        },
        products=[
            ProductSpec(
                "Checking Account", "CHK",
                weight=90, value_range=(0, 5_000), currency="USD",
            ),
            ProductSpec(
                "Savings Account", "SAV",
                weight=40, value_range=(100, 20_000), currency="USD",
            ),
            ProductSpec(
                "BNPL Credit", "BNPL",
                weight=30, value_range=(50, 3_000), currency="USD",
                eligible_customer_types=["Individual"],
            ),
            ProductSpec(
                "Debit Card", "DC",
                weight=85, value_range=(0, 5_000), currency="USD",
            ),
            ProductSpec(
                "Business Account", "BIZ",
                weight=100, value_range=(500, 50_000), currency="USD",
                eligible_customer_types=["Small Business"],
            ),
        ],
    )


def apac_insurance_profile() -> EnterpriseProfile:
    """
    Regional APAC insurer — multi-market across Australia, Taiwan, Japan,
    South Korea, and Singapore.

    Demographics: mid-career skew (30–59), individual-dominant with a
    corporate group book.
    Products: life, health, home & contents, motor (individual); group life
    and corporate health (corporate). Values expressed in AUD; adjust
    currency per-record if multi-currency is required.
    """
    return EnterpriseProfile(
        geo_weights={
            "en_AU": 35,
            "zh_TW": 20,
            "ja_JP": 20,
            "ko_KR": 15,
            "en_SG": 10,
        },
        age_bands=[
            AgeBand(18, 29, 15),
            AgeBand(30, 39, 25),
            AgeBand(40, 49, 28),
            AgeBand(50, 59, 22),
            AgeBand(60, 75, 10),
        ],
        customer_type_weights={
            "Individual": 90,
            "Corporate":  10,
        },
        products=[
            ProductSpec(
                "Life Insurance", "LIFE",
                weight=40, value_range=(50_000, 2_000_000), currency="AUD",
                eligible_customer_types=["Individual"],
            ),
            ProductSpec(
                "Health Insurance", "HLTH",
                weight=55, value_range=(1_200, 8_000), currency="AUD",
            ),
            ProductSpec(
                "Home & Contents", "HOME",
                weight=30, value_range=(300, 3_000), currency="AUD",
                eligible_customer_types=["Individual"],
            ),
            ProductSpec(
                "Motor Insurance", "MOTO",
                weight=35, value_range=(400, 2_500), currency="AUD",
                eligible_customer_types=["Individual"],
            ),
            ProductSpec(
                "Group Life", "GRPLIFE",
                weight=100, value_range=(100_000, 5_000_000), currency="AUD",
                eligible_customer_types=["Corporate"],
            ),
            ProductSpec(
                "Corporate Health", "GRPHLTH",
                weight=100, value_range=(5_000, 200_000), currency="AUD",
                eligible_customer_types=["Corporate"],
            ),
        ],
    )
