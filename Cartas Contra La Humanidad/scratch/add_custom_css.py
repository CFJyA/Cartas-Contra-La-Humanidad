import re

with open('wwwroot/css/game.css', 'r', encoding='utf-8') as f:
    css = f.read()

custom_classes = """
.bg-cah-input {
    background-color: var(--bg-surface) !important;
    color: var(--text-primary) !important;
}
.border-cah {
    border-color: var(--border-color) !important;
}
.text-cah-primary {
    color: var(--text-primary) !important;
}
.text-cah-secondary {
    color: var(--text-secondary) !important;
}
"""

css += custom_classes

with open('wwwroot/css/game.css', 'w', encoding='utf-8') as f:
    f.write(css)
