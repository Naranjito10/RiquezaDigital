/**
 * High-Fidelity Logic Processor for Sirux CRM
 * Ported from legacy "Cristian" workflow with 80+ fields.
 */

const item = items[0].json;
const body = item.body || item; // Robustness for dispatcher/direct

const results = {};

// --- 1. CORE IDENTITY & PROFILE ---
results['NOMBRE'] = body.Nombre || '';
results['APELLIDOS_NOMBRE'] = [body.Apellidos, body.Nombre].filter(Boolean).join(', ');
results['EMAIL'] = (body.Correo || body['Dirección de correo electrónico'] || '').toLowerCase().trim();
results['CONTACTO'] = String(body['Numero de contacto'] || body['Número Contacto (en que tienes whatsapp)'] || body['Número de contacto (en el que tienes whatsapp)'] || '').replace(/\D+/g, '');

// --- 2. MERCURY & INSTRUCTOR LOGIC ---
const instructorResponses = [
    body['¿Con qué centro o instructor realizaste tu primer curso?'],
    body['¿En qué ciudad has hecho el curso?'],
    body['¿Con qué centro o instructor realizaste tu primer curso ONE?']
];

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

const respInst = instructorResponses.find(r => r && mapaCiudades[r.trim()]);
results['INSTRUCTOR'] = mapaCiudades[respInst] || '';

const primerCursoStr = (body['¿Cuál es el primer curso que has hecho con nosotros?'] || '').toLowerCase();
const esCursoValido = primerCursoStr.includes('genial business') || primerCursoStr.includes('30 dias 1 idioma');
results['MERCURY'] = (respInst || esCursoValido) ? '✅' : '❌';

// --- 3. AGE & METADATA ---
const fechaNac = body['Fecha de nacimiento'] || '';
if (fechaNac && fechaNac.includes('/')) {
    const parts = fechaNac.split('/');
    if (parts.length === 3) {
        const nacimiento = new Date(parts[2], parts[1] - 1, parts[0]);
        const hoy = new Date();
        let edad = hoy.getFullYear() - nacimiento.getFullYear();
        const m = hoy.getMonth() - nacimiento.getMonth();
        if (m < 0 || (m === 0 && hoy.getDate() < nacimiento.getDate())) edad--;
        results['EDAD'] = edad;
    }
}
results['MES'] = new Date().toLocaleString('es-ES', { month: 'long' });
results['AÑO'] = new Date().getFullYear().toString();
results['MODALIDAD'] = body['Has conocido el curso por'] || '';
results['TERMINAL ESTABLE'] = body['¿Quién es tu TUTOR?'] || body['¿Quién es el TUTOR de tu hijo/hija?'] || '';
results['CIUDAD'] = body['¿En qué ciudad vives?'] || body['¿En qué ciudad vives? (si es un pueblo indica la ciudad grande más cercana)'] || '';
results['PROFESIÓN'] = body['¿A qué te dedicas actualmente?'] || '';

