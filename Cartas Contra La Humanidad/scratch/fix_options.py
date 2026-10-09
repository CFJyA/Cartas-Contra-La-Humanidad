import re

with open('Views/Home/Index.cshtml', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Fix encoding issues that were introduced
html = html.replace('Rǭpida', 'Rápida')
html = html.replace('Estǭndar', 'Estándar')
html = html.replace('Maratn', 'Maratón')
html = html.replace('FrenǸtico', 'Frenético')
html = html.replace('Lmite', 'Límite')
html = html.replace('Cdigo', 'Código')
html = html.replace('', '')

# Apply custom names and Express mode
html = re.sub(r'<select id="select-target-score"[^>]*>.*?</select>', '''<select id="select-target-score" class="form-select bg-cah-input border-cah text-cah-primary">
                            <option value="3">¡Pendejo, No Dura Nada! | 3 pts.</option>
                            <option value="5">Rapidín en el Baño | 5 pts.</option>
                            <option value="7" selected>La Clásica Pedita | 7 pts.</option>
                            <option value="10">Noche de Faltas a la Moral | 10 pts.</option>
                            <option value="15">Hasta que Amanezca | 15 pts.</option>
                        </select>''', html, flags=re.DOTALL)

html = re.sub(r'<select id="select-timer-seconds"[^>]*>.*?</select>', '''<select id="select-timer-seconds" class="form-select bg-cah-input border-cah text-cah-primary">
                            <option value="30">Frenético | 30 seg.</option>
                            <option value="60" selected>Equilibrado | 60 seg.</option>
                            <option value="90">Chill | 90 seg.</option>
                            <option value="0">Pa\' Los Lentos | Sin Límite</option>
                        </select>''', html, flags=re.DOTALL)

html = re.sub(r'Incluir a <em>.*?</em> \(.*?\)', 'Incluir a <em>El Bot Tóxico</em> (Un bot wey que tira cartas a lo pendejo 🤖)', html)

with open('Views/Home/Index.cshtml', 'w', encoding='utf-8') as f:
    f.write(html)
