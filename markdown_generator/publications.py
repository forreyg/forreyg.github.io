# coding: utf-8

import os
import pandas as pd

publications = pd.read_csv("publications.tsv", sep="\t", header=0)

def yaml_block(s: str) -> str:
    """
    Safe YAML folded block scalar.
    Keeps LaTeX ($...$) intact and avoids quote-escaping hell.
    """
    if s is None:
        return ""
    s = str(s).replace("\r\n", "\n").replace("\r", "\n").strip()
    if not s:
        return ""
    # indent every line by 2 spaces for YAML block scalar
    return "\n".join("  " + line for line in s.split("\n"))

for _, item in publications.iterrows():
    pub_date = str(item.pub_date)
    url_slug = str(item.url_slug)
    title = "" if pd.isna(item.title) else str(item.title).strip()
    venue = "" if pd.isna(item.venue) else str(item.venue).strip()
    paper_url = "" if pd.isna(item.paper_url) else str(item.paper_url).strip()
    excerpt = "" if pd.isna(item.excerpt) else str(item.excerpt).strip()
    citation = "" if pd.isna(item.citation) else str(item.citation).strip()

    md_filename = os.path.basename(f"{pub_date}-{url_slug}.md")
    html_filename = f"{pub_date}-{url_slug}"

    md = "---\n"
    md += f'title: "{title.replace(chr(34), r"\"")}"\n'  # escape only double-quotes in title
    md += "collection: publications\n"
    md += "category: manuscripts\n"
    md += f"permalink: /publication/{html_filename}\n"
    md += f"date: {pub_date}\n"
    md += f"venue: '{venue.replace(\"'\", \"''\")}'\n"  # YAML single-quote escaping

    # Ensure paperurl is present (this is what your layout will use to link the title to arXiv)
    if len(paper_url) > 5:
        md += f"paperurl: '{paper_url.replace(\"'\", \"''\")}'\n"

    # Keep excerpt/citation as YAML block scalars so LaTeX stays readable and intact
    if len(excerpt) > 5:
        md += "excerpt: >-\n" + yaml_block(excerpt) + "\n"

    if len(citation) > 5:
        md += "citation: >-\n" + yaml_block(citation) + "\n"

    md += "---\n\n"

    # ✅ FIX 1: NO "Download paper" link/button in the body (your layout/title will link to arXiv)
    # (intentionally not adding any <a href='...'>Download paper here</a>)

    # Optional: include the excerpt in the page body too (helps if your theme doesn’t render math in YAML excerpt)
    if len(excerpt) > 5:
        md += "<p>\n" + excerpt + "\n</p>\n\n"

    # Optional: keep the recommended citation line (no download link)
    if len(citation) > 5:
        md += "Recommended citation: " + citation + "\n"

    with open(os.path.join("..", "_publications", md_filename), "w", encoding="utf-8") as f:
        f.write(md)
