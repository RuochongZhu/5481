#!/usr/bin/env python3
"""
Multi-Agent Vibe Research Pipeline
===================================
Cornell SYSEN 6170 — Multi-Agent Lab

Research Topic: AI Data Crisis & CampusGo as Authenticity Sensor

Architecture:
  Agent 1 (Literature Scout)
      ↓  full markdown output
  Agent 2 (Quantitative Analyst)
      ↓  Agent 1 + Agent 2 outputs
  Agent 3 (Solution Architect)

Improvements over original version:
  - Extracted agent_run() helper function (inspired by functions.py pattern)
  - YAML-based rules file for agent behavior (inspired by 04_rules.yaml pattern)
  - format_rules_for_prompt() injects rules into system prompts at runtime
  - Cleaner separation of concerns: config, rules, prompts, execution

Prompt Iteration History:
  v1: Basic role descriptions → output was unstructured, no consistent formatting
  v2: Added strict markdown headers and section constraints → structure improved
      but inter-agent coherence was poor; agents repeated rather than built on
      each other's work
  v3: Injected concrete numerical anchors (3.119 / 3.883 bits entropy,
      variance formula, 138 commits), enforced word limits per agent, and
      embedded real CampusGo component names → reliable, coherent chain output
  v4 (final): Extracted YAML rules file + agent_run() helper + format_rules_for_prompt()
      → modular, maintainable, rules can be tweaked without touching code
"""

import os
import sys
import yaml
import textwrap
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MODEL = "claude-sonnet-4-20250514"
OUTPUT_FILE = "agent_output.txt"
COMBINED_MD = "combined_output.md"
RULES_FILE = "agent_rules.yaml"

# ---------------------------------------------------------------------------
# CampusGo project data (injected into Agent 3 context)
# ---------------------------------------------------------------------------
CAMPUSGO_DATA = textwrap.dedent("""\
    CampusGo (https://campusgo.college) — live deployment
    Repository: github.com/RuochongZhu/CampusRide  ·  138 commits
    Stack: Vue 3 + Node.js + Supabase  ·  Team: 5-6 members

    Key Vue Components:
      - ActivityCheckinModal.vue  → GPS-based check-in
      - CheckInQRCode.vue         → QR code with 30-min rotation
      - MapCanvas.vue             → Satellite map view
      - CommentsSection.vue       → Post-activity comments
      - ActivityChatModal.vue     → 1-on-1 activity chat
      - GroupChatModal.vue        → Group chat modal
      - RatingModal.vue           → Star-rating system
      - ActivityForm.vue          → Activity creation (7 categories)

    4-Layer Authenticity Stack:
      1. Identity   — JWT + .edu email verification
      2. Physical   — GPS check-in + QR 30-min rotation + distance validation
      3. Social     — Star ratings + co-presence verification
      4. Behavioral — Ride transactions + coordination patterns

    Composite Score:
      A_score = 0.25·ID + 0.35·Geo + 0.20·Social + 0.20·Behavioral
""")

# ---------------------------------------------------------------------------
# Helper functions (inspired by functions.py agent_run pattern)
# ---------------------------------------------------------------------------

