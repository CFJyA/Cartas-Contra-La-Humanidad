import json

white_cards_raw = [
    # Page 2
    "Quemarse.", "Racismo.", "Olor a gente vieja.", "Un micropene.", "Mujeres en comerciales de yogurt.",
    "Connotaciones clasistas.", "Importarte una mierda el Tercer Mundo.", "Meterme un jarro de vidrio en el ano.",
    "Rehabilitación por orden judicial.", "Un molino lleno de cadáveres.", "Los gays.", "Un Pelón Pelo Rico gigante.",
    "Niños africanos.", "Un implante mamario asimétrico.", "Comérselo todo y vomitar.", "El inmigrante trabajador.",
    "Un complejo de Edipo.", "Un caballo pequeño.", "Mocos.", "Envidia de pene.",
    # Page 3
    "Enrique Peña Nieto.", "Mi trasero.", "Colchones Atlas.", "Cienciología.", "Arcadas.", "Chabelo.",
    "Darth Vader.", "Tamal Oaxaqueño.", "Consejos de un teporocho.", "Día del taco.", "Hombres japoneses ancianos.",
    "Muestras gratis.", "Estrógeno.", "Tensión sexual.", "Hambruna.", "Un pelo púbico abandonado.", "Hombres.",
    "Conmovedores huérfanos.", "Pedazos de autostopista muerto.", "Una bolsa de habichuelas mágicas.",
    # Page 4
    "Represión.", "Cabriolas.", "Mi estado amoroso.", "Compensación excesiva.", "Orinar un poco.",
    "La caída de Edgar.", "Una bola de cerumen, semen, y uñas de pie.", "Torsión testicular.", "El Diablo en persona.",
    "Age of Empires.", "Carlos Salinas de Gortari.", "Hitler robótico.", "Ser fabuloso.", "Fotos de tetas.",
    "Una caricia gentil en la parte interior del muslo.", "Testigos de Jehová.", "Los ritmos de África.",
    "El testículo que perdió Lance Armstrong.", "Pedófilos.", "El Papa.",
    # Page 5
    "Serpientes voladoras.", "Elba Esther Gordillo.", "«A veces me como una olla.»", "Pelea sexy de almohadas.",
    "Invadir Polonia.", "Mejoras cibernéticas.", "Muertes civiles.", "Trabajos.", "El orgasmo femenino.",
    "Teiboleras.", "Los Boy Scouts.", "Lecumberri.", "Pintar con los dedos.", "Mirada de Osito Cariñosito.",
    "Los judíos.", "Ser marginado.", "La sangre de Cristo.", "Padres muertos.", "El arte de la seducción.",
    "Morir de difteria.",
    # Page 6
    "Mr. Musculo, justo detrás de ti.", "Imanes.", "Centros de madres.", "Chaparritas.", "Natalie Portman.",
    "Agricultura.", "Laura Bozzo.", "Sexo sorpresa!", "El plan de los homosexuales.", "Adal Ramones.",
    "La Conquista.", "Un giro de trama de M. Night Shyamalan.", "Rimas del corte.",
    "La luz de un billón de soles.", "Amputados.", "Arrojar una virgen a un volcán.", "Italianos.", "Explosiones.",
    "Una buena olfateada.", "Destruir la evidencia.",
    # Page 7
    "Niños en correas.", "Catapultas.", "Un trillón de dólares.", "Amigos con ventaja.", "Morir.", "Silencio.",
    "Hazte hombre!", "La base de datos de virus ha sido actualizada.", "Justin Bieber.", "La Sagrada Biblia.",
    "Cocos.", "Sanar lo gay con rezos.", "Embarazo adolescente.", "Porno alemán fetichista.", "La mano invisible.",
    "Mis demonios internos.", "Muslos poderosos.", "Empelotarse y mirar Nickelodeon.", "Deuda agobiante.",
    "Pilotos kamikaze.",
    # Page 8
    "Enseñarle a amar a un robot.", "Brutalidad policial.", "Carne de caballo.", "Promo 2x1 Tacos al Pastor.",
    "Heteronormatividad.", "Michael Jackson.", "Un gorro a la moda.", "Dar un agarrón.", "Pasta base.",
    "Cambia-formas.", "Masturbar con los dedos.", "Una fiesta de cumpleaños decepcionante.", "El Patriarcado.",
    "Mi alma.", "Fiestas de machos.", "Lo Crónico.", "Eugenesia.", "Soluciones de administración sinergística.",
    "RoboCop.", "Servidumbre.",
    # Page 9
    "Stephen Hawking hablando sucio.", "Un hombre al borde del orgasmo.", "Cagadera.", "Ridículo público.",
    "Limpia con huevo.", "Los obesos mórbidos.", "Condón atrapado.", "La Michoacana.", "Lady Tacos de Canasta.", "Vicente Fox.",
    "Tortugas bio-ingenierizadas con aliento ácido.", "Sueños húmedos.", "Bling bling.",
    "Disparar un rifle al aire mientras penetras a un cerdo.", "Sexo de llamas.", "Necrofilia.", "Profanar tumbas.",
    "Depilar el área del bikini.", "Ave María purísima, sin pecado concebida.", "Múltiples heridas por puñaladas.",
    # Page 10
    "El delicioso culo de Daniel Radcliffe.", "Un mono fumando un cigarro.", "Esmegma.", "Una audiencia en vivo.",
    "Hacer pucheros.", "La violación de nuestros mas básicos derechos humanos.", "Insondable estupidez.",
    "Amanecer y arcoíris.", "Sacudir el miembro.", "Supuesta diversidad cultural.", "Los terroristas.",
    "La constitución de 1980.", "Una tortuga caimán mordiéndote la punta del pene.",
    "Atropello vehicular con múltiples victimas.", "La Gran Depresión.", "Emociones.",
    "Enojarse tanto que generas una erección.", "Patinaje artístico del mismo sexo.", "Un rifle de asalto M16.",
    "Longaniza.",
    # Page 11
    "Incesto.", "Garabatero.", "Aves que no vuelan.", "Hacer lo correcto.",
    "Tirarse un eructo y que venga con sorpresa.", "Solamente la puntita.", "Ser mala onda con los niños.",
    "Pañales sucios.", "Ver a la abuela desnuda.", "Ataques de polillas.", "Hacer trampa en este juego.",
    "Esconder una erección.", "Desnudez frontal.", "Vigorosas manos de Jazz.", "Pezones de cuchillo.",
    "Una cachetada suave.", "Los brazos de Michelle Bachelet.", "Herpes en la boca.", "Un fisicoculturista peruano.",
    "Destrucción mutua asegurada.",
    # Page 12
    "El Rapto.", "El camino por delante.", "Stalin.", "Lactancia.", "El 27/F.",
    "El verdadero sentido de la Navidad.", "Auto-aversión.", "Un tumor cerebral.", "Bebes muertos.",
    "Música ranchera.", "Una detonación termonuclear.", "Gansos.", "Luis Jara.", "Dios.", "Un nerd espástico.",
    "Harry Potter erótico.", "Niños con cáncer anal.", "Fantasías con un bombero.", "El sueño americano.",
    "Pubertad.",
    # Page 13
    "Dulce, dulce venganza.", "Guiñarle el ojo a gente anciana.", "Las maravillas de Oriente.", "Oompa-Loompas.",
    "Autentica comida peruana.", "Preadolescentes.", "Papelucho.", "Un vibrador.", "Disfunción eréctil.",
    "Tener anos por ojos.", "El suave y brillante cuerpo del Guatón Salinas.", "Solos de saxofón.",
    "Minas antipersonales.", "Quedarse sin semen.", "Tiempo para mi.", "La Ley.", "Arresto ciudadano.",
    "El sur'e.", "Pulgares opuestos.", "Fantasmas.",
    # Page 14
    "Alcoholismo.", "Chistes malos y fuera de lugar acerca del Holocausto.", "Payas inapropiadas.",
    "Amputaciones de guerra.", "Exactamente lo que esperabas.", "Una paradoja de viaje en el tiempo.",
    "Desodorante AXE.", "La vida del pirata.", "Decir «Te amo».", "Una morena sexy.", "Ser un maldito hechicero.",
    "Ser un león depresivo de zoológico.", "Un macabro asesinato.", "Un cóndor con un sombrero.",
    "Tirarse un peo y huir del lugar.", "Un show de apareamiento.", "El equipo de gimnasia Chino.", "Fricción.",
    "Asiáticos malos para las matemáticas.", "El miedo en si mismo.",
    # Page 15
    "Castigos con la correa.", "Levadura.", "Cajita Feliz.", "Lamer cosas para reclamarlas como tuyas.",
    "Vikingos.", "El superhéroe Chocman.", "Queso caliente.", "Nicolas Cage.", "Un condón defectuoso.",
    "La inevitable muerte del universo por calentamiento.", "Unión Demócrata Independiente.", "Felipe Camiroaga.",
    "Porno de tentáculos.", "Cachalotes.", "Lady Gaga.", "La ira de Vladimir Putin.", "Hoyos de la gloria.",
    "Problemas paternales.", "Un mimo teniendo un infarto.", "Gente blanca.",
    # Page 16
    "Un vida de tristeza.", "Sensual escape de senos.", "Un océano de problemas.", "Nazis.",
    "Un cooler lleno de órganos.", "Dar el 110%.", "Hacerlo por atrás.", "Arturo Prat.",
    "Sostener un niño y tirarle un eructo en la cara.", "Un montaje de voleibol homoerotico.", "Cachorros!",
    "Alargamiento natural de masculinidad.", "Gente morena.",
    "Dejar caer un candelabro sobre tus enemigos y luego trepar por la cuerda.", "Sopa demasiado caliente.",
    "Sexo con Peter Rock.", "Inyecciones de hormonas.", "Sacarlo.", "El Big Bang.",
    "Comprar mercaderías en Superbodega aCuenta.",
    # Page 17
    "Dar a luz al Anticristo.", "Oscuras y misteriosas fuerzas fuera de nuestro control.", "Pancho Reyes.",
    "El tigre Tony.", "Billy y Mike.", "Sexo oral no recíproco.", "Raúl Hasbún.", "Gente guashita rica.",
    "Prepucio.", "Gente sin culo.", "El milagro de dar a luz.", "Esperar hasta el matrimonio.",
    "Dos enanos cagando en un tarro.", "Ritalín.", "Una lamentable masturbación manual.",
    "Hacer trampa en las Olimpiadas Especiales.", "Tejado de vidrio.", "El guatón Loyola.",
    "Miley Cyrus a los 55.", "Nuestro primer presidente chimpancé.",
    # Page 18
    "Comenzar a cantar y bailar de la nada.", "Un pistola de agua llena de pipi de gato.", "El Metro.",
    "Un video casero de Vivi Kreutzberger llorando sobre una cazuela.", "El pastor Soto.",
    "Pantalones extremadamente apretados.", "Grado 3.", "Despertar desnudo en medio de la Alameda.",
    "El frio, refrescante sabor de Pepsi.", "Merecer la cuna.", "Esperanza.", "Sacarte la polera.",
    "Sábanas con peste cristal.", "Limpieza étnica.", "Eructo vaginal.",
    "Reír sin poder hacer nada al escuchar el genocidio de Ruanda.", "Volarse demasiado.", "Selección natural.",
    "Un huemul gaseoso.", "Mi vida sexual.",
    # Page 19
    "Arnold Schwarzenegger.", "Pretender que te importa.", "Ricardo Lagos.", "La vagina de Pilar Sordo.",
    "Una cara fea.", "Mi negro trasero.", "Batman!!!", "Vagabundos.", "Preguntas racistas de la PSU.",
    "Centauros.", "Una sorpresa salada.", "72 vírgenes.", "Células madre embrionarias.", "Bukkake pixelado.",
    "Harakiri.", "Una lobotomía con un picahielos.", "Conexión humana genuina.", "Ira menstrual.",
    "Lluvia dorada.", "Un torrente eterno de diarrea.",
    # Page 20
    "La carrera de cantante de Iván Zamorano.", "Accidentes horribles por remoción de vello con laser.",
    "Auto canibalismo.", "Un feto.", "Cabalgar hacia el ocaso.", "Goblins.", "Comerse el ultimo bison.",
    "Objetos brillantes.", "Ser rico.", "Un emboque.", "Lepra.", "Paz mundial.", "Dedos de mantequilla.",
    "Manos de motosierra.", "La fundacion Make-a-Wish.", "Aliento a pene.", "Poner un huevo.",
    "La locura del hombre.", "Mis genitales.", "La abuela.",
    # Page 21
    "Bacteria come carne.", "Gente pobre.", "50.000 voltios directo a los pezones.", "Escucha activa.",
    "El superhombre.", "Malas decisiones de vida.", "Monaguillos.", "Mi vagina.",
    "Pac-Man tragando semen de forma incontrolable.", "Aspirar pegamento.", "La placenta.",
    "Los profundamente discapacitados.", "Combustión humana espontanea.", "El KKK.", "El clítoris.",
    "No usar pantalones.", "Sexo con consentimiento.", "Gente negra.", "Una cubeta de cabezas de pescado.",
    "Cuidados terminales.",
    # Page 22
    "Post-its pasivo agresivos.", "Whiskas.", "El corazón de un niño.", "Migas por toda la maldita alfombra.",
    "Tu extraño hermano.", "Ser gordo y estúpido.", "Casarse, tener hijos, comprar cosas, retirarse a Valparaíso y morir.",
    "Johnny Depp.", "Leonardo DiCaprio.", "Esperar un eructo y vomitar en el suelo.", "Labores de una esposa.",
    "Una pirámide de cabezas cercenadas.", "Genghis Khan.", "Universidades cota mil.", "Crucifixión.",
    "Una subscripción a Men's Health.", "El lechero.", "Fuego aliado.", "Voto femenino.", "SIDA.",
    # Page 23
    "Ex presidente.", "Onzas de heroína.", "Cachondeo a nalga pelada.", "Ropa interior comestible.",
    "Mi colección de juguetes sexuales de alta tecnología.", "La Fuerza.", "Abejas?",
    "Algo de maldita paz y tranquilidad.", "Masturbarse en una piscina llena de lagrimas de niños.",
    "Un cerdo enano con un pequeño abrigo y botitas.", "Tres penes al mismo tiempo.", "Masturbación.",
    "Tom Cruise.", "Un desayuno balanceado.", "Cuentas anales.", "Beber solo.", "Aborto vía colgador.",
    "Calzones usados.", "Acariciarse.",
    # Page 24
    "Limpiarle el culo.", "Mote con huesillos.", "Un completo al desayuno.", "La voz de Morgan Freeman.",
    "Un hombre de mediana edad en patines.", "Ghandi.", "El solo de flauta de «Todos juntos.»",
    "Abdominales espectaculares.", "Keanu Reeves.", "Rojo Fama contra Fama.", "Abuso de menores.",
    "Lindorfo.", "Ciencia.", "Una tribu de mujeres guerreras.", "Viagra.", "Su majestad, la reina Elizabeth II.",
    "La matanza vía tiroteo del año.", "Cobrar venganza.", "Una erección que dura mas de 4 horas.",
    # Bonus spicy & Latin memes
    "Un shot de tequila caliente.", "Chayanne en tanga.", "El удовлетворение de mandar a todos al carajo.",
    "Meter la pata hasta el fondo.", "Comer tacos en la calle a las 4 AM.", "El SAT tocando a tu puerta.",
    "Una bendición no planeada.", "La chancla voladora de mi mamá.", "Chabelo inmortal.",
    "Un grupo de WhatsApp de la familia a las 6 AM.", "Llorar en la regadera con rolas de José José.",
    "Decir 'la última y nos vamos'.", "El gansito congelado.", "Pagar en abonos chiquitos.",
    "Gritar '¡Viva México cabrones!'.", "Vender fotos de patas en OnlyFans."
]

