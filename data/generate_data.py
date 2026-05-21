import random
from pathlib import Path

import numpy as np
import pandas as pd


def generate_marketing_data(n_rows: int = 500, export_path: Path | str | None = None) -> pd.DataFrame:
    """Generate realistic marketing campaign data with intentional underperformers."""
    random.seed(42)
    np.random.seed(42)

    platforms = ["Meta", "Google", "LinkedIn"]
    audience_segments = [
        "Tech Bros 25-34",
        "Soccer Moms",
        "Enterprise Leaders",
        "Budget Shoppers 45-54",
        "Fitness Fanatics 18-24",
        "Retail Professionals",
        "Healthcare Buyers",
        "Financial Planners",
        "Education Decision Makers",
    ]
    creatives = [
        "Growth Accelerator",
        "Performance Playbook",
        "Conversion Booster",
        "Sales Funnel Refresh",
        "Lead Magnet Pulse",
        "Audience Expansion",
        "Smart Offers",
    ]

    data = []
    for i in range(1, n_rows + 1):
        platform = random.choice(platforms)
        audience = random.choice(audience_segments)
        creative_name = random.choice(creatives)

        base_spend = random.uniform(300, 2500)
        impressions = random.randint(8000, 120000)
        ctr = random.uniform(0.0025, 0.06)
        clicks = int(impressions * ctr)
        conversion_rate = random.uniform(0.01, 0.15)
        conversions = max(1, int(clicks * conversion_rate))

        if audience in ["Soccer Moms", "Budget Shoppers 45-54", "Fitness Fanatics 18-24"]:
            ctr *= random.uniform(0.25, 0.6)
            conversions = max(1, int(clicks * random.uniform(0.005, 0.03)))
            base_spend *= random.uniform(1.15, 1.8)

        spend = round(base_spend, 2)
        cpa = round(spend / conversions, 2)
        roas = round((conversions * random.uniform(30, 125)) / spend, 2)

        data.append(
            {
                "Campaign ID": f"CMP-{1000 + i}",
                "Platform": platform,
                "Audience Segment": audience,
                "Ad Creative Name": creative_name,
                "Spend ($)": spend,
                "Impressions": impressions,
                "Clicks": clicks,
                "Conversions": conversions,
                "CTR": round(clicks / impressions, 4),
                "CPA": cpa,
                "ROAS": roas,
            }
        )

    df = pd.DataFrame(data)

    if export_path is not None:
        export_path = Path(export_path)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(export_path, index=False)

    return df


if __name__ == "__main__":
    df = generate_marketing_data(n_rows=500, export_path=Path("data/marketing_campaigns.xlsx"))
    print("Generated marketing data and exported to data/marketing_campaigns.xlsx")
