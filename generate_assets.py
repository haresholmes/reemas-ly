#!/usr/bin/env python3
import os, subprocess, sys

cwd = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(cwd, 'assets')
chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

if not os.path.exists(chrome_path):
    print(f'Error: Chrome not found at {chrome_path}', file=sys.stderr)
    sys.exit(1)

renders = [
    ('seal.svg', 'seal.png', 2048, 2048),
    ('seal-gold.svg', 'seal-gold.png', 2048, 2048),
    ('seal-navy.svg', 'seal-navy.png', 2048, 2048),
    ('seal-badge-dark.svg', 'seal-badge-dark.png', 2048, 2048),
    ('logo.svg', 'logo.png', 2048, 2048),
    ('logo-horizontal.svg', 'logo-horizontal.png', 2280, 420),
    ('favicon.svg', 'favicon.png', 256, 256),
]

print('--- Generating High-Resolution Transparent PNG Assets ---')
for svg_file, png_file, width, height in renders:
    svg_path = os.path.join(assets_dir, svg_file)
    png_path = os.path.join(assets_dir, png_file)
    
    html_wrapper = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ background: transparent !important; width: {width}px; height: {height}px; overflow: hidden; }}
  img {{ width: {width}px; height: {height}px; display: block; }}
</style>
</head>
<body>
  <img src="{svg_file}">
</body>
</html>'''
    
    wrapper_path = os.path.join(assets_dir, f'_tmp_{png_file}.html')
    with open(wrapper_path, 'w') as f:
        f.write(html_wrapper)
    
    cmd = [
        chrome_path,
        '--headless=new',
        '--disable-gpu',
        '--default-background-color=00000000',
        f'--window-size={width},{height}',
        f'--screenshot={png_path}',
        f'file://{wrapper_path}'
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(wrapper_path):
        os.remove(wrapper_path)
        
    if os.path.exists(png_path) and os.path.getsize(png_path) > 0:
        size_kb = os.path.getsize(png_path) // 1024
        print(f'✔ Rendered {png_file} ({width}x{height}, {size_kb} KB)')
    else:
        print(f'✖ Failed to render {png_file}: {res.stderr}')

print('Asset generation complete!')
