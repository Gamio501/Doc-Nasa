# orquestador/

**Responsable:** Persona 2

Genera el `run_id` y encadena las etapas: extractor → calculador → interprete-llm → verificador → publicador.
Si una etapa falla, se detiene y no publica nada.
