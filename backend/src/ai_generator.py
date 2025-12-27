import os
import json
import random

from openai import OpenAI
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    # Lenguajes soportados
    supported_languages = [
        "Python",
        "JavaScript",
        "TypeScript",
        "Java",
        "C++",
        "C#",
        "Go",
        "Rust",
        "Swift",
        "PHP",
        "SQL",
    ]

    selected_language = random.choice(supported_languages)

    prompt = f"""
Actúa como un entrevistador técnico senior especializado en {selected_language}.
Genera UNA pregunta tipo test de programación ÚNICA para un candidato de nivel {difficulty} en {selected_language}.

IDIOMA:
- Toda la pregunta, las opciones y la explicación deben estar en español neutro.

FORMATO DE CONTENIDO:
- Si la pregunta habla de "salida del siguiente código", "¿qué imprime este código?" o similar,
  debes incluir SIEMPRE un bloque de código en {selected_language}.
- Ese bloque de código NO debe ir dentro del título:
  - "title": texto de la pregunta SIN el bloque de código.
  - "code": bloque de código en {selected_language}, con saltos de línea y sangría correctos.
- Si por algún motivo la pregunta no necesita código, deja "code" como cadena vacía "".

NIVELES:
- easy: sintaxis básica pero aplicada en pequeños fragmentos de código (listas, bucles, condicionales).
- medium: arrays, objetos, POO sencilla, manejo de errores, funciones puras.
- hard: concurrencia, rendimiento, patrones de diseño o trampas sutiles.

REGLAS:
- Evita preguntas triviales del tipo “¿qué es una variable?”.
- Las 4 opciones deben ser plausibles; no pongas tonterías como “ninguna de las anteriores” salvo que tenga sentido.

ESTRUCTURA JSON (OBLIGATORIA):
{{
  "title": "Pregunta en español sin el código",
  "code": "bloque de código en {selected_language} o cadena vacía",
  "options": ["opción 1", "opción 2", "opción 3", "opción 4"],
  "correct_answer_id": 0,
  "explanation": "Explicación en español."
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a JSON generator API. You always output a valid JSON object.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        if content is None:
            raise ValueError("OpenAI response content is None.")

        data: Dict[str, Any] = json.loads(content)

        # Normalizar campo code
        if "code" not in data:
            data["code"] = ""

        # Añadir lenguaje al título si no aparece
        if selected_language not in data.get("title", ""):
            data["title"] = f"[{selected_language}] {data['title']}"

        return data

    except Exception as e:
        print(f"[AI ERROR] Error OpenAI: {e}")
        raise
