import re

with open('wwwroot/css/game.css', 'r', encoding='utf-8') as f:
    css = f.read()

# First, restore the original dark theme variables to a [data-theme="dark"] selector
dark_theme = """
[data-theme="dark"] {
    --bg-dark: #0f1012;
    --bg-surface: #17181c;
    --bg-surface-raised: #202227;
    --border-color: rgba(255, 255, 255, 0.1);
    --border-hover: rgba(255, 255, 255, 0.25);
    --text-primary: #f3f4f6;
    --text-secondary: #9ca3af;
    --card-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5);
    --card-hover-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.7);
    --btn-primary-bg: #ffffff;
    --btn-primary-text: #000000;
    --btn-dark-bg: var(--bg-surface-raised);
    --btn-dark-text: var(--text-primary);
    --btn-dark-border: var(--border-color);
}
"""

# Light theme (default)
light_theme = """
:root {
    --bg-dark: #f0f2f5;
    --bg-surface: #ffffff;
    --bg-surface-raised: #ffffff;
    --border-color: #d1d5db;
    --border-hover: #9ca3af;
    --text-primary: #111827;
    --text-secondary: #6b7280;
    --accent-red: #ef4444;
    --accent-gold: #f59e0b;
    --accent-green: #10b981;
    --accent-blue: #3b82f6;
    --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --card-hover-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    --btn-primary-bg: #000000;
    --btn-primary-text: #ffffff;
    --btn-dark-bg: #ffffff;
    --btn-dark-text: #111827;
    --btn-dark-border: #d1d5db;
}
"""

css = re.sub(r':root\s*\{[^}]+\}', light_theme + dark_theme, css)

# Update button classes to use CSS variables
css = re.sub(r'\.btn-cah-primary\s*\{[^}]+\}', """.btn-cah-primary {
    background: var(--btn-primary-bg);
    color: var(--btn-primary-text);
    border: 2px solid var(--btn-primary-bg);
}""", css)

css = re.sub(r'\.btn-cah-primary:hover\s*\{[^}]+\}', """.btn-cah-primary:hover {
    background: var(--btn-primary-text);
    color: var(--btn-primary-bg);
    border-color: var(--btn-primary-bg);
    transform: translateY(-2px);
}""", css)

css = re.sub(r'\.btn-cah-dark\s*\{[^}]+\}', """.btn-cah-dark {
    background: var(--btn-dark-bg);
    color: var(--btn-dark-text);
    border: 2px solid var(--btn-dark-border);
}""", css)

css = re.sub(r'\.btn-cah-dark:hover\s*\{[^}]+\}', """.btn-cah-dark:hover {
    border-color: var(--text-primary);
}""", css)

css = re.sub(r'\.btn-cah-accent\s*\{[^}]+\}', """.btn-cah-accent {
    background: var(--accent-gold);
    color: white;
    border: 2px solid var(--accent-gold);
}""", css)

css = re.sub(r'\.btn-cah-accent:hover\s*\{[^}]+\}', """.btn-cah-accent:hover {
    background: #d97706;
    border-color: #d97706;
    color: white;
    transform: translateY(-2px);
}""", css)

# Fix white cards and black cards to respond to theme if needed, but CAH cards are literally black and white
# CAH white cards are ALWAYS white, black cards are ALWAYS black.
css = re.sub(r'\.card-white\s*\{[^}]+\}', """.card-white {
    background-color: #ffffff;
    color: #000000;
}""", css)

css = re.sub(r'\.card-black\s*\{[^}]+\}', """.card-black {
    background-color: #000000;
    color: #ffffff;
    border-color: #000000;
}""", css)

# We want the active black card to look good. The user says "The active black card is too small or badly aligned."
# Let's fix `#active-black-card` and `.stage-grid`
# Wait, let's find `#active-black-card`
css = css.replace('#active-black-card {', '#active-black-card { max-width: 350px; margin: 0 auto; ')

with open('wwwroot/css/game.css', 'w', encoding='utf-8') as f:
    f.write(css)
