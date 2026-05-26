={
  "MERCURY": "{{ (() => {
  const respuestas = [
    $('Edit Fields').item.json['¿Con qué centro o instructor realizaste tu primer curso?'],
    $('Edit Fields').item.json['¿En qué ciudad has hecho el curso?'],
    $('Edit Fields').item.json['¿Con qué centro o instructor realizaste tu primer curso ONE?']
  ];
  
  const primerCurso = ($('Edit Fields').item.json['¿Cuál es el primer curso que has hecho con nosotros?'] || '').toLowerCase();

  const mapaCiudades = {
    'Zaragoza (Laura Revilla)': 'Zaragoza Laura',
    'Barcelona (Marco Bevanati)': 'Barcelona Marco',
    "Barcelona (Michele D'Antino)": 'Barcelona Michele',
    'Palma de mallorca (Magdalena Meliá)': 'Mallorca Magdalena',
    'Palma de Mallorca (Giulia Barci)': 'Mallorca Giulia',
    'Málaga (Margherita Vattimo)': 'Malaga Margherita',
    'Sevilla (Alessandro Fornelli)': 'Sevilla Alessandro',
    'Valencia (Filippo Bruni)': 'Valencia Filippo',
    'Valencia (Beatriz Castro)': 'Valencia Beatriz',
    'Madrid (Theo Scacchi / Natalia Salto)': 'Madrid Theo Natalia',
    'Madrid (Valerio Sepe)': 'Madrid Valerio',
    'Madrid (Lucrezia Vattimo)': 'Madrid Lucrezia',
    'Alicante (Emilia Valero)': 'Alicante Emilia',
    'Granada (Fátima Cano)': 'Granada Fátima',
    'Bilbao (María Calero)': 'Bilbao María',
    'San Sebastián (Naiara Parra)': 'San Sebastián Naiara',
    'Pamplona (Elisabeth Tornos)': 'Pamplona Elisabeth'
  };

  const respuesta = respuestas.find(r => r && mapaCiudades[r.trim()]);
  const esCursoValido = primerCurso.includes('genial business') || primerCurso.includes('30 dias 1 idioma');

  return (respuesta || esCursoValido) ? '✅' : '❌';
})() }}",



 "INSTRUCTOR": "{{ 
    (() => {
      const respuestas = [
        $('Edit Fields').item.json['¿Con qué centro o instructor realizaste tu primer curso?'],
        $('Edit Fields').item.json['¿En qué ciudad has hecho el curso?'],
        $('Edit Fields').item.json['¿Con qué centro o instructor realizaste tu primer curso ONE?']
      ];
      
      const respuesta = respuestas.find(r => r && r.trim() !== '') || '';

      const mapaCiudades = {
        'Zaragoza (Laura Revilla)': 'Zaragoza Laura',
        'Barcelona (Marco Bevanati)': 'Barcelona Marco',
        'Palma de mallorca (Magdalena Meliá)': 'Mallorca Magdalena',
        'Málaga (Margherita Vattimo)': 'Malaga Margherita',
        'Sevilla (Alessandro Fornelli)': 'Sevilla Alessandro',
        'Valencia (Filippo Bruni)': 'Valencia Filippo',
        'Valencia (Beatriz Castro)': 'Valencia Beatriz',
        'Madrid (Theo Scacchi / Natalia Salto)': 'Madrid Theo Natalia',
        'Madrid (Valerio Sepe)': 'Madrid Valerio',
        'Madrid (Lucrezia Vattimo)': 'Madrid Lucrezia',
        'Alicante (Emilia Valero)': 'Alicante Emilia',
        'Granada (Fátima Cano)': 'Granada Fátima',
        'Bilbao (María Calero)': 'Bilbao María',
        'San Sebastián (Naiara Parra)': 'San Sebastián Naiara',
        'Pamplona (Elisabeth Tornos)': 'Pamplona Elisabeth'
      };

      return mapaCiudades[respuesta] || '';
    })()
  }}",

  "APELLIDOS Y NOMBRE": "{{ [ $('Edit Fields').item.json.Apellidos, $('Edit Fields').item.json.Nombre ].filter(Boolean).join(', ') }}",
  "NOMBRE": "{{ $('Edit Fields').item.json.Nombre }}",
  "CONTACTO": "{{ $('Edit Fields').item.json['Numero de contacto'] }}",
  "CORREO": "{{ $('Edit Fields').item.json['Correo'] }}",
  "EDAD": "{{
    (() => {
      const fecha = $('Edit Fields').item.json['Fecha de nacimiento'] || '';
      if (!fecha) return '';
      const parts = fecha.split('/');
      if (parts.length !== 3) return '';
      const nacimiento = new Date(parts[2], parts[1] - 1, parts[0]); 
      const hoy = new Date();
      let edad = hoy.getFullYear() - nacimiento.getFullYear();
      const m = hoy.getMonth() - nacimiento.getMonth();
      if (m < 0 || (m === 0 && hoy.getDate() < nacimiento.getDate())) edad--;
      return edad;
    })()
  }}",

  "PROXIMOS EVENTOS": "{{ 
