# ============================================================
# STYLIST AGENT PACKAGE
# ============================================================

from .Scoring.occasion import (
    calculate_occasion_score,
    calculate_item_occasion_score
)

from .Scoring.preferences import (
    calculate_preference_score,
    calculate_temporal_preference_score
)

from .Scoring.weather import (
    calculate_weather_score
)

from .Scoring.outfit_scorer import (
    score_outfits
)

from .Reason.reasons import (
    generate_outfit_reason
)

from .agent import (
    run_stylist_agent
)

from .Scoring.diversity import (
    select_diverse_outfits,
    calculate_outfit_similarity,
    calculate_diversity_summary
)

__all__ = [
    "calculate_occasion_score",
    "calculate_item_occasion_score",
    "calculate_preference_score",
    "calculate_temporal_preference_score",
    "calculate_weather_score",
    "score_outfits",
    "generate_outfit_reason",
    "run_stylist_agent"
]