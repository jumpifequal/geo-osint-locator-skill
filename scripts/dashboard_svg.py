from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

ALLOWED_STATUS = {"STRONG", "PLAUSIBLE", "WEAK", "REJECTED", "INDETERMINATE"}

STATUS_STYLE = {
    "STRONG": ("#DDF6E8", "#17653A"),
    "PLAUSIBLE": ("#FBE2AA", "#815814"),
    "WEAK": ("#F9D6D8", "#A33338"),
    "REJECTED": ("#ECEFF3", "#59616D"),
    "INDETERMINATE": ("#ECEFF3", "#59616D"),
}

def _s(value, default="—"):
    if value is None or value == "":
        return default
    return str(value)

def _esc(value):
    return html.escape(_s(value), quote=True)

def _clip(value, n):
    text = _s(value)
    return text if len(text) <= n else text[: n - 1] + "…"

def _metric_label(value):
    return _s(value).upper() if isinstance(value, str) else _s(value)

def _status(value):
    raw = _s(value, "INDETERMINATE").upper()
    return raw if raw in ALLOWED_STATUS else "INDETERMINATE"

def normalize_candidate(candidate, index):
    if not isinstance(candidate, dict):
        raise TypeError("candidate rows must be objects")
    return {
        "rank": _s(candidate.get("rank"), f"#{index}"),
        "candidate": _s(candidate.get("candidate"), "Unknown candidate"),
        "confidence": _s(candidate.get("confidence")),
        "score": _s(candidate.get("score")),
        "high_value_clues": _s(candidate.get("high_value_clues")),
        "holistic": _metric_label(candidate.get("holistic")),
        "competitor": _s(candidate.get("competitor")),
        "killer": _s(candidate.get("killer")),
        "viewpoint": _metric_label(candidate.get("viewpoint")),
        "status": _status(candidate.get("status")),
    }

