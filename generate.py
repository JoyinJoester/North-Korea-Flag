#!/usr/bin/env python3
"""
North Korea flag contributor component generator.

Generates a composite SVG with a configurable North Korea flag
and top contributor avatars from a GitHub repository.

Usage:
  python generate.py --repo owner/repo
  python generate.py --repo owner/repo --blue "#0055aa" --count 5
  python generate.py  # reads config.json or GITHUB_REPOSITORY env

No external dependencies — stdlib only.
"""

import argparse
import json
import math
import os
import sys
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")

DEFAULTS = {
    "repo": "",
    "blue": "#024FA2",
    "red": "#ED1C27",
    "white": "#FFFFFF",
    "icon_url": "",
    "icon_scale": "0.8",
    "count": "3",
    "avatar_size": "96",
    "output": os.path.join(SCRIPT_DIR, "output.svg"),
    "flag_output": os.path.join(SCRIPT_DIR, "flag.svg"),
}


def load_config_file():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_config(args):
    cfg = load_config_file()
    colors = cfg.get("colors", {})
    icon = cfg.get("icon", {})
    contrib = cfg.get("contributors", {})

    def val(arg_name, cfg_key=None, default_key=None):
        cli = getattr(args, arg_name.replace("-", "_"), None)
        if cli:
            return cli
        if cfg_key and cfg_key in cfg:
            return str(cfg[cfg_key])
        if cfg_key and "." in cfg_key:
            parts = cfg_key.split(".")
            nested = cfg
            for p in parts:
                nested = nested.get(p, {}) if isinstance(nested, dict) else {}
            if nested:
                return str(nested)
        return DEFAULTS.get(default_key or arg_name, "")

    return {
        "repo": args.repo or cfg.get("repo") or os.environ.get("GITHUB_REPOSITORY", ""),
        "colors": {
            "blue": args.blue or colors.get("blue", DEFAULTS["blue"]),
            "red": args.red or colors.get("red", DEFAULTS["red"]),
            "white": args.white or colors.get("white", DEFAULTS["white"]),
        },
        "icon": {
            "url": args.icon_url or icon.get("url", DEFAULTS["icon_url"]),
            "scale": float(args.icon_scale or icon.get("scale", DEFAULTS["icon_scale"])),
        },
        "contributors": {
            "count": int(args.count or contrib.get("count", DEFAULTS["count"])),
            "avatar_size": int(args.avatar_size or contrib.get("avatar_size", DEFAULTS["avatar_size"])),
        },
        "output": args.output or DEFAULTS["output"],
        "flag_output": args.flag_output or DEFAULTS["flag_output"],
    }


def parse_args():
    p = argparse.ArgumentParser(description="Generate North Korea flag contributor SVG")
    p.add_argument("--repo", help="GitHub repo (owner/repo)")
    p.add_argument("--blue", help="Blue stripe color (hex)")
    p.add_argument("--red", help="Red stripe color (hex)")
    p.add_argument("--white", help="White color (hex)")
    p.add_argument("--icon-url", help="Project icon image URL")
    p.add_argument("--icon-scale", help="Icon scale relative to disc (0-1)")
    p.add_argument("--count", help="Number of contributors to show")
    p.add_argument("--avatar-size", help="Avatar diameter in px")
    p.add_argument("--output", help="Output SVG path")
    p.add_argument("--flag-output", help="Standalone flag SVG path")
    return p.parse_args()