(() => {
  const r1 = ($('Edit Fields').item.json['¿Quieres que te informemos de eventos?'] || '').toLowerCase().trim();
  const r2 = ($('Edit Fields').item.json['¿Quieres que te vayamos informando de eventos que vamos haciendo a lo largo del tiempo?'] || '').toLowerCase().trim();

  const afirmativos = ['si', 'sí'];

  if (afirmativos.includes(r1) || afirmativos.includes(r2)) return '✅';
  return '❌';
})()
}}",

"1* CURSO": "{{ 
(() => { 
  const campos = ['¿Cuál es el primer curso que has hecho con nosotros?', '¿Con qué centro o instructor realizaste tu primer curso ONE?', '¿Cuál es el primer curso que has hecho con nosotros?'];
  const v = campos.map(c => $json[c] || '').find(v => v.trim() !== '') || '';
  const t = v.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim();
  if (t.includes('genius')) return '🧠';
  if (t.includes('30 dias') || t.includes('30 días')) return '30 🌍';
  if (t.includes('genial business') || t.includes('general business') || t.includes('business')) return '💼';
  if (t.includes('one')) return '🔥✅';
  return '🚪Vendible';
})()
}}",

  "MES": "{{ new Date().toLocaleString('es-ES', { month: 'long' }) }}",
  "AÑO": "{{ new Date().getFullYear() }}",
  "MODALIDAD": "{{ $('Edit Fields').item.json["Has conocido el curso por"] }}",
  "TERMINAL ESTABLE": "{{ 
    $('Edit Fields').item.json['¿Quién es tu TUTOR?'] || 
    $('Edit Fields').item.json['¿Quién es el TUTOR de tu hijo/hija?'] || 
    ''
  }}",
  "CIUDAD": "{{ $('Edit Fields').item.json['¿En qué ciudad vives?'] || '' }}",




  "COMENTARIO": "________________TRABAJO Y ESTUDIO_____________________",

  "PROFESIÓN": "{{ $('Edit Fields').item.json['¿A qué te dedicas actualmente?'] || '' }}",
  "Nivel": "{{ $('Edit Fields').item.json['¿Qué tipo de curso estudias?'] }}",
  "Tipo": "{{ $('Edit Fields').item.json['¿Qué tipo de curso es?'] }}",
  "Año": "{{ $('Edit Fields').item.json['¿En qué año estas?'] }}",
  "STATUS 🚦": "🚪Vendible",




  "COMENTARIO": "________________CURSOS_____________________",

 "16K": "❌",

  "SSA": "{{ (() => {
  const cursosRaw = $('Edit Fields').item.json['¿Cuáles son los cursos que has hecho o vas a hacer con nosotros?'] || '';
  const cursos = cursosRaw.toLowerCase();
  const edadRaw = $('Edit Fields').item.json['EDAD'] || $('Edit Fields').item.json['Edad'] || '';
  const edad = parseInt(String(edadRaw).replace(/\D/g, '')) || 0;

  const haHechoSSA = cursos.includes('he hecho la soft skills academy');
  const estaCursandoSSA = cursos.includes('estoy haciendo la soft skills academy');

  if (haHechoSSA) return '🏁 Acabado';
  if (estaCursandoSSA) return '🎓 Actualmente Skiller';

  if (edad >= 18 && edad <= 25) return '🚪 Vendible';
  return 'NoInTarget'; })()}}",



  "COMENTARIO": "________________CURSOS PRINCIPALES_____________________",


  "GENIUS": "{{ (() => {
  const cursos = String($json['¿Cuáles son los cursos que has hecho o vas a hacer con nosotros?'] || '');
  const haHechoRaw = $json['Has hecho el curso para'] || '';
  const haHecho = haHechoRaw
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .trim()
    .toLowerCase();

  if (haHecho === 'conseguir objetivos de estudio') return '✅ REALIZADO';
  if (haHecho === 'acompanar a mi hijo/hija') return '🦮 ACOMPAÑANTE';

  if (
    haHecho === 'acompanar a mi hijo/hija y quizas aprender algo yo tambien' ||
    haHecho === 'acompanar a mi hijo/hija y aprender algo tambien'
  ) return '🦮💡 ACOMPAÑANTE INTERESADO';

  if (haHecho === 'aprender idiomas') return '🌎 X IDIOMA';

  if (
    cursos.includes('He hecho el curso Genius como ALUMNO') ||
    cursos.includes('He hecho el curso como alumno')
  ) return '✅ REALIZADO';

  if (cursos.includes('He hecho el curso como padre/madre acompañante')) return '🦮 ACOMPAÑANTE';

  if (
    cursos.includes('Estoy apuntado al curso Genius') ||
    cursos.includes('Estoy Apuntado al curso Genius')
  ) return '✍️';

  const metodo = $json['Área interés método aprendizaje'] || '';
  if (metodo === '4 – Me interesa' || metodo === '5 – Me interesa mucho') return '💡';

  return '🚪 VENDIBLE';
})() }}",





  "30_dias_1_idioma": "{{ (() => {
  const haHecho = String($json['Has hecho el curso para'] || '');
  const cursos = String($json['¿Cuáles son los cursos que has hecho o vas a hacer con nosotros?'] || '');
  const pendiente = $json['¿Tienes pendiente aprender un idioma?'] || '';
  const interes = $json['Área interés idioma en 30 días'] || '';

  if (haHecho === 'Aprender Idiomas') return '🧠 X GENIUS';

  if (cursos.includes('He finalizado el protocolo de 30 dias 1 idioma')) return '✅ REALIZADO';
  if (cursos.includes('Estoy Siguiendo el protocolo de 30 dias 1 idioma')) return '✍️ EN CURSO';

  if (
    cursos.includes('Estoy siguiendo el protocolo de 30 días 1 idioma') ||
    cursos.includes('He finalizado el protocolo de 30 días 1 idioma')
  ) return '💰 YA VENDIDO';

  if (pendiente === 'Si' || pendiente === 'Sí') return '🚪 VENDIBLE';

  if (interes === '5 – Me interesa mucho' || interes === '4 – Me interesa') return '📌 INTERESADO';
  if (interes === '3 – Podría interesarme') return 'PENDIENTE';
  if (interes === '2 – Poco' || interes === '1 – Muy poco') return '❌ NO INTERESADO';
  if (interes === '0 – Nada de interés') return '🚫 RECHAZADO';

  return '🚫 NO EN TARGET';
})() }}",





  "Genial_Business": "{{ (() => {
  const centro = $json['¿Con qué centro o instructor realizaste tu primer curso?'] || '';
  const cursos = String($json['¿Cuáles son los cursos que has hecho o vas a hacer con nosotros?'] || '');
  const coordina = $json['¿En tu trabajo tienes que coordinar un grupo de personas?'] || '';
  const interes = $json['Área interés método aprendizaje'] || '';
  const gestion = $json['Área interés gestión equipos'] || '';

  const situacionRaw =
    $json['¿Estudias o trabajas?'] ||
    $json['¿Estudias o trabajas? '] ||
    $json['¿Estudias o trabajas?  '] ||
    '';

  const situacion = situacionRaw.trim().toLowerCase().replace('.', '');
  const noEnTargetSituacion = ['solo estudio', 'ni estudio ni trabajo'];

  if (noEnTargetSituacion.includes(situacion)) return '🚫 NO EN TARGET';

  if (centro === 'Genial Business' || centro === 'General Business') return '✅ REALIZADO';

  if (
    cursos.includes('He hecho el curso Genial Business') ||
    cursos.includes('He hecho el curso General Business')
  ) return '✅ REALIZADO';

  if (
    cursos.includes('Estoy apuntado al curso Genial Business') ||
    cursos.includes('Estoy Apuntado al curso Genial Business')
  ) return '✍️ FIRMA';

  if (coordina.startsWith('Sí') || interes === '3 – Podría interesarme')
    return '🚪 VENDIBLE';

  if (
    interes === '5 – Me interesa mucho' ||
    interes === '4 – Me interesa' ||
    gestion === '5 – Me interesa mucho' ||
    gestion === '4 – Me interesa'
  ) return '📌 INTERESADO';

  if (
    interes === '2 – Poco' ||
    interes === '1 – Muy poco' ||
    interes === '0 – Nada de interés' ||
    coordina === 'No, recibo tareas e indicaciones'
  ) return '🚫 NO EN TARGET';

  return '';
})() }}",



  "One Echos": "{{
