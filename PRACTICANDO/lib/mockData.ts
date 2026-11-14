export interface ParcelSector {
  id: string;
  name: string;
  valley: string;
  lat: number;
  lon: number;
  crop: "mango" | "limon";
  soilType: string;
  gwetroot: number; // 0.0 - 1.0 (Root zone soil moisture)
  gwettop: number;  // 0.0 - 1.0 (Surface soil moisture)
  prectotcorr: number; // mm/day
  t2mMax: number;    // °C
}

export interface RotationStrategy {
  id: string;
  title: string;
  badge: string;
  badgeColor: "gray" | "green" | "amber";
  recommended: boolean;
  why: string;
  nasaEvidence: string;
  soilWaterBenefits: string[];
  dataGaps: string;
  localRisks: string;
}

export const MOCK_PARCELS: ParcelSector[] = [
  {
    id: "tambogrande",
    name: "Sector Tambogrande — Parcela San Lorenzo",
    valley: "Valle San Lorenzo, Piura",
    lat: -4.92,
    lon: -80.51,
    crop: "mango",
    soilType: "Franco-arenoso con baja materia orgánica",
    gwetroot: 0.38,
    gwettop: 0.18,
    prectotcorr: 0.2,
    t2mMax: 34.2,
  },
  {
    id: "sullana",
    name: "Sector Sullana — Parcela El Chira",
    valley: "Valle del Chira, Sullana",
    lat: -4.9,
    lon: -80.68,
    crop: "limon",
    soilType: "Franco-arcilloso con tendencia a salinidad",
    gwetroot: 0.25,
    gwettop: 0.12,
    prectotcorr: 0.0,
    t2mMax: 35.8,
  },
  {
    id: "catacaos",
    name: "Sector Catacaos — Parcela Medio Piura",
    valley: "Valle Medio Piura, Catacaos",
    lat: -5.26,
    lon: -80.63,
    crop: "mango",
    soilType: "Aluvial fértil con déficit hídrico superficial",
    gwetroot: 0.42,
    gwettop: 0.22,
    prectotcorr: 0.5,
    t2mMax: 33.1,
  },
];