def load_rules(filepath):
    """Load agent rules from a YAML file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, filepath)
    with open(full_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def format_rules_for_prompt(ruleset):
    """
    Format a YAML ruleset into a string for injection into system prompts.
    Mirrors the pattern from 04_rules.py.
    """
    return f"{ruleset['name']}\n{ruleset['description']}\n\n{ruleset['guidance']}"


def agent_run(client, role, task, model=MODEL, max_tokens=2048):
    """
    Run a single agent with a given role (system prompt) and task (user message).
    Mirrors the agent_run() pattern from functions.py.

    Parameters:
    -----------
    client : Anthropic
        The Anthropic API client
    role : str
        System prompt defining the agent's behavior
    task : str
        User message / task input
    model : str
        Model ID to use
    max_tokens : int
        Maximum response length

    Returns:
    --------
    str
        The agent's text response
    """
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=role,
        messages=[{"role": "user", "content": task}],
    )
    return resp.content[0].text


def separator(emoji, title):
    bar = "=" * 72
    return f"\n{bar}\n  {emoji} {title}\n{bar}\n"


# ---------------------------------------------------------------------------
# System prompts (base roles — rules are appended at runtime)
# ---------------------------------------------------------------------------
AGENT1_BASE = textwrap.dedent("""\
    You are **Literature Scout**, the first agent in a three-agent research
    pipeline studying the AI data crisis and authenticity verification.

    OUTPUT FORMAT (strict markdown, ≤ 800 words):

    ## 1 Literature Review Table
    A markdown table with exactly 6 rows:
    | # | Paper | Key Finding |
    Include these papers:
    1. Shumailov et al., "AI models collapse when trained on recursively
       generated data," Nature 2024 — variance formula
       Var(X_j^n) = σ²(1 + n/M)
    2. Alemohammad et al., "Self-Consuming Generative Models Go MAD,"
       ICLR 2024 — Model Autophagy Disorder
    3. Feng, Dohmatob & Kempe, "Model collapse in LLMs," ICML 2024 —
       tail distribution erosion
    4. Widjaja et al., 2023 — 2-gram entropy: AI text = 3.119 bits,
       Human text = 3.883 bits → 20% gap
    5. Borji, "A Categorical Archive of ChatGPT Failures," arXiv 2024 —
       systematic failure taxonomy
    6. Martinez et al., "Towards Understanding Retrieval Collapse," 2025 —
       RAG feedback loops

    ## 2 Problem Statement
    Two paragraphs: (a) model collapse mechanics, (b) web-scale data pollution.

    ## 3 Information-Entropy Connection
    Explain Shannon entropy H(X), KL divergence D_KL, and the measured
    20% entropy gap (3.119 vs 3.883 bits). Show why entropy is the right
    lens for quantifying authenticity loss.

    ## 4 Research Gap
    Identify the gap: existing work diagnoses the crisis but no platform
    actively collects physically-verified, high-entropy human data as a
    countermeasure. This sets up Agent 2's quantitative framework.
""")

AGENT2_BASE = textwrap.dedent("""\
    You are **Quantitative Analyst**, the second agent in a three-agent
    research pipeline. You receive the Literature Scout's output and build
    a formal quantitative framework.

    OUTPUT FORMAT (strict markdown, ≤ 600 words):

    ## 1 Authenticity Loss Function

    Define:
      L_auth = λ₁·D_KL(p_human ∥ p_model)
             + λ₂·ΔH(corpus)
             + λ₃·V_tail

    Where:
    - D_KL  = KL divergence between human and model token distributions
    - ΔH    = entropy degradation over training generations
    - V_tail = tail-distribution variance ratio

    Explain each component in 1-2 sentences.

    ## 2 Entropy Degradation Model

    Present the recursive variance formula from Shumailov et al.:
      Var(X_j^n) = σ²(1 + n/M)
    where n = synthetic generation count, M = original corpus size.
    Derive that entropy drops as H_n ≈ H_0 − (n / 2M) · ln(2πeσ²).
    Explain the implication: each synthetic generation irreversibly
    reduces information content.

    ## 3 Metrics Table

    | # | Metric | Symbol | Target | Meaning |
    Define exactly 6 metrics:
    1. KL Divergence        | D_KL   | < 0.05  | Distribution fidelity
    2. Entropy Gap          | ΔH     | < 5%    | Information preservation
    3. Tail Variance Ratio  | V_tail | > 0.90  | Minority-voice retention
    4. GPS Verification Rate| R_geo  | > 95%   | Physical presence proof
    5. Temporal Freshness   | T_fresh| < 30min | Data recency guarantee
    6. Social Corroboration | S_corr | > 0.80  | Multi-user agreement

    ## 4 Key Insight

    One paragraph: physical-world anchoring (GPS, QR, co-presence) is the
    strongest authenticity guarantee because it is the hardest signal to
    synthesize. This bridges to Agent 3's platform mapping.
