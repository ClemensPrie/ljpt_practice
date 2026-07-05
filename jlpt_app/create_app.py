import re
import glob
import markdown

# 1. Read ALL grammar markdown files (sorted) and concatenate them.
input_files = sorted(glob.glob("n3_grammar_pages_*.md"))
if not input_files:
    # Fallback to a single file name for backwards compatibility
    input_files = ["grammar.md"]

output_file = "index.html"

parts = []
for path in input_files:
    with open(path, "r", encoding="utf-8") as f:
        parts.append(f.read())
content = "\n\n".join(parts)


# 2. Convert Kanji(Furigana) -> <ruby> BEFORE markdown conversion.
#    Widened Kana class to include the long-vowel mark ー and small kana.
def convert_furigana_to_html(text):
    pattern = r'([\u4e00-\u9fff]+)\(([\u3041-\u3096\u30A1-\u30FA\u30FCー]+)\)'
    return re.sub(pattern, r'<ruby>\1<rt>\2</rt></ruby>', text)


pre_processed = convert_furigana_to_html(content)

# 3. Actually convert Markdown to HTML.
#    Enable extensions so ##/**/>/lists/tables render properly.
md = markdown.Markdown(extensions=["extra", "sane_lists", "toc"])
html_body = md.convert(pre_processed)

# 4. Wrap in a mobile-friendly, installable (Add-to-Home-Screen) HTML document.
html_document = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>JLPT N3 文法</title>

    <!-- PWA / Add to Home Screen -->
    <link rel="manifest" href="manifest.webmanifest">
    <meta name="theme-color" content="#007bff">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="JLPT N3">
    <link rel="apple-touch-icon" href="icon-192.png">

    <style>
        body {{
            font-family: 'Hiragino Kaku Gothic Pro', 'Meiryo', sans-serif;
            background-color: #f7f9fc;
            color: #333;
            line-height: 1.8;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 720px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        h1, h2, h3, h4 {{
            border-bottom: 2px solid #eee;
            padding-bottom: 8px;
            margin-top: 30px;
            font-weight: 500;
        }}
        h2 {{ border-bottom-color: #007bff; }}
        p {{ margin: 10px 0; }}
        ul, ol {{ padding-left: 20px; }}
        li {{ margin-bottom: 8px; }}
        blockquote {{
            background: #fff9e6;
            padding: 10px 15px;
            border-left: 4px solid #ffc107;
            margin: 10px 0;
            font-size: 0.95em;
            color: #444;
        }}
        code {{
            background: #f0f0f0;
            padding: 1px 5px;
            border-radius: 4px;
        }}
        hr {{ border: none; border-top: 1px solid #ddd; margin: 30px 0; }}
        ruby {{ ruby-align: center; }}
        rt {{ font-size: 0.7em; margin-top: -2px; }}
        @media (prefers-color-scheme: dark) {{
            body {{ background-color: #1a1a1a; color: #e0e0e0; }}
            .container {{ background: #2d2d2d; box-shadow: 0 2px 10px rgba(0,0,0,0.5); }}
            h1, h2, h3, h4 {{ border-bottom-color: #444; }}
            h2 {{ border-bottom-color: #007bff; }}
            blockquote {{ background: #333; border-left-color: #ffc107; color: #ddd; }}
            code {{ background: #444; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>JLPT N3 文法</h1>
        <hr>
        {html_body}
        <br>
        <p style="text-align:center; color:#777; font-size:0.8em;">Generated from Textbook</p>
    </div>
</body>
</html>
"""

with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_document)

# 5. Write a minimal Web App Manifest so "Add to Home Screen" installs it as a standalone app.
manifest = """{
  "name": "JLPT N3 Grammar",
  "short_name": "JLPT N3",
  "start_url": "./index.html",
  "scope": "./",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#f7f9fc",
  "theme_color": "#007bff",
  "icons": [
    { "src": "icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
"""
with open("manifest.webmanifest", "w", encoding="utf-8") as f:
    f.write(manifest)

print(f"Successfully generated {output_file} from {len(input_files)} markdown file(s).")
print("Also wrote manifest.webmanifest. Add icon-192.png and icon-512.png next to index.html for the home-screen icon.")