def render_dashboard_svg(candidates, decisive_missing_evidence=None, title=None):
    """
    Fixed rendering contract:
    - Up to 3 stacked candidate cards.
    - Candidate #1 is visually highlighted with a blue border.
    - Status badge aligned to the right of the candidate title.
    - Fixed 4-column metric row: Confidence, Score, High/unique clues, Holistic match.
    - Fixed footer row: Competitor · Killer check · Viewpoint.
    - Optional final line: Decisive missing evidence: ...
    - No adaptive/reflow layout choices. Data changes; geometry does not.
    """
    if not isinstance(candidates, list):
        raise TypeError("candidates must be a list")

    rows = [normalize_candidate(c, i + 1) for i, c in enumerate(candidates[:3])]
    if not rows:
        rows = [normalize_candidate({
            "rank": "—",
            "candidate": "INDETERMINATE",
            "confidence": "—",
            "score": "—",
            "high_value_clues": "—",
            "holistic": "ND",
            "competitor": "—",
            "killer": "—",
            "viewpoint": "ND",
            "status": "INDETERMINATE",
        }, 1)]

    width = 1000
    margin_x = 18
    top = 16
    card_h = 152
    card_gap = 16
    bottom_note_h = 40 if decisive_missing_evidence else 10
    height = top + len(rows) * card_h + max(0, len(rows) - 1) * card_gap + bottom_note_h

    card_x = margin_x
    card_w = width - margin_x * 2

    # Exact, fixed x positions modeled after the user-provided reference.
    x_title = card_x + 28
    x_conf = card_x + 28
    x_score = card_x + 258
    x_clues = card_x + 488
    x_holistic = card_x + 718
    badge_right = card_x + card_w - 28

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="Final decision dashboard">',
        '<style>',
        'text{font-family:Arial,Helvetica,sans-serif;fill:#17191D}'
        '.candidate{font-size:20px;font-weight:700}'
        '.metric-label{font-size:17px;fill:#5C5E63}'
        '.metric-value{font-size:18px;font-weight:500}'
        '.footer{font-size:17px;fill:#5C5E63}'
        '.note{font-size:16px;fill:#7A7D82}'
        '.card{fill:#FFFFFF;stroke:#E5E5E5;stroke-width:1.2}'
        '.leader{fill:#FFFFFF;stroke:#78AFFF;stroke-width:2.5}',
        '</style>',
    ]

    y = top
    for idx, row in enumerate(rows):
        card_class = "leader" if idx == 0 else "card"
        parts.append(
            f'<rect x="{card_x}" y="{y}" width="{card_w}" height="{card_h}" '
            f'rx="16" class="{card_class}"/>'
        )

        # Candidate heading
        heading = f'{row["rank"]} — {_clip(row["candidate"], 58)}'
        parts.append(
            f'<text x="{x_title}" y="{y + 41}" class="candidate">{_esc(heading)}</text>'
        )

        # Status badge
        status = row["status"]
        badge_bg, badge_fg = STATUS_STYLE[status]
        badge_w = max(74, 18 + len(status) * 9)
        badge_x = badge_right - badge_w
        badge_y = y + 23
        parts.append(
            f'<rect x="{badge_x}" y="{badge_y}" width="{badge_w}" height="30" rx="11" '
            f'fill="{badge_bg}"/>'
        )
        parts.append(
            f'<text x="{badge_x + badge_w / 2}" y="{badge_y + 21}" '
            f'text-anchor="middle" style="font-family:Arial,Helvetica,sans-serif;'
            f'font-size:15px;font-weight:700;fill:{badge_fg}">{_esc(status)}</text>'
        )

        # Fixed metric labels
        parts.append(f'<text x="{x_conf}" y="{y + 73}" class="metric-label">Confidence</text>')
        parts.append(f'<text x="{x_score}" y="{y + 73}" class="metric-label">Score</text>')
        parts.append(f'<text x="{x_clues}" y="{y + 73}" class="metric-label">High/unique clues</text>')
        parts.append(f'<text x="{x_holistic}" y="{y + 73}" class="metric-label">Holistic match</text>')

        # Fixed metric values
        parts.append(f'<text x="{x_conf}" y="{y + 96}" class="metric-value">{_esc(row["confidence"])}</text>')
        score_text = row["score"]
        if score_text != "—" and "/" not in score_text:
            score_text = f"{score_text}/100"
        parts.append(f'<text x="{x_score}" y="{y + 96}" class="metric-value">{_esc(score_text)}</text>')
        parts.append(f'<text x="{x_clues}" y="{y + 96}" class="metric-value">{_esc(row["high_value_clues"])}</text>')
        parts.append(f'<text x="{x_holistic}" y="{y + 96}" class="metric-value">{_esc(row["holistic"])}</text>')

        footer = (
            f'Competitor: {_clip(row["competitor"], 34)} · '
            f'Killer check: {_clip(row["killer"], 24)} · '
            f'Viewpoint: {_clip(row["viewpoint"], 18)}'
        )
        parts.append(f'<text x="{x_title}" y="{y + 129}" class="footer">{_esc(footer)}</text>')

        y += card_h + card_gap

    if decisive_missing_evidence:
        note = f'Decisive missing evidence: {_clip(decisive_missing_evidence, 110)}'
        parts.append(f'<text x="{card_x}" y="{height - 10}" class="note">{_esc(note)}</text>')

    parts.append('</svg>')
    return "".join(parts)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file")
    parser.add_argument("--out", default="dashboard.svg")
    ns = parser.parse_args()

    data = json.loads(Path(ns.json_file).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        candidates = data.get("candidates", [])
        decisive = data.get("decisive_missing_evidence")
    else:
        candidates = data
        decisive = None

    svg = render_dashboard_svg(candidates, decisive_missing_evidence=decisive)
    Path(ns.out).write_text(svg, encoding="utf-8")
    print(ns.out)

if __name__ == "__main__":
    main()