""")

AGENT3_BASE = textwrap.dedent("""\
    You are **Solution Architect**, the third and final agent. You receive
    outputs from both the Literature Scout and the Quantitative Analyst,
    plus real project data from CampusGo.

    OUTPUT FORMAT (strict markdown, ≤ 800 words):

    ## 1 Feature-to-Metric Mapping

    | # | CampusGo Feature | Component | Metric | How It Helps |
    Map exactly 6 features:
    1. GPS Check-in          | ActivityCheckinModal.vue | R_geo   | …
    2. QR 30-min Rotation    | CheckInQRCode.vue       | T_fresh | …
    3. Satellite Map View    | MapCanvas.vue            | D_KL    | …
    4. Star Ratings          | RatingModal.vue          | S_corr  | …
    5. Three Chat Modalities | ActivityChatModal.vue, GroupChatModal.vue, CommentsSection.vue | ΔH | …
    6. 7 Activity Categories | ActivityForm.vue         | V_tail  | …

    ## 2 Four-Layer Authenticity Stack

    Describe each layer in 2-3 sentences:
    1. **Identity Layer** — JWT + .edu email verification
    2. **Physical Layer** — GPS check-in + QR 30-min rotation + distance ≤ 200m
    3. **Social Layer** — Star ratings + co-presence verification
    4. **Behavioral Layer** — Ride transactions + coordination patterns

    Present the composite score:
      A_score = 0.25·ID + 0.35·Geo + 0.20·Social + 0.20·Behavioral
    Explain why Physical gets the highest weight (hardest to fake, per
    Agent 2's key insight).

    ## 3 Anti-Algorithmic Design Evidence

    Analyze CampusGo's design philosophy:
    - No algorithmic feed or recommendation engine
    - Geography-first discovery (MapCanvas.vue)
    - User-controlled visibility settings
    - Organic social proof via ratings, not engagement optimization
    Explain how this counters the synthetic-data feedback loops identified
    by Agent 1.

    ## 4 Current Development Status

    - 138 commits across integration-production branch
    - Live at campusgo.college
    - Team of 5-6 members
    - Vue 3 + Node.js + Supabase stack
    - 7 activity categories driving tail-distribution diversity
""")


# ---------------------------------------------------------------------------
# Demo mode
# ---------------------------------------------------------------------------

def demo_mode():
    """Print architecture overview when no API key is available."""
    print("\n⚠️  ANTHROPIC_API_KEY not found — running in DEMO MODE\n")
    print("=" * 72)
    print("  MULTI-AGENT ARCHITECTURE OVERVIEW")
    print("=" * 72)

    # Load and display rules
    try:
        rules = load_rules(RULES_FILE)
        print("\n  📋 Loaded YAML Rules from agent_rules.yaml:")
        for _agent_type, rulesets in rules["rules"].items():
            for r in rulesets:
                print(f"    - {r['name']}: {r['description']}")
        print()
    except FileNotFoundError:
        print("\n  ⚠️  agent_rules.yaml not found, using embedded prompts only\n")

    print(textwrap.dedent("""\
        Pipeline: sequential chain (Agent 1 → Agent 2 → Agent 3)

        Agent 1 — Literature Scout
          System prompt: base role + YAML rules → 800-word limit, 6 papers
          Output: literature table, problem statement, entropy connection, gap

        Agent 2 — Quantitative Analyst
          Input:  Agent 1 full output
          System prompt: base role + YAML rules → 600-word limit, L_auth formula
          Output: loss function, degradation model, metrics, key insight

        Agent 3 — Solution Architect
          Input:  Agent 1 + Agent 2 full outputs + CampusGo project data
          System prompt: base role + YAML rules → 800-word limit, feature mapping
          Output: mapping table, authenticity stack, anti-algo analysis, status

        Key Design Patterns (from course labs):
          - agent_run() helper function (from functions.py)
          - YAML rules injection (from 04_rules.yaml / 04_rules.py)
          - format_rules_for_prompt() for runtime rule composition

        Prompt Design Iterations:
          v1 → basic roles, unstructured output
          v2 → markdown headers, better structure, weak coherence
          v3 → numerical anchors + word limits + real data
          v4 → YAML rules + agent_run() helper → modular & maintainable
    """))
    print("=" * 72)
    print("\n  System prompts are defined in this script.")
    print("  Rules are defined in agent_rules.yaml.")
    print("  Set ANTHROPIC_API_KEY and re-run for live execution.\n")


# ---------------------------------------------------------------------------
# Pipeline execution
# ---------------------------------------------------------------------------

def run_pipeline():
    """Execute the three-agent pipeline via Anthropic API."""
    try:
        from anthropic import Anthropic
    except ImportError:
        print("ERROR: anthropic package not installed. Run: pip install anthropic")
        sys.exit(1)

    client = Anthropic()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Load YAML rules
    try:
        rules = load_rules(RULES_FILE)
        rules_agent1 = format_rules_for_prompt(rules["rules"]["literature_scout"][0])
        rules_agent2 = format_rules_for_prompt(rules["rules"]["quantitative_analyst"][0])
        rules_agent3 = format_rules_for_prompt(rules["rules"]["solution_architect"][0])
        print("  📋 YAML rules loaded from agent_rules.yaml")
    except FileNotFoundError:
        rules_agent1 = rules_agent2 = rules_agent3 = ""
        print("  ⚠️  agent_rules.yaml not found, using base prompts only")

    # Compose system prompts = base role + YAML rules
    agent1_system = f"{AGENT1_BASE}\n\n{rules_agent1}"
    agent2_system = f"{AGENT2_BASE}\n\n{rules_agent2}"
    agent3_system = f"{AGENT3_BASE}\n\n{rules_agent3}"

    header = (
        "\n🔬🔬🔬 MULTI-AGENT VIBE RESEARCH PIPELINE 🔬🔬🔬\n"
        f"  Timestamp: {timestamp}\n"
        f"  Model: {MODEL}\n"
    )
    print(header)

    # --- Agent 1 --------------------------------------------------------
    print(separator("📚", "AGENT 1: Literature Scout"))
    agent1_out = agent_run(
        client=client,
        role=agent1_system,
        task=(
            "Conduct a literature review on AI model collapse and data "
            "pollution. Cover the six papers listed in your instructions, "
            "highlight the 20% entropy gap (3.119 vs 3.883 bits), and "
            "identify the research gap that motivates a physically-verified "
            "data collection platform."
        ),
    )
    print(agent1_out)

    # --- Agent 2 --------------------------------------------------------
    print(separator("📐", "AGENT 2: Quantitative Analyst"))
    agent2_out = agent_run(
        client=client,
        role=agent2_system,
        task=(
            "Based on the following literature review from Agent 1, "
            "define the Authenticity Loss Function L_auth, the entropy "
            "degradation model, and the six quantitative metrics.\n\n"
            "--- AGENT 1 OUTPUT ---\n"
            f"{agent1_out}\n"
            "--- END AGENT 1 OUTPUT ---"
        ),
    )
    print(agent2_out)

    # --- Agent 3 --------------------------------------------------------
    print(separator("🏗️ ", "AGENT 3: Solution Architect"))
    agent3_out = agent_run(
        client=client,
        role=agent3_system,
        task=(
            "Using the literature review and quantitative framework below, "
            "map CampusGo's features to the authenticity metrics, describe "
            "the four-layer stack, and analyze the anti-algorithmic design.\n\n"
            "--- AGENT 1 OUTPUT ---\n"
            f"{agent1_out}\n"
            "--- END AGENT 1 OUTPUT ---\n\n"
            "--- AGENT 2 OUTPUT ---\n"
            f"{agent2_out}\n"
            "--- END AGENT 2 OUTPUT ---\n\n"
            "--- CAMPUSGO PROJECT DATA ---\n"
            f"{CAMPUSGO_DATA}\n"
            "--- END CAMPUSGO DATA ---"
        ),
    )
    print(agent3_out)

    # --- Pipeline complete ----------------------------------------------
    print(separator("✅", "PIPELINE COMPLETE"))
    print(f"  All 3 agents finished at {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}")

    # Save combined output
    full_output = (
        f"{header}"
        f"{separator('📚', 'AGENT 1: Literature Scout')}"
        f"{agent1_out}\n"
        f"{separator('📐', 'AGENT 2: Quantitative Analyst')}"
        f"{agent2_out}\n"
        f"{separator('🏗️ ', 'AGENT 3: Solution Architect')}"
        f"{agent3_out}\n"
        f"{separator('✅', 'PIPELINE COMPLETE')}"
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_output)
    print(f"\n  📄 Terminal output saved to {OUTPUT_FILE}")

    combined_md = (
        "# Multi-Agent Research Output\n\n"
        f"*Generated {timestamp} · Model: {MODEL}*\n\n"
        "---\n\n"
        "## Agent 1 — Literature Scout\n\n"
        f"{agent1_out}\n\n"
        "---\n\n"
        "## Agent 2 — Quantitative Analyst\n\n"
        f"{agent2_out}\n\n"
        "---\n\n"
        "## Agent 3 — Solution Architect\n\n"
        f"{agent3_out}\n"
    )
    with open(COMBINED_MD, "w", encoding="utf-8") as f:
        f.write(combined_md)
    print(f"  📄 Combined markdown saved to {COMBINED_MD}\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if os.environ.get("ANTHROPIC_API_KEY"):
        run_pipeline()
    else:
        demo_mode()