export const MOCK_STRATEGIES: Record<string, RotationStrategy[]> = {
  mango: [
    {
      id: "strat-1",
      title: "Estrategia 1: Monocultivo Continuo de Mango",
      badge: "Práctica Actual",
      badgeColor: "gray",
      recommended: false,
      why: "Mantener el suelo desnudo entre hileras de mango sin coberturas vegetales ni rotación temporal.",
      nasaEvidence:
        "Los sensores de la NASA muestran un descenso paulatino de la humedad en raíz (GWETROOT < 0.30) y alta evaporación por radiación solar extrema.",
      soilWaterBenefits: [
        "Cero costo inmediato de semillas adicionales.",
        "Facilidad de tránsito de maquinaria tradicional.",
      ],
      dataGaps:
        "Falta de datos a micro-escala sobre la pérdida exacta de microbiota del suelo por exposición directa al sol.",
      localRisks:
        "Riesgo alto de erosin del suelo, compactación por lluvias intensas tipo El Niño y agotamiento de nitrógeno.",
    },
    {
      id: "strat-2",
      title: "Estrategia 2: Cobertera y Rotación con Frijol Caupí (Frijol Castilla)",
      badge: "⭐ Recomendada NASA + INIA",
      badgeColor: "green",
      recommended: true,
      why: "Sembrar frijol caupí entre las hileras de mango durante la ventana de 70 días tras la cosecha.",
      nasaEvidence:
        "Modelos de la NASA (GWETTOP) confirman que la cobertera vegetal retiene la humedad superficial un +35% y reduce la temperatura del suelo en 3 °C frente a 34.2 °C del aire.",
      soilWaterBenefits: [
        "Fija nitrógeno atmosférico (hasta 40-60 kg N/ha) para el mango.",
        "Protege el suelo de la erosión hídrica y eólica en Piura.",
        "Corta el ciclo de plagas del suelo sin competir con las raíces profundas del árbol.",
      ],
      dataGaps:
        "Varía la velocidad de descomposición del abono verde según la temperatura diaria de cada microcuenca.",
      localRisks:
        "Validar la disponibilidad de agua superficial para la germinación inicial del frijol caupí.",
    },
    {
      id: "strat-3",
      title: "Estrategia 3: Intercalado con Camote y Barrera de Maíz/Sorgo",
      badge: "Alternativa Productiva",
      badgeColor: "amber",
      recommended: false,
      why: "Intercalado de camote para cobertura densa y bordes de maíz como barrera contra los vientos secos piuranos.",
      nasaEvidence:
        "Análisis de estrés hídrico NASA (PRECTOTCORR + T2M_MAX) valida que las barreras vivas disminuyen la evapotranspiración estival.",
      soilWaterBenefits: [
        "Genera ingresos económicos complementarios de corto plazo.",
        "Alta biomasa vegetal para reincorporar como materia orgánica al suelo.",
      ],
      dataGaps:
        "Efecto de la sombra parcial de árboles adultos sobre el rendimiento del camote.",
      localRisks:
        "Requiere monitoreo constante para evitar competencia por riego si el canal local se cierra.",
    },
  ],
  limon: [
    {
      id: "strat-1",
      title: "Estrategia 1: Manejo Tradicional de Limón Sutil",
      badge: "Práctica Actual",
      badgeColor: "gray",
      recommended: false,
      why: "Limpieza total de malezas sin siembra de abonos verdes entre limones.",
      nasaEvidence:
        "Sensibilidad térmica alta en sensores NASA (T2M_MAX > 35 °C), elevando la salinidad por evaporación del agua superficial.",
      soilWaterBenefits: [
        "Inspección visual limpia del pie de la planta.",
      ],
      dataGaps:
        "Impacto exacto del estrés salino en raíces superficiales de cítricos.",
      localRisks:
        "Riesgo de encostramiento del suelo y mayor ataque de queresas/ácaros por estrés hídrico.",
    },
    {
      id: "strat-2",
      title: "Estrategia 2: Rotación de Cobertera con Leguminosa Crotalaria / Frijol Caupí",
      badge: "⭐ Recomendada NASA + INIA",
      badgeColor: "green",
      recommended: true,
      why: "Introducir cobertera verde leguminosa de raíz corta para descompactar el suelo y aportar nitrógeno a los limoneros.",
      nasaEvidence:
        "Datos NASA GWETROOT (0.38) y radiación solar confirman que la cobertura reduce el estrés térmico radicular en época seca.",
      soilWaterBenefits: [
        "Mejora la infiltración de agua en suelos arcillosos de Sullana/El Chira.",
        "Inyecta nitrógeno natural reduciendo el gasto en fertilizantes sintéticos.",
        "Incrementa los microorganismos benéficos que combaten bacterias fitopatógenas.",
      ],
      dataGaps:
        "Tasa de absorción de fósforo en presencia de sales locales.",
      localRisks:
        "Revisa con tu técnico local la poda lateral del limón para dar luz a la cobertera.",
    },
    {
      id: "strat-3",
      title: "Estrategia 3: Cobertura Orgánica Muerta (Mulch) + Alfalfa Temporal",
      badge: "Alternativa Conservadora",
      badgeColor: "amber",
      recommended: false,
      why: "Abonamiento orgánico con humus/compost tipo INIA en camas + alfalfar de protección.",
      nasaEvidence:
        "Estabilidad comprobada en retención hídrica según series de humedad de suelo NASA POWER.",
      soilWaterBenefits: [
        "Mantiene la temperatura radicular fresca durante las horas pico de calor.",
        "Aumenta la retención de nutrientes en el suelo.",
      ],
      dataGaps:
        "Costo de acarreo de materia orgánica externa en zonas distantes.",
      localRisks:
        "Asegurar compost bien madurado para evitar presencia de larvas o hongos de suelo.",
    },
  ],
};