// --- 4. PRODUCT STATUSES (The Heart of the CRM) ---
const cursosDone = String(body['¿Cuáles son los cursos que has hecho o vas a hacer con nosotros?'] || '');
const haHechoRaw = body['Has hecho el curso para'] || body['Has hecho el curso para:'] || '';
const haHecho = (haHechoRaw || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim().toLowerCase();

// GENIUS
if (haHecho === 'conseguir objetivos de estudio') results['GENIUS'] = '✅ REALIZADO';
else if (haHecho === 'acompanar a mi hijo/hija') results['GENIUS'] = '🦮 ACOMPAÑANTE';
else if (haHecho.includes('acompanar a mi hijo/hija y')) results['GENIUS'] = '🦮💡 ACOMPAÑANTE INTERESADO';
else if (haHecho === 'aprender idiomas') results['GENIUS'] = '🌎 X IDIOMA';
else if (cursosDone.includes('He hecho el curso Genius como ALUMNO')) results['GENIUS'] = '✅ REALIZADO';
else if (cursosDone.toLowerCase().includes('apuntado al curso genius')) results['GENIUS'] = '✍️';
else {
    const metInt = body['Área interés método aprendizaje'] || '';
    if (metInt.includes('4') || metInt.includes('5')) results['GENIUS'] = '💡';
    else results['GENIUS'] = '🚪 VENDIBLE';
}

// 30 DIAS
const interest30 = body['Área interés idioma en 30 días'] || '';
const pending30 = body['¿Tienes pendiente aprender un idioma?'] || '';
if (haHecho === 'aprender idiomas') results['30_dias_1_idioma'] = '🧠 X GENIUS';
else if (cursosDone.toLowerCase().includes('finalizado el protocolo de 30 dias')) results['30_dias_1_idioma'] = '✅ REALIZADO';
else if (cursosDone.toLowerCase().includes('siguiendo el protocolo de 30 dias')) results['30_dias_1_idioma'] = '✍️ EN CURSO';
else if (pending30 === 'Si' || pending30 === 'Sí') results['30_dias_1_idioma'] = '🚪 VENDIBLE';
else if (interest30.includes('5') || interest30.includes('4')) results['30_dias_1_idioma'] = '📌 INTERESADO';
else results['30_dias_1_idioma'] = '🚫 NO EN TARGET';

// GENIAL BUSINESS
const situacion = (body['¿Estudias o trabajas?'] || '').toLowerCase();
if (situacion.includes('solo estudio') || situacion.includes('ni estudio ni trabajo')) {
    results['Genial_Business'] = '🚫 NO EN TARGET';
} else if (cursosDone.toLowerCase().includes('he hecho el curso genial business')) {
    results['Genial_Business'] = '✅ REALIZADO';
} else {
    results['Genial_Business'] = '🚪 VENDIBLE';
}

// SSA
const edadVal = parseInt(results['EDAD']) || 0;
if (cursosDone.toLowerCase().includes('he hecho la soft skills academy')) results['SSA'] = '🏁 Acabado';
else if (cursosDone.toLowerCase().includes('estoy haciendo la soft skills academy')) results['SSA'] = '🎓 Actualmente Skiller';
else if (edadVal >= 18 && edadVal <= 25) results['SSA'] = '🚪 Vendible';
else results['SSA'] = 'NoInTarget';

// --- 5. ONE SHOT & TARGET ---
const r1One = body['¿Cuántas veces has hecho el One hasta ahora?'] || body['¿Cuántas veces has hecho ONE?'] || 0;
results['One Echos'] = (Number(r1One) + (cursosDone.toLowerCase().includes('he hecho el curso one') ? 1 : 0)).toString();

const proximoOne = body['¿Vas a participar al próximo One (Febrero 2026)'] || '';
if (cursosDone.toLowerCase().includes('estoy apuntado al curso one')) results['Proximo One'] = '✍️ APUNTADO';
else if (proximoOne.toLowerCase().includes('apuntado')) results['Proximo One'] = '✍️ FIRMA';
else results['Proximo One'] = '';

// --- 6. SATISFACTION & REFERRALS ---
const satisfactionMapping = {
    'Satisfacción material del curso': 'E.MATERIAL DEL CURSO',
    'Satisfacción staff': 'E.STAFF',
    'Satisfacción instructor': 'E.INSTRUCTOR',
    'Satisfacción motivación': 'E.MOTIVACIÓN',
    'Satisfacción relajación': 'E.RELAJACIÓN',
    'Satisfacción lectura rápida': 'E.LECTURA RAPIDA',
    'Satisfacción mapas mentales': 'E.MAPAS MENTALES',
    'Satisfacción técnicas de memoria': 'E.TECNICAS DE MEMORIA',
    'Satisfacción método de estudio': 'E.METODO DE ESTUDIO',
    'Satisfacción idiomas extranjeros': 'E.IDIOMAS EXTRANJEROS'
};
for (const [key, col] of Object.entries(satisfactionMapping)) {
    results[col] = body[key] || '';
}

for (let i = 1; i <= 5; i++) {
    results[`NOMBRE ${i}`] = body[`Persona recomendación ${i}`] || '';
}

// --- 7. OBJECTIVE EXTRACTION ---
const objCampos = [
    'DESCRIBE TU OBJETIVO CON EL CURSO:',
    'Describe tu objetivo con el curso',
    '¿Cual era tu objetivo con el curso?',
    '¿Tienes algún objetivo de estudio?',
    '¿Cuál es la principal mejora que deseabas para tu hijo/hija?'
];
results['OBJETIVO DEL CURSO'] = objCampos.map(c => body[c]).find(v => v && v !== 'undefined' && v.trim() !== '') || '';

return results;
