# ============================================================
# CLOSET-IQ - LLM OUTFIT RERANKER
# ============================================================

import json
import os
from typing import Any, Dict, List, Optional

from google import genai
from pydantic import BaseModel, Field


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "gemini-3.5-flash-lite"

MAX_CANDIDATES = 15
FINAL_OUTFIT_COUNT = 3


# ============================================================
# STRUCTURED OUTPUT SCHEMA
# ============================================================

class SelectedOutfit(BaseModel):

    candidate_id: str = Field(
        description=(
            "ID of the selected outfit candidate, "
            "for example C01."
        )
    )

    # --------------------------------------------------------
    # NEW:
    # Independent LLM contextual score.
    # This does NOT replace or modify the rule final_score.
    # --------------------------------------------------------

    llm_score: float = Field(
        ge=0,
        le=100,
        description=(
            "LLM contextual evaluation score from 0 to 100. "
            "This score is separate from the existing "
            "rule-based final_score."
        )
    )

    reason: str = Field(
        description=(
            "A concise explanation of why this outfit is a strong "
            "choice for the user's context."
        )
    )


class RerankerResponse(BaseModel):

    selected_outfits: List[SelectedOutfit] = Field(
        description="Exactly three selected outfit candidates."
    )


# ============================================================
# HELPER: CONVERT VALUES INTO JSON-SAFE DATA
# ============================================================

def _make_json_safe(value: Any) -> Any:
    """
    Recursively converts values into JSON-safe structures.

    This protects the LLM request from objects such as:
        - Pydantic models
        - dataclasses / custom objects
        - tuples / sets

    Normal dictionaries, lists, strings, numbers and booleans
    are preserved.
    """

    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, dict):
        return {
            str(key): _make_json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple, set)):
        return [_make_json_safe(item) for item in value]

    if hasattr(value, "model_dump"):
        return _make_json_safe(value.model_dump())

    if hasattr(value, "__dict__"):
        return _make_json_safe(vars(value))

    return str(value)


# ============================================================
# HELPER: COMPACT ONE WARDROBE ITEM
# ============================================================

def _compact_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Keeps only information useful to Gemini.

    IMPORTANT:
    FashionCLIP embeddings and other unnecessary database
    information are intentionally NOT sent to Gemini.
    """

    compact = {
        "id": item.get("id"),
        "name": item.get("name"),
        "category": item.get("category"),
        "color": item.get("color"),
        "pattern": item.get("pattern"),
        "fit": item.get("fit"),

        # Support current/older field naming safely.
        "style": item.get("style"),
        "styles": item.get("styles"),

        "season": item.get("season"),
        "seasons": item.get("seasons"),

        "occasion": item.get("occasion"),
        "occasions": item.get("occasions"),
    }

    # Remove empty values so we don't waste tokens.
    return {
        key: _make_json_safe(value)
        for key, value in compact.items()
        if value is not None
    }


# ============================================================
# HELPER: EXTRACT ITEMS FROM AN OUTFIT
# ============================================================

def _extract_outfit_items(
    outfit: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Supports the current dynamic outfit format:

        {
            "items": [...]
        }

    It also safely supports dictionary-based outfit structures
    if any older combination reaches this function.
    """

    items = outfit.get("items")

    if isinstance(items, list):
        return [
            _compact_item(item)
            for item in items
            if isinstance(item, dict)
        ]

    # --------------------------------------------------------
    # Compatibility fallback for older outfit structures
    # --------------------------------------------------------

    ignored_keys = {
        "occasion_score",
        "preference_score",
        "weather_score",
        "learned_preference_score",
        "color_compatibility_score",
        "final_score",
        "reasons",
        "llm_score",
        "llm_reason",
        "accessory",
        "accessories",
    }

    extracted_items = []

    for key, value in outfit.items():

        if key in ignored_keys:
            continue

        if not isinstance(value, dict):
            continue

        # Only treat dictionary values containing clothing-like
        # fields as wardrobe items.
        if (
            "id" in value
            or "category" in value
            or "color" in value
        ):
            extracted_items.append(_compact_item(value))

    return extracted_items


# ============================================================
# HELPER: COMPACT ONE OUTFIT CANDIDATE
# ============================================================

