import re

with open('wwwroot/css/game.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Change root variables
css = re.sub(r'--bg-dark: #[0-9a-fA-F]+;', '--bg-dark: #f2f2f2;', css)
css = re.sub(r'--bg-surface: #[0-9a-fA-F]+;', '--bg-surface: #ffffff;', css)
css = re.sub(r'--bg-surface-raised: #[0-9a-fA-F]+;', '--bg-surface-raised: #ffffff;', css)
css = re.sub(r'--border-color: rgba[^;]+;', '--border-color: #d1d1d1;', css)
css = re.sub(r'--border-hover: rgba[^;]+;', '--border-hover: #000000;', css)
css = re.sub(r'--text-primary: #[0-9a-fA-F]+;', '--text-primary: #000000;', css)
css = re.sub(r'--text-secondary: #[0-9a-fA-F]+;', '--text-secondary: #666666;', css)
css = re.sub(r'font-family:[^;]+;', 'font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;', css)

# Cards styling
css = re.sub(r'\.cah-card {[^}]+}', r'''.cah-card {
    border-radius: 12px;
    padding: 24px 20px;
    font-weight: 700;
    font-size: 1.25rem;
    line-height: 1.2;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.2s ease, margin 0.2s;
    position: relative;
    user-select: none;
    letter-spacing: -0.5px;
    min-height: 280px;
    border: 1px solid var(--border-color);
}''', css)

# Make sure white cards have black text
css = css.replace('.card-white {\n    background-color: #ffffff;\n    color: #0f1012;\n}', '.card-white {\n    background-color: #ffffff;\n    color: #000000;\n}')

# Make sure black cards have white text
css = css.replace('.card-black {\n    background-color: #0f1012;\n    color: #ffffff;\n}', '.card-black {\n    background-color: #000000;\n    color: #ffffff;\n    border-color: #000000;\n}')

# Fix badges and buttons to fit B&W theme
css = css.replace('.btn-cah-primary {\n    background: linear-gradient(135deg, var(--accent-blue), #2563eb);\n    color: white;\n    border: none;\n}', '.btn-cah-primary {\n    background: #000000;\n    color: white;\n    border: 2px solid #000000;\n}')
css = css.replace('.btn-cah-primary:hover {\n    background: linear-gradient(135deg, #2563eb, #1d4ed8);\n    transform: translateY(-2px);\n    color: white;\n}', '.btn-cah-primary:hover {\n    background: #ffffff;\n    color: #000000;\n    transform: translateY(-2px);\n}')

css = css.replace('.btn-cah-dark {\n    background: var(--bg-surface-raised);\n    color: var(--text-primary);\n    border: 1px solid var(--border-color);\n}', '.btn-cah-dark {\n    background: #ffffff;\n    color: #000000;\n    border: 2px solid #000000;\n}')
css = css.replace('.btn-cah-dark:hover {\n    border-color: var(--border-hover);\n    background: rgba(255, 255, 255, 0.05);\n}', '.btn-cah-dark:hover {\n    background: #f0f0f0;\n}')

css = css.replace('.btn-cah-accent {\n    background: linear-gradient(135deg, var(--accent-gold), #d97706);\n    color: white;\n    border: none;\n}', '.btn-cah-accent {\n    background: #000000;\n    color: white;\n    border: 2px solid #000000;\n}')
css = css.replace('.btn-cah-accent:hover {\n    background: linear-gradient(135deg, #d97706, #b45309);\n    transform: translateY(-2px);\n    color: white;\n}', '.btn-cah-accent:hover {\n    background: #333333;\n    color: white;\n    transform: translateY(-2px);\n}')


with open('wwwroot/css/game.css', 'w', encoding='utf-8') as f:
    f.write(css)
