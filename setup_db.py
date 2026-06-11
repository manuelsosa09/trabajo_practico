import sqlite3
from auth import hash_password

conn = sqlite3.connect("music_store.db")
cursor = conn.cursor()

# Crear tablas
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT UNIQUE NOT NULL,
    contraseña TEXT NOT NULL,
    avatar TEXT,
    biografia TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS instrumentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    imagen TEXT,
    categoria TEXT,
    historia TEXT,
    material TEXT,
    origen TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS favoritos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    instrumento_id INTEGER
)

""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS comentarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    id_instrumento INTEGER,
    comentario TEXT,
    fecha TEXT
)
""")

# Usuario Manuel
try:
    cursor.execute("INSERT INTO usuarios (nombre, correo, contraseña) VALUES (?, ?, ?)",
                   ("Manuel", "cristaldom095@gmail.com", hash_password("12345")))
except:
    pass

instrumentos = [
    (
        "Guitarra Clásica",
        "assets/images/guitarra_clasica.png",
        "Cuerda",
        "La guitarra clásica surgió en España entre los siglos XVIII y XIX y se convirtió en uno de los instrumentos más usados en música académica y popular. Hoy se emplea tanto en recitales solistas como en música de cámara, folclore y arreglos modernos.",
        "Cuerpo de madera (cedro o abeto), diapasón de ébano y cuerdas de nailon.",
        "España"
    ),
    (
        "Piano",
        "assets/images/piano.png",
        "Teclado",
        "El piano apareció a inicios del siglo XVIII como evolución del clavicémbalo, permitiendo controlar la intensidad del sonido mediante la presión de las teclas. Es uno de los instrumentos más versátiles, presente en la música clásica, el jazz, el pop y la banda sonora de cine.",
        "Caja de resonancia de madera, cuerdas de acero y mecanismo de martillos cubiertos de fieltro.",
        "Italia"
    ),
    (
        "Batería",
        "assets/images/bateria.png",
        "Percusión",
        "La batería moderna se desarrolló a inicios del siglo XX al combinar distintos tambores y platillos en un solo set para un solo intérprete. Es el motor rítmico de estilos como el rock, el jazz, el funk y el pop, marcando el pulso y los cambios de energía.",
        "Cascos de madera o metal con parches sintéticos y platillos de aleaciones de metal.",
        "Estados Unidos"
    ),
    (
        "Violín",
        "assets/images/violin.png",
        "Cuerda",
        "El violín tomó su forma actual en el siglo XVI y es clave en la orquesta clásica, la música de cámara y muchas tradiciones populares. Su gran expresividad lo hace ideal tanto para melodías delicadas como para pasajes virtuosos muy rápidos.",
        "Cuerpo de madera (abeto y arce), diapasón de ébano y cuerdas metálicas o sintéticas.",
        "Italia"
    ),
    (
        "Flauta Traversera",
        "assets/images/flauta_traversa.png",
        "Viento",
        "La flauta traversera pasó de ser de madera a metal en el siglo XIX, ganando afinación estable y proyección sonora para uso en banda y orquesta. Se utiliza en música clásica, bandas sonoras y también en fusiones con jazz y música popular.",
        "Tubo cilíndrico de metal (normalmente plata, níquel o aleaciones) con llaves mecánicas.",
        "Europa"
    ),
    (
        "Trompeta",
        "assets/images/trompeta.png",
        "Viento",
        "La trompeta se utiliza desde la antigüedad como instrumento ceremonial y militar; la trompeta moderna con pistones se consolidó en el siglo XIX. Destaca por su sonido brillante y potente, muy presente en orquestas, jazz, bandas y música latina.",
        "Tubo metálico enrollado, generalmente de latón, con campana y tres pistones.",
        "Europa"
    ),
    (
        "Saxofón",
        "assets/images/saxofon.png",
        "Viento",
        "El saxofón fue inventado por Adolphe Sax en el siglo XIX y se hizo famoso en el jazz, las bandas militares y la música popular. Su timbre cálido y flexible le permite adaptarse a baladas, solos virtuosos y líneas melódicas muy expresivas.",
        "Cuerpo de latón con llaves y boquilla con caña simple de madera.",
        "Bélgica"
    ),
    (
        "Clarinete",
        "assets/images/clarinete.png",
        "Viento",
        "El clarinete apareció a inicios del siglo XVIII y se consolidó como instrumento fundamental en la orquesta, la banda sinfónica y el jazz tradicional. Es capaz de producir desde notas muy graves y oscuras hasta registros agudos brillantes y ligeros.",
        "Cuerpo de madera (generalmente granadillo) o plástico, con llaves metálicas y boquilla con caña simple.",
        "Alemania"
    ),
    (
        "Guitarra Eléctrica",
        "assets/images/guitarra_electrica.png",
        "Cuerda",
        "La guitarra eléctrica surgió en la década de 1930 y revolucionó la música popular, siendo esencial en el rock, el blues y el pop. Combinada con amplificadores y efectos, puede generar una enorme variedad de sonidos y estilos.",
        "Cuerpo macizo de madera, pastillas magnéticas, cuerdas de acero y herrajes metálicos.",
        "Estados Unidos"
    ),
    (
        "Contrabajo",
        "assets/images/contrabajo.png",
        "Cuerda",
        "El contrabajo es el instrumento de cuerda frotada más grave de la orquesta y se usa también en jazz, tango y otras músicas populares. Sostiene la base armónica y rítmica, acompañando tanto a pequeños conjuntos como a grandes orquestas.",
        "Cuerpo de madera de gran tamaño, diapasón de ébano y cuerdas metálicas entorchadas.",
        "Italia"
    ),
    (
        "Arpa",
        "assets/images/arpa.png",
        "Cuerda",
        "El arpa tiene raíces muy antiguas y en su versión moderna de pedales es un instrumento emblemático de la orquesta y la música solista. Su sonido etéreo se asocia a pasajes líricos, glissandos y atmósferas suaves y brillantes.",
        "Estructura de madera, caja de resonancia vertical y numerosas cuerdas de nailon, metal o tripa.",
        "Irlanda"
    ),
    (
        "Oboe",
        "assets/images/oboe.png",
        "Viento",
        "El oboe fue desarrollado a partir del shawm barroco y hoy es conocido por su timbre penetrante y expresivo dentro de la orquesta. Muchas obras sinfónicas confían al oboe solos emotivos y líneas melódicas muy cantables.",
        "Cuerpo de madera con llaves metálicas y una lengüeta doble de caña.",
        "Francia"
    ),
    (
        "Fagot",
        "assets/images/fagot.png",
        "Viento",
        "El fagot es el bajo de la familia de maderas y aporta un color grave y cálido tanto en la orquesta como en la música de cámara. Puede sonar serio y profundo, pero también es usado para pasajes cómicos y personajes graciosos.",
        "Cuerpo de madera seccionado en varias partes, tudel metálico y lengüeta doble de caña.",
        "Alemania"
    ),
    (
        "Xilófono",
        "assets/images/xilofono.png",
        "Percusión",
        "El xilófono está formado por láminas afinadas que se golpean con baquetas y se utiliza en orquesta, banda y música educativa. Es ideal para aprender melodías básicas y para crear efectos brillantes y rítmicos.",
        "Láminas de madera dura montadas sobre un bastidor, a veces con resonadores metálicos.",
        "África"
    ),
    (
        "Timbales",
        "assets/images/timbales.png",
        "Percusión",
        "Los timbales sinfónicos evolucionaron a partir de tambores de caballería y hoy son esenciales en la percusión orquestal. Permiten afinar notas concretas y realizar redobles y golpes que enfatizan momentos clave de la música.",
        "Caldos metálicos semiesféricos con parches sintéticos o de cuero y sistema de afinación por pedal.",
        "España"
    ),
    (
        "Marimba",
        "assets/images/marimba.png",
        "Percusión",
        "La marimba tiene raíces africanas y se desarrolló fuertemente en América, especialmente en México y Centroamérica. Su sonido cálido y envolvente la hace perfecta para repertorio solista, música de cámara y arreglos modernos.",
        "Láminas de madera afinadas con resonadores tubulares debajo.",
        "África"
    ),
    (
        "Ukelele",
        "assets/images/ukelele.png",
        "Cuerda",
        "El ukelele se popularizó en Hawái a finales del siglo XIX y hoy es muy usado en música ligera y acompañamiento vocal. Es pequeño, fácil de transportar y accesible para quienes dan sus primeros pasos en la música.",
        "Cuerpo pequeño de madera y cuatro cuerdas de nailon.",
        "Hawái"
    ),
    (
        "Banjo",
        "assets/images/banjo.png",
        "Cuerda",
        "El banjo tiene origen en instrumentos africanos llevados a América y es típico del bluegrass, el folk y el country. Su timbre brillante y percusivo destaca en patrones rítmicos rápidos y acompañamientos enérgicos.",
        "Aro circular con parche tensado, mástil de madera y cuerdas metálicas.",
        "Estados Unidos"
    ),
    (
        "Harmónica",
        "assets/images/harmonica.png",
        "Viento",
        "La armónica se difundió en el siglo XIX y es muy usada en blues, rock y música popular por su sonido expresivo y portátil. Muchos músicos la llevan en el bolsillo para improvisar melodías y acompañamientos en cualquier lugar.",
        "Pequeño cuerpo de metal o plástico con lengüetas metálicas internas.",
        "Alemania"
    ),
    (
        "Acordeón",
        "assets/images/acordeon.png",
        "Viento",
        "El acordeón apareció en el siglo XIX y se volvió fundamental en músicas tradicionales europeas y latinoamericanas. Su combinación de fuelle, botones y teclas permite tocar melodías, acordes y bajos al mismo tiempo.",
        "Cajas de madera y metal unidas por un fuelle, con botones o teclas y lengüetas libres internas.",
        "Italia"
    ),
    (
        "Chelo",
        "assets/images/chelo.png",
        "Cuerda",
        "El chelo, o violonchelo, surgió en el siglo XVI y ocupa el registro grave dentro de la familia del violín. Es apreciado por su sonido cálido y cercano a la voz humana, muy usado en conciertos solistas y música de cámara.",
        "Cuerpo grande de madera, cuerdas metálicas y arco de crin.",
        "Italia"
    ),
    (
        "Viola",
        "assets/images/viola.png",
        "Cuerda",
        "La viola es ligeramente más grande que el violín y tiene un tono más oscuro y melancólico. En la orquesta ocupa un papel intermedio entre violines y chelos, añadiendo profundidad al conjunto.",
        "Cuerpo de madera, cuerdas metálicas y arco.",
        "Italia"
    ),
    (
        "Trombón",
        "assets/images/trombon.png",
        "Viento",
        "El trombón destaca por su vara deslizante, utilizada en orquesta, jazz y bandas sinfónicas. Puede producir glissandos muy característicos y pasar de sonidos suaves a ataques muy potentes.",
        "Tubo de latón largo y campana metálica.",
        "Europa"
    ),
    (
        "Tuba",
        "assets/images/tuba.png",
        "Viento",
        "La tuba es el instrumento más grave de los metales y aporta la base armónica en orquestas y bandas. Su gran tamaño permite producir notas profundas que sostienen el resto de la sección.",
        "Tubo de latón de gran tamaño con pistones.",
        "Europa"
    ),
    (
        "Corneta",
        "assets/images/corneta.png",
        "Viento",
        "La corneta es similar a la trompeta y se usa frecuentemente en bandas militares y de desfile. Su sonido penetrante sirve para llamadas, señales y melodías breves y claras.",
        "Tubo de latón enrollado con boquilla cónica.",
        "Inglaterra"
    ),
    (
        "Ocarina",
        "assets/images/ocarina.png",
        "Viento",
        "La ocarina es un instrumento ancestral usado en culturas de Mesoamérica y Asia y se hizo popular también en videojuegos y música contemporánea. Su sonido suave y dulcemente afinado la vuelve ideal para melodías simples.",
        "Cuerpo de cerámica, madera o plástico perforado.",
        "Mesoamérica"
    ),
    (
        "Flauta Dulce",
        "assets/images/flauta_dulce.png",
        "Viento",
        "La flauta dulce es muy usada en educación musical por su sencillez de digitación y costo accesible. También tiene repertorio propio de la música antigua y se interpreta en conjuntos especializados.",
        "Cuerpo de plástico o madera con orificios.",
        "Europa"
    ),
    (
        "Bandoneón",
        "assets/images/bandoneon.png",
        "Viento",
        "El bandoneón es esencial en el tango argentino y tiene un sonido muy expresivo y nostálgico. Su mecanismo de fuelle y botones permite complejas armonías y melodías entrelazadas.",
        "Fuelle de cuero, botones y lengüetas metálicas internas.",
        "Alemania / Argentina"
    ),
    (
        "Charango",
        "assets/images/charango.png",
        "Cuerda",
        "El charango es un cordófono andino tradicional usado en música folclórica de Bolivia, Perú y el norte de Argentina. Su timbre agudo acompaña zambas, huaynos y otros ritmos de la región.",
        "Cuerpo de madera (originalmente caparazón de armadillo) y cuerdas metálicas.",
        "Andes"
    ),
    (
        "Mandolina",
        "assets/images/mandolina.png",
        "Cuerda",
        "La mandolina es un instrumento de cuerda pulsada muy usado en bluegrass, música italiana y repertorio barroco. Sus dobles cuerdas y su ataque rápido producen un sonido brillante y chispeante.",
        "Cuerpo de madera en forma de lágrima con cuerdas metálicas dobles.",
        "Italia"
    ),
    (
        "Sitar",
        "assets/images/sitar.png",
        "Cuerda",
        "El sitar es un instrumento representativo de la música clásica del norte de India y se reconoce por su sonido resonante y lleno de armónicos. Se emplea en ragas extensas que exploran diferentes modos y emociones.",
        "Cuerpo de calabaza y madera con muchas cuerdas simpáticas.",
        "India"
    ),
    (
        "Laúd",
        "assets/images/laud.png",
        "Cuerda",
        "El laúd fue muy popular en Europa durante el Renacimiento y el Barroco, utilizado para acompañar canciones y piezas instrumentales. Hoy se interpreta en conjuntos de música antigua y proyectos históricos.",
        "Cuerpo abombado de madera y numerosas cuerdas.",
        "Europa"
    ),
    (
        "Cajón Peruano",
        "assets/images/cajon_peruano.png",
        "Percusión",
        "El cajón peruano es un instrumento afroperuano ampliamente usado en flamenco y música latina moderna. Produce graves profundos y agudos secos, y se toca sentado encima golpeando la tapa frontal.",
        "Caja de madera hueca con tapa delantera percutida.",
        "Perú"
    ),
    (
        "Bongó",
        "assets/images/bongo.png",
        "Percusión",
        "El bongó es un instrumento afrocubano compuesto por dos pequeños tambores unidos de diferente tamaño. Se utiliza en son, salsa y otros estilos caribeños para crear patrones rápidos y sincopados.",
        "Cascos de madera con parches tensados.",
        "Cuba"
    ),
    (
        "Congas",
        "assets/images/congas.png",
        "Percusión",
        "Las congas son tambores altos utilizados en salsa, rumba y música latina en general. Tienen técnicas específicas de mano que permiten obtener distintos tonos y golpes.",
        "Cuerpos de madera o fibra con parches amplios.",
        "Cuba"
    ),
    (
        "Triángulo",
        "assets/images/triangulo.png",
        "Percusión",
        "El triángulo es un pequeño idiófono metálico usado en orquestas, bandas y música popular. Su sonido brillante resalta fácilmente sobre el resto de la agrupación, incluso con un solo golpe.",
        "Barra de acero doblada en forma triangular.",
        "Europa"
    ),
    (
        "Kalimba",
        "assets/images/kalimba.png",
        "Percusión",
        "La kalimba es un instrumento africano tocado con los pulgares, también llamado piano de mano. Produce un sonido dulce y relajante, ideal para patrones repetitivos y acompañamientos suaves.",
        "Caja de resonancia de madera con láminas metálicas.",
        "África"
    ),
    (
        "Pandereta",
        "assets/images/pandereta.png",
        "Percusión",
        "La pandereta es común en música folclórica, religiosa y popular por su mezcla de parche y sonajas metálicas. Se puede sacudir, golpear o raspar, generando diferentes matices rítmicos.",
        "Aro de madera o plástico con sonajas metálicas.",
        "Europa"
    ),
    (
        "Gaita Gallega",
        "assets/images/gaita_gallega.png",
        "Viento",
        "La gaita gallega es un instrumento tradicional del noroeste de España, protagonista en fiestas y procesiones. Su sonido penetrante y continuo acompaña danzas, marchas y melodías folclóricas.",
        "Bolsa de aire de cuero y tubos de madera.",
        "España"
    ),
    (
        "Armonio",
        "assets/images/armonio.png",
        "Teclado",
        "El armonio es un instrumento de teclado con fuelle muy usado en la música clásica india y en contextos religiosos. Su sonido continuo y cálido permite acompañar cantos, ragas y himnos.",
        "Caja de madera con fuelle y lengüetas libres.",
        "India"
    ),
]



for instr in instrumentos:
    try:
        cursor.execute("""
        INSERT INTO instrumentos (nombre, imagen, categoria, historia, material, origen)
        VALUES (?, ?, ?, ?, ?, ?)
        """, instr)
    except:
        pass

conn.commit()
conn.close()
print("Base de datos lista con usuario y 40 instrumentos.")