black_cards_data = [
    # Page 25
    {"text": "¿Cómo perdí mi virginidad?", "pick": 1},
    {"text": "¿Por qué no puedo dormir en las noches?", "pick": 1},
    {"text": "¿Qué es ese olor?", "pick": 1},
    {"text": "Tengo 99 problemas pero ______ no es uno de ellos.", "pick": 1},
    {"text": "Tal vez ella nació con eso. Quizás es ______.", "pick": 1},
    {"text": "¿Cuál es el próximo juguete de la Cajita Feliz?", "pick": 1},
    {"text": "Acá está la Iglesia. Acá está el campanario. Abre las puertas y hay un ______.", "pick": 1},
    {"text": "Es una lástima que los niños estos días se estén involucrando con ______.", "pick": 1},
    {"text": "Hoy en el Diario de Eva: ¡Ayuda! ¡Mi hijo es/está ______!", "pick": 1},
    {"text": "La medicina alternativa está valorando los poderes curativos de ______.", "pick": 1},
    {"text": "Y el OSCAR a ______ es para ______.", "pick": 2},
    {"text": "¿Qué es ese ruido?", "pick": 1},
    {"text": "¿Qué hizo que terminara mi última relación?", "pick": 1},
    {"text": "El nuevo reality show tiene como protagonistas a 8 celebridades viviendo con ______.", "pick": 1},
    {"text": "Bebo para olvidar ______.", "pick": 1},
    {"text": "Lo siento profesor, no pude completar mi tarea porque ______.", "pick": 1},
    {"text": "¿Cuál es el placer culpable de Batman?", "pick": 1},
    {"text": "Este es el modo en que se acaba el mundo: no con una explosión, sino con ______.", "pick": 1},
    {"text": "¿Cuál es el mejor amigo de una mujer?", "pick": 1},
    {"text": "La DGAC ahora prohíbe ______ en los aviones.", "pick": 1},
    # Page 26
    {"text": "Y así es como quiero morir.", "pick": 1},
    {"text": "Para mi siguiente truco, sacaré ______ de ______.", "pick": 2},
    {"text": "En la nueva película original de Disney, Hannah Montana lucha contra ______ por primera vez.", "pick": 1},
    {"text": "______ es un camino peligroso que lleva a ______.", "pick": 2},
    {"text": "Lo conseguiré con un poco de ayuda de ______.", "pick": 1},
    {"text": "Querida Rosa, estoy teniendo algunos problemas con ______ y me gustaría tu consejo.", "pick": 1},
    {"text": "En vez de carbón, el Viejito Pascuero ahora les da ______ a los niños malos.", "pick": 1},
    {"text": "¿Qué es lo más emo?", "pick": 1},
    {"text": "En 1.000 años cuando el dinero sea un recuerdo distante, ¿con qué pagaremos por bienes y servicios?", "pick": 1},
    {"text": "Presentando al increíble dúo de superhéroe y ayudante: ¡Son ______ y ______!", "pick": 2},
    {"text": "En la nueva película de M. Night Shyamalan, Bruce Willis descubre que realmente ha sido ______ todo el tiempo.", "pick": 2},
    {"text": "Una romántica cena a la luz de las velas no estaría completa sin ______.", "pick": 1},
    {"text": "¡Apuesto a que no puedes solo con uno!", "pick": 1},
    {"text": "A la gente fresa le gusta ______.", "pick": 1},
    {"text": "Dame esos 5.", "pick": 1},
    {"text": "Próximamente de J.K. Rowling: Harry Potter y la Cámara de ______.", "pick": 1},
    {"text": "¡Presentando Fútbol Xtreme! Es como el fútbol, pero con ______.", "pick": 1},
    {"text": "En un mundo destrozado por ______, nuestro único consuelo es ______.", "pick": 2},
    {"text": "¡Guerra! ¿Para qué nos sirve?", "pick": 1},
    {"text": "Durante el sexo, me gusta pensar en ______.", "pick": 1},
    # Page 27
    {"text": "¿Qué me están escondiendo mis padres?", "pick": 1},
    {"text": "¿Qué es lo que siempre resulta para acostarte con alguien?", "pick": 1},
    {"text": "En Reclusorio Norte, se dice que puedes cambiar 200 cigarros por ______.", "pick": 1},
    {"text": "¿Qué me traje de vuelta desde Uruguay?", "pick": 1},
    {"text": "¿Qué no te gustaría encontrar en tu pozole?", "pick": 1},
    {"text": "¿Qué traería de vuelta en el tiempo para convencer a la gente de que soy un poderoso hechicero?", "pick": 1},
    {"text": "¿Cómo estoy manteniendo el estado de mi relación?", "pick": 1},
    {"text": "¡Es una trampa!", "pick": 1},
    {"text": "Llegando a Broadway esta temporada: ______: El musical.", "pick": 1},
    {"text": "Mientras EEUU competía con la URSS en la carrera espacial, el gobierno mexicano invirtió millones en la investigación de ______.", "pick": 1},
    {"text": "Después del terremoto, Carlos Slim le llevó ______ a la gente de Iztapalapa.", "pick": 1},
    {"text": "A continuación en ESPN: La Serie Mundial de ______.", "pick": 1},
    {"text": "1° paso: ______ | 2° paso: ______ | 3° paso: ¡Ganancia!", "pick": 2},
    {"text": "Dijeron que estábamos locos. Dijeron que no podíamos meter ______ dentro de ______. Estaban equivocados.", "pick": 2},
    {"text": "... Pero antes de matarlo Sr. Bond, debo mostrarle ______.", "pick": 1},
    {"text": "¿Qué me causa pedos incontrolables?", "pick": 1},
    {"text": "La nueva Chevrolet Tahoe. Con el poder y espacio para llevar ______ a donde quieras.", "pick": 1},
    {"text": "El paseo de curso se arruinó completamente por culpa de ______.", "pick": 1},
    {"text": "Cuando el Faraón no cedió, Moisés invocó una plaga de ______.", "pick": 1},
    {"text": "¿Cuál es mi poder secreto?", "pick": 1},
    # Page 28
    {"text": "¿De qué hay una tonelada en el cielo?", "pick": 1},
    {"text": "¿Qué cosa encontraría la abuela perturbadora, pero extrañamente encantadora?", "pick": 1},
    {"text": "Nunca entendí realmente ______ hasta que encontré ______.", "pick": 2},
    {"text": "¿Qué le entregó la ONU a los niños de Siria vía entrega aérea?", "pick": 1},
    {"text": "¿Qué ayuda a Facundo a soltar sus gases?", "pick": 1},
    {"text": "¿Qué comió Vin Diesel en la cena?", "pick": 1},
    {"text": "______: bueno hasta la última gota.", "pick": 1},
    {"text": "¿Por qué estoy pegajoso/a?", "pick": 1},
    {"text": "¿Qué mejora con los años?", "pick": 1},
    {"text": "Probado con niños, aprobado por madres: ______.", "pick": 1},
    {"text": "Papi, ¿por qué está llorando mamá?", "pick": 1},
    {"text": "¿Qué están usando los profesores en los colegios de escasos recursos para motivar a sus alumnos?", "pick": 1},
    {"text": "Un reciente estudio demuestra que los jóvenes tienen 50% menos sexo luego de ser expuestos a ______.", "pick": 1},
    {"text": "La vida de los indígenas cambió para siempre cuando los españoles les presentaron ______.", "pick": 1},
    {"text": "Haz un Haiku.", "pick": 3, "draw": 2},
    {"text": "No sé con qué armas se peleará la tercera guerra mundial, pero la cuarta se peleará con ______.", "pick": 1},
    {"text": "¿Por qué me duele todo el cuerpo?", "pick": 1},
    {"text": "¿Qué estoy dejando por la Cuaresma?", "pick": 1},
    {"text": "¿Sobre qué está pensando AMLO en estos momentos?", "pick": 1},
    {"text": "El Museo de Historia Natural abrió una exhibición interactiva de ______.", "pick": 1},
    # Page 29
    {"text": "Cuando sea presidente, crearé el Departamento de ______.", "pick": 1},
    {"text": "La Rosa de Guadalupe presenta: «______, la historia de ______».", "pick": 2},
    {"text": "Cuando sea un billonario, construiré una estatua de 20 metros conmemorando ______.", "pick": 1},
    {"text": "Cuando estaba en ácido, ______ se transformó en ______.", "pick": 2},
    {"text": "Es cierto, maté a ______. ¿Cómo preguntas? ______.", "pick": 2},
    {"text": "¿Qué es mi anti-droga?", "pick": 1},
    {"text": "______ + ______ = ______.", "pick": 3, "draw": 2},
    {"text": "¿Qué nunca falla en alegrar la fiesta?", "pick": 1},
    {"text": "¿Cuál es la nueva dieta de moda?", "pick": 1},
    {"text": "¡Consejo! Cuando tu pareja te pida que bajes, trata de sorprenderle con ______ en cambio.", "pick": 1},
    # Bonus spicy
    {"text": "Mi terapeuta dice que la raíz de todos mis traumas es ______.", "pick": 1},
    {"text": "No hay nada más caliente que susurrarle al oído: «______».", "pick": 1},
    {"text": "El verdadero secreto para ganar en la vida no es trabajar duro, es ______.", "pick": 1},
    {"text": "En mi funeral no quiero flores, quiero ______.", "pick": 1},
    {"text": "Cosas que jamás deberías meterte por la nariz: ______.", "pick": 1}
]

white_cards = []
for i, text in enumerate(white_cards_raw, 1):
    white_cards.append({
        "id": f"w_{i}",
        "text": text.strip(),
        "type": "white"
    })

black_cards = []
for i, item in enumerate(black_cards_data, 1):
    black_cards.append({
        "id": f"b_{i}",
        "text": item["text"].strip(),
        "pick": item.get("pick", 1),
        "draw": item.get("draw", 0),
        "type": "black"
    })

data = {
    "whiteCards": white_cards,
    "blackCards": black_cards
}

with open("Data/cards_database.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Generated {len(white_cards)} white cards and {len(black_cards)} black cards.")
