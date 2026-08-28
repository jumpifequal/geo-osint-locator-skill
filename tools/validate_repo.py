from __future__ import annotations

from pathlib import Path
import importlib.util
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "SKILL.md",
    "agents/openai.yaml",
    "assets/icon.svg",
    "scripts/dashboard_svg.py",
    "scripts/rerank_candidates.py",
    "references/01_evidence_policy.md",
    "references/20_discriminative_reranking.md",
    "docs/architecture.md",
    "README.md",
]

def load_module(path: Path):
    source = path.read_text(encoding="utf-8")
    compile(source, str(path), "exec")
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    for rel in REQUIRED:
        path = ROOT / rel
        assert path.exists(), f"missing required file: {rel}"

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
    assert match, "SKILL.md frontmatter missing"
    fm = yaml.safe_load(match.group(1))
    assert fm["name"] == "geo-osint-locator"
    assert "description" in fm and fm["description"].strip()

    ui = yaml.safe_load((ROOT / "agents/openai.yaml").read_text(encoding="utf-8"))
    assert ui["interface"]["icon_small"] == "./assets/icon.svg"
    assert ui["interface"]["icon_large"] == "./assets/icon.svg"
    assert ui["interface"]["brand_color"] == "#FFFFFF"

    scripts = {}
    for path in sorted((ROOT / "scripts").glob("*.py")):
        scripts[path.stem] = load_module(path)

    sample = [
        {
            "rank":"#1","candidate":"Candidate A","confidence":"PROBABLE","score":84,
            "high_value_clues":3,"holistic":"PASS","competitor":"Candidate B",
            "killer":"DISCRIMINATIVE","viewpoint":"COMPATIBLE","status":"PLAUSIBLE"
        },
        {
            "rank":"#2","candidate":"Candidate B","confidence":"POSSIBLE","score":61,
            "high_value_clues":2,"holistic":"PASS","competitor":"Candidate A",
            "killer":"GENERIC","viewpoint":"ND","status":"WEAK"
        },
        {
            "rank":"#3","candidate":"Candidate C","confidence":"LOW","score":38,
            "high_value_clues":1,"holistic":"FAIL","competitor":"Candidate A",
            "killer":"GENERIC","viewpoint":"INCOMPATIBLE","status":"REJECTED"
        },
    ]
    svg = scripts["dashboard_svg"].render_dashboard_svg(
        sample,
        decisive_missing_evidence="one additional discriminative observation"
    )
    assert svg.startswith("<svg")
    assert 'class="leader"' in svg
    assert all(name in svg for name in ["Candidate A", "Candidate B", "Candidate C"])

    generic = {
        "name":"generic","status":"ACTIVE","competitor_status":"WEAKER",
        "holistic_state":"PASS","score":88,
        "positive_clues":[
            {"discrimination":"LOW","quality":"CERTAIN","persistence":"STRUCTURAL"},
            {"discrimination":"LOW","quality":"CERTAIN","persistence":"STRUCTURAL"},
            {"discrimination":"MEDIUM","quality":"PROBABLE","persistence":"STRUCTURAL"},
        ],
    }
    specific = {
        "name":"specific","status":"ACTIVE","competitor_status":"WEAKER",
        "holistic_state":"PASS","score":72,
        "positive_clues":[
            {"discrimination":"HIGH","quality":"CERTAIN","persistence":"STRUCTURAL"},
            {"discrimination":"UNIQUE","quality":"PROBABLE","persistence":"STRUCTURAL"},
        ],
    }
    ranked = scripts["rerank_candidates"].rerank([generic, specific])
    assert ranked[0]["name"] == "specific"

    print(f"PASS: {len(scripts)} Python scripts imported")
    print("PASS: SKILL.md frontmatter")
    print("PASS: agents/openai.yaml")
    print("PASS: deterministic dashboard renderer")
    print("PASS: discriminative reranking")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
