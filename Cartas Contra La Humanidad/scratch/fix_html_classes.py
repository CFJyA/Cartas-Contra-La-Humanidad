import re

with open('Views/Home/Index.cshtml', 'r', encoding='utf-8') as f:
    html = f.read()

# I want to revert bg-light back to bg-cah-input or something, and use CSS for it
html = html.replace('bg-light text-dark border-dark', 'bg-cah-input border-cah')
html = html.replace('text-dark', 'text-cah-primary')
html = html.replace('text-muted', 'text-cah-secondary')

with open('Views/Home/Index.cshtml', 'w', encoding='utf-8') as f:
    f.write(html)
