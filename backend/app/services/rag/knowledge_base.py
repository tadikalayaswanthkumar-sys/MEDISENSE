"""
MediSense AI - Clinical Knowledge Base & Reference Benchmark Registry
Contains standardized medical reference ranges, clinical units, diagnostic thresholds,
and disease risk guidelines for lab test analysis.
"""

CLINICAL_KNOWLEDGE_BASE = {
    # -------------------------------------------------------------------------
    # 1. Glycemic & Metabolic Panel
    # -------------------------------------------------------------------------
    "glucose": {
        "name": "Fasting Blood Glucose",
        "category": "Metabolic Panel",
        "unit": "mg/dL",
        "optimal": {"min": 70, "max": 99},
        "prediabetes": {"min": 100, "max": 125},
        "diabetes": {"min": 126, "max": 1000},
        "hypoglycemia": {"min": 0, "max": 69},
        "clinical_notes": (
            "Fasting glucose >= 126 mg/dL indicates Diabetes Mellitus. "
            "Values between 100-125 mg/dL reflect Prediabetes (Impaired Fasting Glucose). "
            "Values < 70 mg/dL indicate Hypoglycemia requiring acute glycemic management."
        ),
        "recommendations": {
            "high": "Consult an endocrinologist, reduce refined carbohydrates, and monitor HbA1c.",
            "moderate": "Adopt a low-glycemic index diet, engage in 150 mins/week moderate exercise, and retest in 3 months.",
            "low": "Consume fast-acting carbohydrates (15-20g) and recheck blood sugar after 15 minutes."
        }
    },
    "hba1c": {
        "name": "Glycated Hemoglobin (HbA1c)",
        "category": "Metabolic Panel",
        "unit": "%",
        "optimal": {"min": 4.0, "max": 5.6},
        "prediabetes": {"min": 5.7, "max": 6.4},
        "diabetes": {"min": 6.5, "max": 20.0},
        "clinical_notes": (
            "HbA1c reflects average blood glucose over the preceding 2-3 months. "
            ">= 6.5% confirms Diabetes Mellitus. 5.7%-6.4% indicates Prediabetes."
        ),
        "recommendations": {
            "high": "Initiate comprehensive diabetes management plan and lifestyle modification.",
            "moderate": "Implement lifestyle intervention, dietary counseling, and physical activity."
        }
    },
    "insulin": {
        "name": "Fasting Serum Insulin",
        "category": "Metabolic Panel",
        "unit": "uIU/mL",
        "optimal": {"min": 2.6, "max": 24.9},
        "clinical_notes": "Elevated fasting insulin (> 25 uIU/mL) points toward Insulin Resistance / Metabolic Syndrome."
    },

    # -------------------------------------------------------------------------
    # 2. Lipid Profile Panel
    # -------------------------------------------------------------------------
    "cholesterol": {
        "name": "Total Cholesterol",
        "category": "Lipid Profile",
        "unit": "mg/dL",
        "optimal": {"min": 125, "max": 199},
        "borderline": {"min": 200, "max": 239},
        "high": {"min": 240, "max": 1000},
        "clinical_notes": (
            "Total cholesterol >= 240 mg/dL represents High Hypercholesterolemia. "
            "Values 200-239 mg/dL represent Borderline High Risk for Atherosclerosis."
        ),
        "recommendations": {
            "high": "Adopt Mediterranean diet low in saturated/trans fats, increase dietary fiber, and discuss statin therapy.",
            "moderate": "Increase soluble fiber (oats, legumes), limit saturated fats < 7% total calories."
        }
    },
    "hdl": {
        "name": "HDL Cholesterol (Good Cholesterol)",
        "category": "Lipid Profile",
        "unit": "mg/dL",
        "optimal": {"min": 50, "max": 150},
        "borderline": {"min": 40, "max": 49},
        "low": {"min": 0, "max": 39},
        "clinical_notes": (
            "HDL < 40 mg/dL is an independent risk factor for Coronary Artery Disease (CAD). "
            "HDL >= 60 mg/dL provides cardioprotective benefits."
        )
    },
    "ldl": {
        "name": "LDL Cholesterol (Bad Cholesterol)",
        "category": "Lipid Profile",
        "unit": "mg/dL",
        "optimal": {"min": 0, "max": 99},
        "near_optimal": {"min": 100, "max": 129},
        "borderline": {"min": 130, "max": 159},
        "high": {"min": 160, "max": 189},
        "very_high": {"min": 190, "max": 1000},
        "clinical_notes": (
            "LDL >= 190 mg/dL is Very High and warrants primary cardiovascular prevention. "
            "Target LDL for high-risk patients is < 70 mg/dL."
        )
    },
    "triglycerides": {
        "name": "Triglycerides",
        "category": "Lipid Profile",
        "unit": "mg/dL",
        "optimal": {"min": 0, "max": 149},
        "borderline": {"min": 150, "max": 199},
        "high": {"min": 200, "max": 499},
        "very_high": {"min": 500, "max": 5000},
        "clinical_notes": (
            "Triglycerides >= 500 mg/dL significantly increase the risk of Acute Pancreatitis. "
            "Values 150-499 mg/dL increase risk of cardiovascular events."
        )
    },

    # -------------------------------------------------------------------------
    # 3. Complete Blood Count (CBC)
    # -------------------------------------------------------------------------
    "hemoglobin": {
        "name": "Hemoglobin (Hb)",
        "category": "Complete Blood Count",
        "unit": "g/dL",
        "optimal": {"min": 13.5, "max": 17.5},
        "mild_anemia": {"min": 10.0, "max": 13.4},
        "severe_anemia": {"min": 0, "max": 9.9},
        "polycythemia": {"min": 17.6, "max": 30.0},
        "clinical_notes": (
            "Hemoglobin < 13.5 g/dL (male) or < 12.0 g/dL (female) indicates Anemia. "
            "Values < 8.0 g/dL signal Severe Anemia requiring urgent evaluation. "
            "Elevated Hb > 17.5 g/dL suggests Polycythemia or Chronic Hypoxia."
        ),
        "recommendations": {
            "low": "Evaluate iron status (ferritin, TIBC), Vitamin B12/Folate levels, and stool occult blood.",
            "high": "Ensure adequate hydration and evaluate for smoking history, sleep apnea, or pulmonary disease."
        }
    },
    "wbc": {
        "name": "White Blood Cell Count (WBC)",
        "category": "Complete Blood Count",
        "unit": "x10^3/uL",
        "optimal": {"min": 4.5, "max": 11.0},
        "leukopenia": {"min": 0, "max": 4.4},
        "leukocytosis": {"min": 11.1, "max": 100.0},
        "clinical_notes": (
            "WBC > 11.0 x10^3/uL indicates Leukocytosis (bacterial infection, inflammation, stress, tissue injury). "
            "WBC < 4.5 x10^3/uL indicates Leukopenia (viral infection, bone marrow suppression, autoimmune)."
        )
    },
    "rbc": {
        "name": "Red Blood Cell Count (RBC)",
        "category": "Complete Blood Count",
        "unit": "x10^6/uL",
        "optimal": {"min": 4.3, "max": 5.9},
        "clinical_notes": "RBC count reflects total oxygen-carrying capacity."
    },
    "platelets": {
        "name": "Platelet Count (PLT)",
        "category": "Complete Blood Count",
        "unit": "x10^3/uL",
        "optimal": {"min": 150, "max": 450},
        "thrombocytopenia": {"min": 0, "max": 149},
        "thrombocytosis": {"min": 451, "max": 2000},
        "clinical_notes": (
            "Platelets < 150 x10^3/uL indicates Thrombocytopenia (increased bleeding risk). "
            "Platelets > 450 x10^3/uL indicates Thrombocytosis (reactive inflammation or myeloproliferative disorder)."
        )
    },
    "hematocrit": {
        "name": "Hematocrit (HCT)",
        "category": "Complete Blood Count",
        "unit": "%",
        "optimal": {"min": 38.8, "max": 50.0},
        "clinical_notes": "Percentage of total blood volume composed of red blood cells."
    },
    "mcv": {
        "name": "Mean Corpuscular Volume (MCV)",
        "category": "Complete Blood Count",
        "unit": "fL",
        "optimal": {"min": 80, "max": 100},
        "microcytic": {"min": 0, "max": 79},
        "macrocytic": {"min": 101, "max": 200},
        "clinical_notes": (
            "MCV < 80 fL points to Microcytic Anemia (Iron deficiency, Thalassemia). "
            "MCV > 100 fL points to Macrocytic Anemia (B12/Folate deficiency, Liver disease)."
        )
    },

    # -------------------------------------------------------------------------
    # 4. Renal / Kidney Function Panel
    # -------------------------------------------------------------------------
    "creatinine": {
        "name": "Serum Creatinine",
        "category": "Kidney Function",
        "unit": "mg/dL",
        "optimal": {"min": 0.6, "max": 1.2},
        "elevated": {"min": 1.3, "max": 2.5},
        "severe": {"min": 2.6, "max": 20.0},
        "clinical_notes": (
            "Creatinine > 1.2 mg/dL indicates impaired renal clearance or Acute Kidney Injury (AKI). "
            "Values > 2.5 mg/dL suggest severe renal impairment requiring nephrology consultation."
        ),
        "recommendations": {
            "high": "Maintain fluid hydration, avoid nephrotoxic NSAIDs (ibuprofen/naproxen), and check eGFR."
        }
    },
    "bun": {
        "name": "Blood Urea Nitrogen (BUN)",
        "category": "Kidney Function",
        "unit": "mg/dL",
        "optimal": {"min": 7, "max": 20},
        "high": {"min": 21, "max": 200},
        "clinical_notes": (
            "BUN > 20 mg/dL indicates Uremia, Azotemia, dehydration, high protein intake, or renal insufficiency."
        )
    },
    "egfr": {
        "name": "Estimated Glomerular Filtration Rate (eGFR)",
        "category": "Kidney Function",
        "unit": "mL/min/1.73m2",
        "optimal": {"min": 90, "max": 200},
        "mild_reduction": {"min": 60, "max": 89},
        "kidney_disease": {"min": 15, "max": 59},
        "kidney_failure": {"min": 0, "max": 14},
        "clinical_notes": (
            "eGFR < 60 mL/min/1.73m2 for > 3 months diagnoses Chronic Kidney Disease (CKD). "
            "eGFR < 15 mL/min/1.73m2 indicates Kidney Failure (End-Stage Renal Disease)."
        )
    },
    "uric_acid": {
        "name": "Serum Uric Acid",
        "category": "Kidney & Joint Function",
        "unit": "mg/dL",
        "optimal": {"min": 3.5, "max": 7.2},
        "high": {"min": 7.3, "max": 20.0},
        "clinical_notes": (
            "Uric acid > 7.2 mg/dL indicates Hyperuricemia, placing patient at risk for Gouty Arthritis and Renal Calculi (Kidney Stones)."
        )
    },

    # -------------------------------------------------------------------------
    # 5. Liver Function Panel (Hepatic)
    # -------------------------------------------------------------------------
    "alt": {
        "name": "Alanine Aminotransferase (ALT / SGPT)",
        "category": "Liver Function",
        "unit": "U/L",
        "optimal": {"min": 7, "max": 56},
        "high": {"min": 57, "max": 10000},
        "clinical_notes": (
            "Elevated ALT (> 56 U/L) is a sensitive marker of acute hepatocellular injury (Hepatitis, Fatty Liver/NAFLD, toxic exposure)."
        )
    },
    "ast": {
        "name": "Aspartate Aminotransferase (AST / SGOT)",
        "category": "Liver Function",
        "unit": "U/L",
        "optimal": {"min": 10, "max": 40},
        "high": {"min": 41, "max": 10000},
        "clinical_notes": (
            "AST > 40 U/L indicates liver or muscle cell breakdown. AST/ALT ratio > 2 suggests alcoholic liver injury."
        )
    },
    "bilirubin": {
        "name": "Total Bilirubin",
        "category": "Liver Function",
        "unit": "mg/dL",
        "optimal": {"min": 0.2, "max": 1.2},
        "high": {"min": 1.3, "max": 30.0},
        "clinical_notes": (
            "Total Bilirubin > 1.2 mg/dL indicates Hyperbilirubinemia (Jaundice, biliary obstruction, or hemolysis)."
        )
    },
    "albumin": {
        "name": "Serum Albumin",
        "category": "Liver & Nutritional Status",
        "unit": "g/dL",
        "optimal": {"min": 3.5, "max": 5.5},
        "low": {"min": 0, "max": 3.4},
        "clinical_notes": (
            "Albumin < 3.5 g/dL indicates Hypoalbuminemia (chronic liver dysfunction, nephrotic syndrome, malnutrition, or systemic inflammation)."
        )
    },

    # -------------------------------------------------------------------------
    # 6. Thyroid Function Panel
    # -------------------------------------------------------------------------
    "tsh": {
        "name": "Thyroid Stimulating Hormone (TSH)",
        "category": "Thyroid Function",
        "unit": "uIU/mL",
        "optimal": {"min": 0.45, "max": 4.5},
        "hypothyroidism": {"min": 4.51, "max": 100.0},
        "hyperthyroidism": {"min": 0, "max": 0.44},
        "clinical_notes": (
            "TSH > 4.5 uIU/mL indicates Hypothyroidism (sluggish thyroid function). "
            "TSH < 0.45 uIU/mL indicates Hyperthyroidism (overactive thyroid function)."
        ),
        "recommendations": {
            "high": "Consult an endocrinologist for Free T4 / Free T3 evaluation and thyroid replacement therapy consideration.",
            "low": "Evaluate for hyperthyroid symptoms (tachycardia, weight loss, tremor) and order Free T4."
        }
    },

    # -------------------------------------------------------------------------
    # 7. Inflammatory & Cardiac Markers
    # -------------------------------------------------------------------------
    "crp": {
        "name": "C-Reactive Protein (CRP)",
        "category": "Inflammation & Cardiac Risk",
        "unit": "mg/L",
        "optimal": {"min": 0, "max": 3.0},
        "high_risk": {"min": 3.1, "max": 300.0},
        "clinical_notes": (
            "CRP > 3.0 mg/L signals systemic inflammation or elevated cardiovascular disease risk."
        )
    }
}