(() => {
  const r1 = $('Edit Fields').item.json['¿Cuántas veces has hecho el One hasta ahora?'] || '';
  const r2 = $('Edit Fields').item.json['¿Cuántas veces has hecho ONE?'] || '';
  const cursos = $('Edit Fields').item.json['¿Cuáles son los cursos que has hecho o vas a hacer con nosotros?'] || '';

  let base = Number((r1 || r2).toString().trim());

  if (isNaN(base)) base = 0;

  const cursosNorm = cursos.toLowerCase();

  if (cursosNorm.includes('he hecho el curso one')) {
    base = base + 1;
  }

  return String(base);
})()
}}",




  "Proximo One": "{{(() => {
    const proximo = $('Edit Fields').item.json['¿Vas a participar al próximo One (Febrero 2026)'] || '';
    const cursos = $('Edit Fields').item.json['¿Cuáles son los cursos que has hecho o vas a hacer con nosotros?'] || '';

    const proximoNorm = proximo.toLowerCase();
    const cursosNorm = cursos.toLowerCase();

    if (cursosNorm.includes('estoy apuntado al curso one')) {
      return '✍️ APUNTADO';
    }

    if (proximoNorm.includes('estoy apuntado') || proximoNorm.includes('apuntado'))
      return '✍️ FIRMA';

    if (proximoNorm.includes('no me interesa'))
      return '🥱 NO INTERESADO';

    if (proximoNorm.includes('valorando'))
      return '🤔 VALORANDO';

    return ''; })()}}",



  "Domina tu discurso": "{{(() => {
      const interes = $('Edit Fields').item.json['Área interés hablar en público'] || '';
      if (interes === '0 – Nada de interés') return '🚫 RECHAZADO';
      if (interes === '1 – Muy poco' || interes === '2 – Poco') return '❌ NO INTERESADO';
      if (interes === '3 – Podría interesarme') return '🚪 VENDIBLE';
      if (interes === '4 – Me interesa' || interes === '5 – Me interesa mucho') return '📌 INTERESADO';
      return '🚪 VENDIBLE';
    })()
  }}",

  "Genius Kids": "{{ 
    (() => {
      const familia = $('Edit Fields').item.json['En tu núcleo familiar'] || '';
      if (familia.includes('Hijos entre 8 y 12 años') || 
          familia.includes('Hijos entre 13 y 15 años') ||
          familia.includes('¿Tienes hijos de 8 a 12 años?') ||
          familia.includes('¿Tienes hijos de 13 a 15 años?')) return '🚪 VENDIBLE';
      return '🚫 NO EN TARGET';
    })()
  }}",





  "COMENTARIO": "________________FOLLOW UPS_____________________",


  "L Rapida": "{{ 
    (() => {
      const haHecho = $('Edit Fields').item.json['Has hecho el curso para'] || '';
      const profundizacion = $('Edit Fields').item.json['¿Has participado a las clases de profundización?'] || '';
      
      if (profundizacion.includes('Lectura rápida')) return '✅ REALIZADO';
      if (haHecho === 'Conseguir objetivos de estudio' || haHecho === 'Aprender Idiomas') return '🚪 VENDIBLE';
      if (haHecho === 'Acompañar a mi hijo/hija') return '🚫 NO EN TARGET';
      return '🚪 VENDIBLE';
    })()
  }}",

  "G Tiempo": "{{ 
    (() => {
      const haHecho = $('Edit Fields').item.json['Has hecho el curso para'] || '';
      const profundizacion = $('Edit Fields').item.json['¿Has participado a las clases de profundización?'] || '';
      
      if (profundizacion.includes('Gestión del tiempo')) return '✅ REALIZADO';
      if (haHecho === 'Conseguir objetivos de estudio' || haHecho === 'Aprender Idiomas') return '🚪 VENDIBLE';
      if (haHecho === 'Acompañar a mi hijo/hija') return '🚫 NO EN TARGET';
      return '🚪 VENDIBLE';
    })()
  }}",

  "Estress e IA": "{{ 
    (() => {
      const haHecho = $('Edit Fields').item.json['Has hecho el curso para'] || '';
      const profundizacion = $('Edit Fields').item.json['¿Has participado a las clases de profundización?'] || '';
      
      if (profundizacion.includes('Gestión del estrés') || profundizacion.includes('Inteligencia Artificial')) return '✅ REALIZADO';
      if (haHecho === 'Conseguir objetivos de estudio' || haHecho === 'Aprender Idiomas') return '🚪 VENDIBLE';
      if (haHecho === 'Acompañar a mi hijo/hija') return '🚫 NO EN TARGET';
      return '🚪 VENDIBLE';
    })()
  }}",

  "Estudiantes": "{{
    (() => {
      const estudiasTrabajas = $('Edit Fields').item.json['¿Estudias o trabajas?'] || '';
      const haHecho = $('Edit Fields').item.json['Has hecho el curso para'] || '';
      const followUp = $('Edit Fields').item.json['¿Has participado al follow up temático?'] || '';
      
      if (estudiasTrabajas.toLowerCase().includes('solo trabajo')) return '🚫 NO EN TARGET';
      if (haHecho === 'Conseguir objetivos de estudio') return '💡 INTERESADO';
      if (haHecho === 'Aprender Idiomas') return '🚪 VENDIBLE';
      if (haHecho.includes('Acompañar a mi hijo/hija')) return '🚫 NO EN TARGET';
      if (followUp === 'Estudiantes') return '📌 INTERESADO';
      
      return '';
    })()
  }}",

  "Idiomas": "{{
    (() => {
      const pendiente = $('Edit Fields').item.json['¿Tienes pendiente aprender un idioma?'] || '';
      const haHecho = $('Edit Fields').item.json['Has hecho el curso para'] || '';
      const followUp = $('Edit Fields').item.json['¿Has participado al follow up temático?'] || '';
      
      if (pendiente === 'Si' || pendiente === 'Sí' || 
          haHecho === 'Conseguir objetivos de estudio' || 
          haHecho === 'Aprender Idiomas') return '🚪 VENDIBLE';
      
      if (followUp === 'Idiomas') return '📌 INTERESADO';
      
      if (pendiente === 'No' || haHecho === 'Acompañar a mi hijo/hija') return '🚫 NO EN TARGET';
      
      return '';
    })()
  }}",

  "Profesionales": "{{
    (() => {
      const agendado = $('Edit Fields').item.json['¿Has agendado el follow up de los profesionales?'] || '';
      const estudiasTrabajas = $('Edit Fields').item.json['¿Estudias o trabajas?'] || '';
      const haHecho = $('Edit Fields').item.json['Has hecho el curso para'] || '';
      const followUp = $('Edit Fields').item.json['¿Has participado al follow up temático?'] || '';
      const participado = $('Edit Fields').item.json['Has Participado al follow up dedicado a los profesionales?'] || '';
      
      if (agendado.toLowerCase().includes('no y no me interesa')) return '🥱 NO INTERESADO';
      if (estudiasTrabajas.toLowerCase().includes('solo estudio')) return '🚫 NO EN TARGET';
      
      if (haHecho === 'Conseguir objetivos de estudio' || 
          haHecho.includes('Acompañar a mi hijo/hija') || 
          haHecho === 'Aprender Idiomas') return '🚪 VENDIBLE';
      
      if (agendado === 'Sí' || followUp === 'Profesionales' || participado === 'Sí') return '📌 INTERESADO';
      if (agendado === 'Sí, pero no confirmado') return 'PENDIENTE';
      
      return '';
    })()
  }}",




  "COMENTARIO": "________________EVENTOS_____________________",


  "Evento Vendido al curso": "{{ 
    (() => {
      const evento = $('Edit Fields').item.json['Evento finde atención'] || '';
      if (evento === 'Sí') return '💡 INTERESADO';
      if (evento === 'No') return '🥱 NO INTERESADO';
      if (evento.toLowerCase().includes('más o menos')) return '🚪 VENDIBLE';
      return '';
    })()
  }}",



  "One Shot 21/09": "",
  "Target": "{{ $('Edit Fields').item.json['Target 14 diciembre'] ? '📌 INTERESADO' : '' }}",
  "Familia 2.0": "{{ $('Edit Fields').item.json['Escanea tu familia'] || '' }}",
  "Comunic- Arte": "{{
    (() => {
      const interes = $('Edit Fields').item.json['Área interés comunicación y mediación'] || '';
      if (interes === '0' || interes === '0 – Nada de interés') return '❌ RECHAZADO';
      if (interes === '1' || interes === '1 – Muy poco' || interes === '2' || interes === '2 – Poco') return '🥱 NO INTERESADO';
      if (interes === '3' || interes === '3 – Podría interesarme') return '🚪 VENDIBLE';
      if (interes === '4' || interes === '4 – Me interesa') return '💡 TEMPLADO';
      if (interes === '5' || interes === '5 – Me interesa mucho') return '💡🔥 CALIENTE';
      return '';
    })()
  }}",

  "Riqueza sin limites": "{{
    (() => {
      const interes = $('Edit Fields').item.json['Área interés gestión económica'] || '';
      if (interes === '0' || interes === '0 – Nada de interés') return '❌ RECHAZADO';
      if (interes === '1' || interes === '1 – Muy poco' || interes === '2' || interes === '2 – Poco') return '🥱 NO INTERESADO';
      if (interes === '3' || interes === '3 – Podría interesarme') return '🚪 VENDIBLE';
      if (interes === '4' || interes === '4 – Me interesa') return '💡 TEMPLADO';
      if (interes === '5' || interes === '5 – Me interesa mucho') return '💡🔥 CALIENTE';
      return '';
    })()
  }}",

  "Hackea tu cuerpo": "{{
    (() => {
      const curiosidad = $('Edit Fields').item.json['Otros temas curiosidad'] || '';
      if (!curiosidad) return '';
      if (curiosidad.includes('Ninguno de estos')) return '❌ RECHAZADO CONTENIDO';
      if (curiosidad.includes('Salud y bienestar')) return '🚪 VENDIBLE';
      if (curiosidad.includes('Gestión económica') || curiosidad.includes('Networking') || curiosidad.includes('Comunicación y Mediación')) return '💡 TEMPLADO';
      if (curiosidad.includes('Crecimiento personal') || curiosidad.includes('Hablar en público')) return '💡🔥 CALIENTE';
      return '';
    })()
  }}",

  "Venta": "{{
    (() => {
      const interes = $('Edit Fields').item.json['Área interés ventas'] || '';
      if (interes === '0' || interes === '0 – Nada de interés') return '❌ RECHAZADO';
      if (interes === '1' || interes === '1 – Muy poco' || interes === '2' || interes === '2 – Poco') return '🥱 NO INTERESADO';
      if (interes === '3' || interes === '3 – Podría interesarme') return '🚪 VENDIBLE';
      if (interes === '4' || interes === '4 – Me interesa') return '💡 TEMPLADO';
      if (interes === '5' || interes === '5 – Me interesa mucho') return '💡🔥 CALIENTE';
      return '';
    })()
  }}",

  "Networking": "{{
    (() => {
      const interes = $('Edit Fields').item.json['Área interés networking'] || '';
      if (interes === '0' || interes === '0 – Nada de interés') return '❌ RECHAZADO';
      if (interes === '1' || interes === '1 – Muy poco' || interes === '2' || interes === '2 – Poco') return '🥱 NO INTERESADO';
      if (interes === '3' || interes === '3 – Podría interesarme') return '🚪 VENDIBLE';
      if (interes === '4' || interes === '4 – Me interesa') return '💡 TEMPLADO';
      if (interes === '5' || interes === '5 – Me interesa mucho') return '💡🔥 CALIENTE';
      return '';
    })()
  }}",






  "COMENTARIO": "________________OBJETIVOS Y ENCUESTA_____________________",


  "OBJETIVO DEL CURSO": "{{ 