def _compact_candidate(
    outfit: Dict[str, Any],
    candidate_id: str,
) -> Dict[str, Any]:
    """
    Converts the real scored outfit into the compact structure
    sent to Gemini.

    Existing rule scores are preserved exactly.
    """

    return {
        "candidate_id": candidate_id,

        "items": _extract_outfit_items(outfit),

        "scores": {
            "occasion_score": outfit.get(
                "occasion_score"
            ),

            "preference_score": outfit.get(
                "preference_score"
            ),

            "weather_score": outfit.get(
                "weather_score"
            ),

            "learned_preference_score": outfit.get(
                "learned_preference_score"
            ),

            "color_compatibility_score": outfit.get(
                "color_compatibility_score"
            ),

            "final_score": outfit.get(
                "final_score"
            ),
        },
    }


# ============================================================
# HELPER: PREPARE CANDIDATES
# ============================================================

def _prepare_candidates(
    candidates: List[Dict[str, Any]]
) -> tuple[
    List[Dict[str, Any]],
    Dict[str, Dict[str, Any]]
]:
    """
    Creates temporary candidate IDs:

        C01
        C02
        ...
        C15

    and maps those temporary IDs back to the REAL outfit
    dictionaries.

    Gemini never receives authority over the real objects.
    """

    candidates = candidates[:MAX_CANDIDATES]

    compact_candidates = []
    candidate_map = {}

    for index, outfit in enumerate(
        candidates,
        start=1
    ):

        candidate_id = f"C{index:02d}"

        candidate_map[candidate_id] = outfit

        compact_candidates.append(
            _compact_candidate(
                outfit=outfit,
                candidate_id=candidate_id,
            )
        )

    return compact_candidates, candidate_map


# ============================================================
# HELPER: BUILD PROMPT
# ============================================================

def _build_prompt(
    compact_candidates: List[Dict[str, Any]],
    occasion: str,
    weather: Optional[Any],
    preferences: Optional[Any],
    learned_preferences: Optional[Any],
) -> str:
    """
    Creates the complete Gemini reranking prompt.

    Gemini receives:
        - requested occasion
        - weather
        - explicit preferences
        - learned preferences
        - up to 15 already-scored diverse candidates

    Gemini evaluates all supplied candidates and returns
    exactly three final recommendations.

    Each selected recommendation receives an independent
    contextual LLM score from 0 to 100.
    """

    context = {
        "occasion": occasion,

        "weather": _make_json_safe(
            weather
        ),

        "user_preferences": _make_json_safe(
            preferences
        ),

        "learned_preferences": _make_json_safe(
            learned_preferences
        ),

        "candidate_outfits": compact_candidates,
    }

    context_json = json.dumps(
        context,
        ensure_ascii=False,
        separators=(",", ":"),
        default=str,
    )

    prompt = f"""
You are the final outfit reranking component of Closet-IQ,
an intelligent wardrobe styling system.

The Closet-IQ rule engine has ALREADY:

1. generated valid outfit combinations,
2. evaluated occasion suitability,
3. evaluated explicit user preferences,
4. evaluated weather suitability,
5. evaluated learned preferences from feedback,
6. checked color compatibility,
7. calculated final rule-based scores,
8. filtered the candidates for diversity.

Your task is NOT to generate outfits.

Your task is to evaluate ALL supplied candidate outfits,
compare them using the complete context, and select the best
{FINAL_OUTFIT_COUNT} final recommendations.

For every selected outfit, you must also provide an
independent llm_score from 0 to 100.

The llm_score is a contextual LLM evaluation.

It is NOT the existing rule-based final_score.

Do NOT copy final_score and do NOT mathematically recalculate
the existing Closet-IQ rule formula.

Use the following importance guidelines when forming the
llm_score:

- Occasion appropriateness: approximately 30%
- Explicit user preference alignment: approximately 25%
- Weather practicality: approximately 15%
- Learned preference alignment: approximately 10%
- Overall outfit coherence and coordination: approximately 20%

These percentages describe the relative importance of the
contextual factors for your judgment. They are NOT a request
to reproduce the existing deterministic rule formula.

Use the complete supplied outfit information when evaluating
overall outfit coherence, including categories, colors,
patterns, fit, style and other supplied clothing attributes.

SCORING INTERPRETATION:

90-100:
Exceptional contextual match.

80-89:
Very strong contextual match.

70-79:
Good contextual match with some weaker factors.

60-69:
Reasonable contextual match.

Below 60:
Noticeable contextual weaknesses.

Evaluate and compare ALL supplied candidates before deciding
which three should be returned.

The three returned candidates should be the candidates you
judge strongest after considering both the supplied
rule-based evidence and your contextual evaluation.

IMPORTANT RULES:

- Select ONLY from the supplied candidate IDs.
- Never invent a candidate ID.
- Never invent clothing items.
- Never modify an outfit.
- Never modify any supplied rule-based score.
- Never combine items from different candidates.
- Select each candidate only once.
- Consider the requested occasion.
- Consider current weather information when available.
- Consider explicit user preferences when available.
- Consider learned preferences when available.
- Respect the existing rule-based scores as important evidence.
- Consider the outfit as a complete coordinated look.
- Do not simply select three outfits because they have the
  highest numerical final_score.
- Use the complete context to make the final comparison.
- Prefer recommendations that are individually strong while
  still giving the user useful choice among the final three.
- Give every selected candidate an llm_score from 0 to 100.
- The llm_score must represent your independent contextual
  evaluation of that candidate.
- Give one concise, user-friendly reason for each selection.
- The reason should explain important factors behind the
  selection.
- The reason must refer only to information actually supplied.
- Do not claim information that is not present in the context.

Return exactly {FINAL_OUTFIT_COUNT} selected outfits.

CLOSET-IQ CONTEXT:

{context_json}
"""

    return prompt.strip()


