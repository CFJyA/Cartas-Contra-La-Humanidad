import json
import uuid

with open('Data/cards_database.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

new_white_cards = [
    "Los 43 de Ayotzinapa.",
    "La matanza de Tlatelolco.",
    "Fosas comunes en Tamaulipas.",
    "Los Zetas.",
    "El Cártel de Jalisco Nueva Generación (CJNG).",
    "Un convoy de sicarios con tenis pirata.",
    "Decapitar vatos y subirlo al Blog del Narco.",
    "El chupacabras.",
    "La Rosa de Guadalupe.",
    "Dar mordida a los tránsitos.",
    "Elba Esther Gordillo en lencería.",
    "Un tinaco Rotoplas abandonado en el cerro.",
    "Cobro de piso en la tortillería.",
    "Linchamientos en el Estado de México.",
    "Gritar 'puto' en el estadio.",
    "Echarle la culpa de todo a Calderón.",
    "Un bache del tamaño de un Tsuru.",
    "Ir al IMSS y salir sin pierna.",
    "Un pozole de carne humana.",
    "Comprar piratería en Tepito.",
    "Que te asalten en la combi.",
    "El Oxxo de la esquina que nunca tiene sistema.",
    "AMLO diciendo 'abrazos, no balazos'.",
    "La Santa Muerte.",
    "Balaceras en Culiacán."
]

new_black_cards = [
    {"text": "El verdadero secreto de AMLO para gobernar México es ______.", "pick": 1},
    {"text": "¿Qué encontraron realmente en las fosas de Tamaulipas? ______.", "pick": 1},
    {"text": "El próximo episodio de La Rosa de Guadalupe trata sobre ______ y ______.", "pick": 2},
    {"text": "La próxima estrategia de seguridad del gobierno incluirá ______.", "pick": 1},
    {"text": "No me asaltes carnal, mejor llévate ______.", "pick": 1},
    {"text": "Antes de matarme, el sicario del CJNG me obligó a mirar ______.", "pick": 1},
    {"text": "¿Cuál es la causa de los baches en el Estado de México? ______.", "pick": 1},
    {"text": "En Tepito, por 500 pesos te consigues ______.", "pick": 1},
    {"text": "El verdadero responsable de lo de Ayotzinapa fue ______.", "pick": 1},
    {"text": "Si sobrevives al IMSS, te dan como premio ______.", "pick": 1}
]

for wc in new_white_cards:
    db['whiteCards'].append({
        "id": "w_" + uuid.uuid4().hex[:8],
        "text": wc,
        "type": "white"
    })

for bc in new_black_cards:
    db['blackCards'].append({
        "id": "b_" + uuid.uuid4().hex[:8],
        "text": bc["text"],
        "pick": bc["pick"],
        "type": "black"
    })

with open('Data/cards_database.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Cartas mexicanizadas agregadas exitosamente.")