def fetch_contributors(repo, count=10):
    url = f"https://api.github.com/repos/{repo}/contributors?per_page={count}"
    req = urllib.request.Request(url, headers={"User-Agent": "north-korea-svg-gen"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        return [
            {"login": c["login"], "contributions": c["contributions"]}
            for c in data
            if c.get("type") == "User"
        ]
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
        print(f"Warning: failed to fetch contributors: {e}", file=sys.stderr)
        return []


def build_star_points(cx, cy, outer_r, inner_r=None):
    if inner_r is None:
        inner_r = outer_r * math.sin(math.radians(18)) / math.sin(math.radians(54))
    points = []
    for i in range(10):
        angle = math.radians(-90 + i * 36)
        r = outer_r if i % 2 == 0 else inner_r
        points.append(f"{cx + r * math.cos(angle):.2f},{cy + r * math.sin(angle):.2f}")
    return " ".join(points)


def build_flag_svg(config):
    c = config["colors"]
    flag_w, flag_h = 660, 400
    u = flag_h / 8  # 50

    blue_h = u           # 50
    white_h = u * 0.25   # 12.5
    red_h = u * 5.5      # 275

    red_white_h = red_h + 2 * white_h  # 300
    disc_r = red_white_h / 3           # 100
    disc_cx = flag_w * 0.25            # 165
    disc_cy = flag_h / 2               # 200

    star_r = disc_r - white_h          # 87.5
    star_points = build_star_points(disc_cx, disc_cy, star_r)

    icon = config.get("icon", {})
    icon_url = icon.get("url", "").strip()
    icon_scale = icon.get("scale", 0.8)

    if icon_url:
        icon_size = disc_r * 2 * icon_scale
        ix = disc_cx - icon_size / 2
        iy = disc_cy - icon_size / 2
        disc_content = (
            f'<defs><clipPath id="icon-clip">'
            f'<circle cx="{disc_cx:.1f}" cy="{disc_cy:.1f}" r="{disc_r:.1f}"/>'
            f'</clipPath></defs>'
            f'<image href="{_xml_escape(icon_url)}" '
            f'x="{ix:.1f}" y="{iy:.1f}" '
            f'width="{icon_size:.1f}" height="{icon_size:.1f}" '
            f'clip-path="url(#icon-clip)" '
            f'preserveAspectRatio="xMidYMid slice"/>'
        )
    else:
        disc_content = f'<polygon points="{star_points}" fill="{c["red"]}"/>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{flag_w}" height="{flag_h}" viewBox="0 0 {flag_w} {flag_h}">
  <rect x="0" y="0" width="{flag_w}" height="{blue_h:.1f}" fill="{c["blue"]}"/>
  <rect x="0" y="{blue_h:.1f}" width="{flag_w}" height="{white_h:.1f}" fill="{c["white"]}"/>
  <rect x="0" y="{(blue_h + white_h):.1f}" width="{flag_w}" height="{red_h:.1f}" fill="{c["red"]}"/>
  <rect x="0" y="{(blue_h + white_h + red_h):.1f}" width="{flag_w}" height="{white_h:.1f}" fill="{c["white"]}"/>
  <rect x="0" y="{(blue_h + white_h + red_h + white_h):.1f}" width="{flag_w}" height="{blue_h:.1f}" fill="{c["blue"]}"/>
  <circle cx="{disc_cx}" cy="{disc_cy}" r="{disc_r}" fill="{c["white"]}"/>
  {disc_content}
</svg>'''
    return svg


def _r(v):
    return round(v)


def build_composite_svg(config, contributors):
    c = config["colors"]
    flag_w, flag_h = 660, 400
    count = config["contributors"].get("count", 3)
    top = contributors[:count]

    u = flag_h / 8
    red_top = u + u * 0.25       # 62.5
    red_bot = red_top + u * 5.5  # 337.5
    red_mid = (red_top + red_bot) / 2

    avatar_zone_left = 310
    avatar_zone_right = flag_w - 20
    avatar_zone_w = avatar_zone_right - avatar_zone_left
    slot_w = avatar_zone_w / max(count, 1)

    # For single contributor, use more of the red stripe area
    if count == 1:
        avatar_zone_left = 300
        avatar_zone_right = flag_w - 40
        avatar_zone_w = avatar_zone_right - avatar_zone_left
        slot_w = avatar_zone_w
        max_avatar = min(int(slot_w - 20), int((red_bot - red_top) * 0.45))
    else:
        max_avatar = min(int(slot_w - 20), int((red_bot - red_top) * 0.4))

    avatar_size = min(config["contributors"].get("avatar_size", 96), max_avatar)
    avatar_r = avatar_size / 2

    avatar_blocks = []
    for i, user in enumerate(top):
        cx = avatar_zone_left + slot_w * i + slot_w / 2
        cy = red_mid - 10
        avatar_url = f"https://github.com/{_xml_escape(user['login'])}.png?size={avatar_size}"
        commits_text = f"{user['contributions']:,}"

        profile_url = f"https://github.com/{_xml_escape(user['login'])}"
        avatar_blocks.append(f'''
  <!-- {user['login']} -->
  <a href="{profile_url}" target="_blank">
  <circle cx="{_r(cx)}" cy="{_r(cy)}" r="{_r(avatar_r + 3)}" fill="{c['white']}" opacity="0.25"/>
  <clipPath id="clip{i}"><circle cx="{_r(cx)}" cy="{_r(cy)}" r="{_r(avatar_r)}"/></clipPath>
  <image href="{_xml_escape(avatar_url)}"
         x="{_r(cx - avatar_r)}" y="{_r(cy - avatar_r)}"
         width="{avatar_size}" height="{avatar_size}"
         clip-path="url(#clip{i})"
         preserveAspectRatio="xMidYMid slice"/>
  <text x="{_r(cx)}" y="{_r(cy + avatar_r + 15)}" text-anchor="middle"
        font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"
        font-size="13" font-weight="600" fill="{c['white']}">{_xml_escape(user['login'])}</text>
  <text x="{_r(cx)}" y="{_r(cy + avatar_r + 28)}" text-anchor="middle"
        font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"
        font-size="10" fill="{c['white']}" opacity="0.8">{commits_text} commits</text>
  </a>''')

    flag_svg = build_flag_svg(config)
    flag_inner = _extract_svg_inner(flag_svg)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{flag_w}" height="{flag_h}" viewBox="0 0 {flag_w} {flag_h}">
{flag_inner}
{"".join(avatar_blocks)}
</svg>'''


def _xml_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _extract_svg_inner(svg_str):
    start = svg_str.index(">") + 1
    end = svg_str.rindex("</svg>")
    return svg_str[start:end]


def main():
    args = parse_args()
    config = build_config(args)
    repo = config["repo"]

    if not repo:
        print("Error: --repo is required (or set GITHUB_REPOSITORY env)", file=sys.stderr)
        sys.exit(1)

    count = config["contributors"]["count"]
    print(f"Fetching contributors for {repo}...")
    contributors = fetch_contributors(repo, count=count + 5)

    if not contributors:
        print("No contributors fetched; generating with placeholders.", file=sys.stderr)
        contributors = [
            {"login": f"contributor-{i+1}", "contributions": 0}
            for i in range(count)
        ]

    # Write standalone flag
    with open(config["flag_output"], "w", encoding="utf-8") as f:
        f.write(build_flag_svg(config))
    print(f"Wrote {config['flag_output']}")

    # Write composite
    with open(config["output"], "w", encoding="utf-8") as f:
        f.write(build_composite_svg(config, contributors))
    print(f"Wrote {config['output']}")

    for user in contributors[:count]:
        print(f"  {user['login']}: {user['contributions']:,} commits")


if __name__ == "__main__":
    main()