# ============================================================
# HELPER: RULE-BASED FALLBACK
# ============================================================

def _fallback_top_outfits(
    candidates: List[Dict[str, Any]],
    count: int = FINAL_OUTFIT_COUNT,
) -> List[Dict[str, Any]]:
    """
    Safe fallback.

    Candidates reaching this module are already sorted/scored
    by the existing Stylist Agent.

    Therefore, if Gemini fails, we simply preserve the first
    three rule-ranked candidates.

    No existing score is changed.

    Since Gemini was not successfully used, llm_score and
    llm_reason are both None.
    """

    fallback = []

    for outfit in candidates[:count]:

        fallback_outfit = dict(outfit)

        # ----------------------------------------------------
        # Gemini was not used successfully.
        # Therefore there is no valid LLM score/reason.
        # ----------------------------------------------------

        fallback_outfit["llm_score"] = None
        fallback_outfit["llm_reason"] = None

        fallback.append(
            fallback_outfit
        )

    return fallback


# ============================================================
# HELPER: VALIDATE GEMINI SELECTION
# ============================================================

def _validate_selection(
    response_data: RerankerResponse,
    candidate_map: Dict[str, Dict[str, Any]],
) -> bool:
    """
    Validates Gemini's response before trusting it.

    Checks:
        - exactly 3 candidates
        - no duplicate IDs
        - every ID exists
        - every llm_score is within 0-100
        - every selection has a reason
    """

    selections = (
        response_data.selected_outfits
    )

    # Must return exactly 3.
    if len(selections) != FINAL_OUTFIT_COUNT:
        return False

    selected_ids = [
        selection.candidate_id
        for selection in selections
    ]

    # No duplicates.
    if (
        len(set(selected_ids))
        != FINAL_OUTFIT_COUNT
    ):
        return False

    # Every ID must exist in our supplied candidate map.
    for candidate_id in selected_ids:

        if candidate_id not in candidate_map:
            return False

    # --------------------------------------------------------
    # NEW:
    # Every selection must contain a valid LLM score.
    # --------------------------------------------------------

    for selection in selections:

        if (
            selection.llm_score < 0
            or selection.llm_score > 100
        ):
            return False

    # Every selection must contain a reason.
    for selection in selections:

        if not selection.reason:
            return False

        if not selection.reason.strip():
            return False

    return True


# ============================================================
# MAIN FUNCTION
# ============================================================