(() => {
  const data = $('Edit Fields').item.json || {};
  const posiblesCampos = [
    'DESCRIBE TU OBJETIVO CON EL CURSO:',
    'Describe tu objetivo con el curso',
    'DESCRIBE TU OBJETIVO CON EL CURSO: (2)',
    '¿Cual era tu objetivo con el curso?',
    '¿Tienes algún objetivo de estudio?',
    '¿Cual era tu objetivo con el curso? (2)',
    '¿Cual era tu objetivo con el curso? (3)',
    '¿Cual era tu objetivo del curso?',
    '¿Cuál es la principal mejora que deseabas para tu hijo/hija?',
    'Cual es la principal mejora que desea para tu hijo/hija?'
  ];

  for (const campo of posiblesCampos) {
    const valor = data[campo];
    if (valor && valor !== 'undefined' && valor.trim() !== '') {
      return valor;
    }
  }
  return '';
})()
}}",

  "E.MATERIAL DEL CURSO": "{{ $('Edit Fields').item.json['Satisfacción material del curso'] }}",
  "E.STAFF": "{{ $('Edit Fields').item.json['Satisfacción staff'] }}",
  "E.INSTRUCTOR": "{{ $('Edit Fields').item.json['Satisfacción instructor'] }}",
  "E.MOTIVACIÓN": "{{ $('Edit Fields').item.json['Satisfacción motivación'] }}",
  "E.RELAJACIÓN": "{{ $('Edit Fields').item.json['Satisfacción relajación'] }}",
  "E.LECTURA RAPIDA": "{{ $('Edit Fields').item.json['Satisfacción lectura rápida'] }}",
  "E.MAPAS MENTALES": "{{ $('Edit Fields').item.json['Satisfacción mapas mentales'] }}",
  "E.TECNICAS DE MEMORIA": "{{ $('Edit Fields').item.json['Satisfacción técnicas de memoria'] }}",
  "E.METODO DE ESTUDIO": "{{ $('Edit Fields').item.json['Satisfacción método de estudio'] }}",
  "E.IDIOMAS EXTRANJEROS": "{{ $('Edit Fields').item.json['Satisfacción idiomas extranjeros'] }}",
  "Comunicación": "{{ $('Edit Fields').item.json['¿Hay algo que quieras comunicarnos?'] }}",
  "NOMBRE 1": "{{ $('Edit Fields').item.json['Persona recomendación 1'] }}",
  "NOMBRE 2": "{{ $('Edit Fields').item.json['Persona recomendación 2'] }}",
  "NOMBRE 3": "{{ $('Edit Fields').item.json['Persona recomendación 3'] }}",
  "NOMBRE 4": "{{ $('Edit Fields').item.json['Persona recomendación 4'] }}",
  "NOMBRE 5": "{{ $('Edit Fields').item.json['Persona recomendación 5'] }}",
  "COMENTARIO PROFU Y FOLLOW UP": "",
  "NOTAS": ""


}