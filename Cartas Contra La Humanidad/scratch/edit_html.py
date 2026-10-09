import re

with open('Views/Home/Index.cshtml', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace bg-dark text-white with simple custom classes or remove them to inherit from CSS
html = html.replace('bg-dark', 'bg-light')
html = html.replace('text-white', 'text-dark')
html = html.replace('border-secondary', 'border-dark')
html = html.replace('text-secondary', 'text-muted')

with open('Views/Home/Index.cshtml', 'w', encoding='utf-8') as f:
    f.write(html)