def rerank_outfits(
    candidates: List[Dict[str, Any]],
    occasion: str,
    weather: Optional[Any] = None,
    preferences: Optional[Any] = None,
    learned_preferences: Optional[Any] = None,
) -> List[Dict[str, Any]]:
    """
    Reranks rule-based Closet-IQ outfit candidates using Gemini.

    Expected pipeline:

        existing scoring
              ↓
        diversity filtering
              ↓
        Top 15 candidates
              ↓
        rerank_outfits(...)
              ↓
        Gemini evaluates candidates
              ↓
        Gemini selects 3
              ↓
        validated real outfits
              ↓
        Top 3
        + existing rule final_score
        + llm_score
        + existing rule reasons
        + llm_reason

    If Gemini cannot be used, returns the existing
    rule-ranked Top 3.

    IMPORTANT:
    This function does NOT mutate the original candidate
    dictionaries.
    """

    # --------------------------------------------------------
    # 1. BASIC VALIDATION
    # --------------------------------------------------------

    if not candidates:
        return []

    # If fewer than or exactly 3 candidates exist,
    # Gemini does not need to rerank them.
    if len(candidates) <= FINAL_OUTFIT_COUNT:

        return _fallback_top_outfits(
            candidates,
            count=len(candidates),
        )

    # --------------------------------------------------------
    # 2. CHECK API KEY
    # --------------------------------------------------------

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        print(
            "[LLM RERANKER] GEMINI_API_KEY not found. "
            "Using rule-based fallback."
        )

        return _fallback_top_outfits(
            candidates
        )

    # --------------------------------------------------------
    # 3. PREPARE MAXIMUM 15 CANDIDATES
    # --------------------------------------------------------

    compact_candidates, candidate_map = (
        _prepare_candidates(
            candidates
        )
    )

    # --------------------------------------------------------
    # 4. BUILD COMPACT PROMPT
    # --------------------------------------------------------

    prompt = _build_prompt(
        compact_candidates=compact_candidates,
        occasion=occasion,
        weather=weather,
        preferences=preferences,
        learned_preferences=learned_preferences,
    )

    print(
        f"[LLM RERANKER] Candidates sent: "
        f"{len(compact_candidates)}"
    )

    print(
        f"[LLM RERANKER] Prompt characters: "
        f"{len(prompt)}"
    )

    # --------------------------------------------------------
    # 5. CALL GEMINI
    # --------------------------------------------------------

    try:

        client = genai.Client(
            api_key=api_key
        )

        response = client.interactions.create(
            model=MODEL_NAME,
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": (
                    RerankerResponse.model_json_schema()
                ),
            },
        )

        # ----------------------------------------------------
        # 6. PARSE STRUCTURED RESPONSE
        # ----------------------------------------------------

        if not response.output_text:

            raise ValueError(
                "Gemini returned an empty response."
            )

        parsed_response = (
            RerankerResponse.model_validate_json(
                response.output_text
            )
        )

        # ----------------------------------------------------
        # 7. VALIDATE THE MODEL'S SELECTION
        # ----------------------------------------------------

        if not _validate_selection(
            parsed_response,
            candidate_map,
        ):

            raise ValueError(
                "Gemini returned invalid candidate selections."
            )

        # ----------------------------------------------------
        # 8. MAP IDs BACK TO REAL OUTFITS
        # ----------------------------------------------------

        final_outfits = []

        for selection in (
            parsed_response.selected_outfits
        ):

            real_outfit = candidate_map[
                selection.candidate_id
            ]

            # Copy so original scored outfit is not mutated.
            final_outfit = dict(
                real_outfit
            )

            # ------------------------------------------------
            # NEW:
            # Preserve rule final_score and add a completely
            # separate LLM contextual score.
            # ------------------------------------------------

            final_outfit["llm_score"] = round(
                float(selection.llm_score),
                2,
            )

            final_outfit["llm_reason"] = (
                selection.reason.strip()
            )

            final_outfits.append(
                final_outfit
            )

        selected_ids = [
            selection.candidate_id
            for selection in (
                parsed_response.selected_outfits
            )
        ]

        print(
            "[LLM RERANKER] Selected: "
            + ", ".join(selected_ids)
        )

        # ----------------------------------------------------
        # NEW:
        # Helpful terminal output for testing.
        # ----------------------------------------------------

        for selection in (
            parsed_response.selected_outfits
        ):

            print(
                f"[LLM RERANKER] "
                f"{selection.candidate_id} "
                f"LLM Score: "
                f"{selection.llm_score}/100"
            )

        print(
            "[LLM RERANKER] Fallback used: False"
        )

        return final_outfits

    # --------------------------------------------------------
    # 9. SAFE FALLBACK
    # --------------------------------------------------------

    except Exception as error:

        print(
            f"[LLM RERANKER] Gemini failed: {error}"
        )

        print(
            "[LLM RERANKER] Using rule-based Top 3."
        )

        print(
            "[LLM RERANKER] Fallback used: True"
        )

        return _fallback_top_outfits(
            candidates
        )