"""
Gastroenterology Domain for GPDISC
Comprehensive digestive system consultation covering abdominal pain, liver disease,
inflammatory bowel disease, and GI conditions.
"""

from .. import BaseDomainModule, DomainConfig, DomainQueryResult
from typing import Dict, List, Optional, Any
import re

class GastroenterologyDomain(BaseDomainModule):
    """
    Gastroenterology Specialist Domain

    Covers:
    - Abdominal pain differential diagnosis
    - GORD/GERD management
    - Peptic ulcer disease
    - Inflammatory bowel disease (Crohn's, UC)
    - Irritable bowel syndrome
    - Liver function test interpretation
    - Hepatitis management
    - Pancreatitis evaluation
    - GI bleeding assessment
    - Coeliac disease recognition
    - Endoscopy/colonoscopy result interpretation
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="gastroenterology",
            version="1.0.0",
            dependencies=[],
            description="Gastroenterology: abdominal pain, liver disease, IBD, IBS, GI bleeding, hepatitis, pancreatitis",
            keywords=[
                # GI symptoms
                "abdominal pain", "stomach pain", "belly pain", "tummy pain",
                "nausea", "vomiting", "vomit", "retching",
                "diarrhea", "diarrhoea", "loose stool", "frequent stool",
                "constipation", "hard stool", "straining",
                "bloating", "distension", "flatulence", "wind", "gas",
                "heartburn", "reflux", "indigestion", "dyspepsia",
                "dysphagia", "difficulty swallowing",
                "rectal bleeding", "blood in stool", "melaena", "hematochezia",
                "jaundice", "yellow skin", "yellow eyes",
                "ascites", "fluid in abdomen",

                # GI conditions
                "gastroenterology", "gastrointestinal", "digestive",
                "gerd", "gord", "gastroesophageal reflux",
                "peptic ulcer", "stomach ulcer", "duodenal ulcer",
                "gastritis", "h pylori", "helicobacter",
                "crohn's", "crohns", "ulcerative colitis", "uc", "ibd",
                "irritable bowel", "ibs",
                "coeliac", "celiac", "gluten",
                "diverticulitis", "diverticulosis",

                # Liver conditions
                "liver", "hepatic", "hepatitis", "cirrhosis",
                "fatty liver", "nafld", "nash",
                "lft", "liver function test", "alt", "ast", "alp", "ggt", "bilirubin",
                "jaundice", "icterus",

                # Pancreas/biliary
                "pancreatitis", "pancreatic",
                "gallstone", "biliary", "cholecystitis",

                # Procedures
                "endoscopy", "gastroscopy", "ogd",
                "colonoscopy", "sigmoidoscopy",
                "gastroscopy", "capsule endoscopy"
            ],
            capabilities=[
                "abdominal_pain_diagnosis",
                "gerd_management",
                "peptic_ulcer_management",
                "lft_interpretation",
                "hepatitis_management",
                "ibd_management",
                "ibs_management",
                "pancreatitis_assessment",
                "gi_bleed_evaluation",
                "coeliac_disease_screening",
                "endoscopy_interpretation",
                "liver_disease_assessment"
            ]
        )

    def process_query(self, query: str, context: dict = None) -> DomainQueryResult:
        """Route gastroenterology query to appropriate handler"""
        query_lower = query.lower()

        # Abdominal pain
        if "abdominal pain" in query_lower or "stomach pain" in query_lower or "belly pain" in query_lower:
            return self._handle_abdominal_pain(query, context)

        # GI bleeding
        elif any(term in query_lower for term in ["rectal bleeding", "blood in stool", "melaena", "melena", "hematochezia"]):
            return self._handle_gi_bleed(query, context)

        # Liver function tests
        elif any(term in query_lower for term in ["lft", "liver function", "alt", "ast", "alp", "ggt", "bilirubin"]):
            return self._interpret_lft(query, context)

        # Liver disease
        elif any(term in query_lower for term in ["liver disease", "cirrhosis", "fatty liver", "nafld", "nash"]):
            return self._manage_liver_disease(query, context)

        # Hepatitis
        elif "hepatitis" in query_lower:
            return self._manage_hepatitis(query, context)

        # Pancreatitis
        elif "pancreatit" in query_lower:
            return self._assess_pancreatitis(query, context)

        # IBD (Crohn's, UC)
        elif any(term in query_lower for term in ["crohn", "ulcerative colitis", "uc", "ibd"]):
            return self._manage_ibd(query, context)

        # IBS
        elif "ibs" in query_lower or "irritable bowel" in query_lower:
            return self._manage_ibs(query, context)

        # GORD/GERD
        elif any(term in query_lower for term in ["gord", "gerd", "reflux", "heartburn"]):
            return self._manage_gerd(query, context)

        # Peptic ulcer
        elif any(term in query_lower for term in ["peptic ulcer", "stomach ulcer", "duodenal ulcer"]):
            return self._manage_peptic_ulcer(query, context)

        # Coeliac disease
        elif any(term in query_lower for term in ["coeliac", "celiac", "gluten"]):
            return self._assess_coeliac(query, context)

        # Diarrhea
        elif "diarrh" in query_lower:
            return self._handle_diarrhea(query, context)

        # Constipation
        elif "constipat" in query_lower:
            return self._handle_constipation(query, context)

        # Endoscopy
        elif any(term in query_lower for term in ["endoscopy", "gastroscopy", "colonoscopy"]):
            return self._interpret_endoscopy(query, context)

        # General gastroenterology
        else:
            return self._handle_general_gastro(query, context)

    def _handle_abdominal_pain(self, query: str, context: dict) -> DomainQueryResult:
        """Handle abdominal pain queries"""
        answer = """**Abdominal Pain Differential Diagnosis**

**Anatomic Approach:**

**Right Upper Quadrant (RUQ):**
- **Biliary disease:** Cholecystitis, cholelithiasis (right shoulder tip pain)
- **Hepatic:** Hepatitis, abscess
- **Renal:** Pyelonephritis, nephrolithiasis
- **Pulmonary:** Pneumonia, pleurisy (lower lobe)
- **Other:** Peptic ulcer, appendicitis (early)

**Left Upper Quadrant (LUQ):**
- **Splenic:** Splenomegaly, infarction
- **Gastric:** Gastritis, peptic ulcer
- **Renal:** Pyelonephritis, nephrolithiasis
- **Pancreatic:** Pancreatitis (epigastric, radiates through to back)
- **Other:** Splenic rupture (trauma)

**Right Lower Quadrant (RLQ):**
- **Appendicitis** (McBurney's point, migration from periumbilical)
- **Gynecologic:** Ovarian cyst, torsion, ectopic pregnancy
- **Renal:** Nephrolithiasis, UTI
- **Gastrointestinal:** Crohn's disease (ileitis)

**Left Lower Quadrant (LLQ):**
- **Gynecologic:** Ovarian cyst, PID, ectopic pregnancy
- **Renal:** Nephrolithiasis, UTI
- **Gastrointestinal:** Diverticulitis (sigmoid), IBS

**Epigastric:**
- **Peptic ulcer disease** (gastric/duodenal)
- **Gastritis**
- **GERD**
- **Pancreatitis** (radiates through to back)
- **Myocardial infarction** (referred pain - ALWAYS EXCLUDE FIRST!)

**Periumbilical:**
- **Appendicitis** (early)
- **Small bowel obstruction**
- **Gastroenteritis**

**Suprapubic:**
- **Urinary:** Cystitis, UTI, retention
- **Gynecologic:** PID, ovarian pathology
- **Gastrointestinal:** Appendicitis (pelvic)

**General/Diffuse:**
- **Gastroenteritis**
- **IBS**
- **Early obstruction**
- **Peritonitis** (surgical emergency)
- **Mesenteric ischemia** (elderly, atrial fibrillation)

**Red Flags (Urgent Referral):**
- **Guarding, rigidity, rebound** (peritonitis - EMERGENCY)
- **Absent bowel sounds** (obstruction, ileus)
- **Pulsatile abdominal mass** (AAA - EMERGENCY)
- **Blood in stool/vomit**
- **Weight loss, anemia** (malignancy)
- **Jaundice** (biliary obstruction)
- **Severe, sudden onset** (perforation, ischemia)

**When to Refer Urgently (2-week wait pathway):**
- Unintentional weight loss
- Age > 50 with change in bowel habits
- Iron deficiency anemia
- Rectal bleeding (age > 50, or change in bowel habits)
- Abdominal mass
- Palpable gallbladder + jaundice (Courvoisier's sign)

**Sources:** NICE NG12, BMJ Best Practice, RCP 2024"""

        return DomainQueryResult(
            domain_name="gastroenterology",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "gastroenterology",
                "focus": "abdominal_pain_differential",
                "sources": ["NICE NG12", "BMJ Best Practice", "RCP 2024"]
            }
        )

    def _handle_gi_bleed(self, query: str, context: dict) -> DomainQueryResult:
        """Handle GI bleeding queries"""
        answer = """**GI Bleeding Assessment**

**Severity Assessment (Rockall Score):**

**Age:**
- < 60: 0 points
- 60-79: 1 point
- ≥ 80: 2 points

**Shock:**
- No shock (SBP > 100, HR < 100): 0 points
- Tachycardia (HR > 100, SBP > 100): 1 point
- Hypotension (SBP < 100): 2 points

**Comorbidity:**
- No major comorbidity: 0 points
- Heart failure, ischemic heart disease, any major comorbidity: 2 points
- Renal failure, liver failure, disseminated malignancy: 3 points

**Diagnosis:**
- Mallory-Weiss tear: 0 points
- All diagnoses: 1 point
- Upper GI malignancy: 2 points

**Evidence of Bleeding:**
- None: 0 points
- Dark blood/spotting: 1 point
- Fresh blood, clot, active bleeding: 2 points

**Rockall Score Interpretation:**
- **0-2:** Low risk (discharge, outpatient endoscopy)
- **3-4:** Moderate risk (admit, endoscopy within 24h)
- **5-10:** High risk (admit, urgent endoscopy, ICU consideration)

**Upper vs Lower GI Bleed:**

**Upper GI Bleed:**
- **Hematemesis** (coffee grounds or fresh blood)
- **Melaena** (black, tarry, foul-smelling stool)
- **Causes:**
  - **Peptic ulcer disease** (50%)
  - **Varices** (esophageal, gastric)
  - **Mallory-Weiss tear**
  - **Erosive gastritis**
  - **Malignancy**
  - **Angiodysplasia**

**Lower GI Bleed:**
- **Hematochezia** (fresh red blood per rectum)
- **Causes:**
  - **Diverticulosis** (most common)
  - **Angiodysplasia**
  - **Colorectal cancer**
  - **Inflammatory bowel disease**
  - **Hemorrhoids**
  - **Anal fissure**

**Immediate Management:**

**Resuscitation:**
- **ABC assessment**
- **Two large-bore IV cannulas**
- **Fluid resuscitation** (crystalloids, blood products)
- **Cross-match** (4-6 units PRBC)
- **Coagulation profile**, group and save

**Specific Measures:**

**For Variceal Bleed (Suspected):**
- **IV terlipressin** (1-2 mg IV 4-hourly)
- **IV antibiotics** (ceftriaxone 1g daily)
- **PPI** (not for varices, but for ulcer co-existent)
- **Urgent endoscopy** (within 12 hours)

**For Peptic Ulcer Bleed:**
- **IV PPI** (omeprazole 80mg bolus, then 8mg/hour infusion)
- **Endoscopic therapy:** Adrenaline injection, clips, heat probe
- **Consider:** Second-look endoscopy if high-risk

**Blood Transfusion Threshold:**
- **Hb < 7 g/dL** (stable patients)
- **Hb < 9 g/dL** (if active bleed, cardiovascular disease)
- **Platelets** if < 50 × 10^9/L (or < 20 × 10^9/L if stable)

**Red Flags (Emergency):**
- **Hemodynamic instability** (SBP < 90, HR > 120)
- **Hematemesis** (large volume, fresh blood)
- **Melaena** (large volume, ongoing)
- **Syncope**, postural hypotension
- **Comorbidities** (cardiovascular disease, anticoagulation)

**Discharge Criteria (Low Risk):**
- **Hemodynamically stable**
- **No further bleeding** (stable Hb, no melaena/hematemesis)
- **Rockall score 0-2**
- **Able to return** if symptoms recur
- **Follow-up endoscopy** arranged

**Sources:** NICE CG141, British Society of Gastroenterology 2024"""

        return DomainQueryResult(
            domain_name="gastroenterology",
            answer=answer,
            confidence=0.92,
            metadata={
                "specialty": "gastroenterology",
                "focus": "gi_bleed",
                "sources": ["NICE CG141", "BSG 2024"]
            }
        )

    def _interpret_lft(self, query: str, context: dict) -> DomainQueryResult:
        """Interpret liver function tests"""
        answer = """**Liver Function Test (LFT) Interpretation**

**Standard LFT Panel:**
- **ALT** (Alanine transaminase) - Liver-specific
- **AST** (Aspartate transaminase) - Liver, muscle, heart
- **ALP** (Alkaline phosphatase) - Liver, bone, placenta
- **GGT** (Gamma-glutamyl transferase) - Liver, biliary
- **Bilirubin** (Total & Direct) - Excretion
- **Albumin** - Synthetic function
- **PT/INR** - Synthetic function

**Normal Ranges (varies by lab):**
- **ALT:** 10-40 U/L (higher in men)
- **AST:** 10-35 U/L
- **ALP:** 30-130 U/L (higher in growing children, pregnancy)
- **GGT:** 0-60 U/L (higher in men)
- **Bilirubin:** < 21 µmol/L (< 1.2 mg/dL)
- **Albumin:** 35-50 g/L

**Pattern Recognition:**

**1. Hepatocellular Pattern:**
- **ALT >> AST** or **AST > ALT** (ratio < 2)
- **Causes:**
  - **Viral hepatitis** (ALT >> AST)
  - **NAFLD/NASH** (ALT > AST, but both < 4x normal)
  - **Drug-induced liver injury**
  - **Ischemic hepatitis** (shock liver) - AST >> ALT
  - **Cirrhosis** (AST > ALT, ratio > 2)

**2. Cholestatic Pattern:**
- **ALP >> ALT** (ALP > 2x normal, ALT/AST normal or mildly elevated)
- **Causes:**
  - **Biliary obstruction** (stone, stricture, tumor)
  - **Drug-induced** (antibiotics, oral contraceptives)
  - **Primary biliary cholangitis** (PBC)
  - **Primary sclerosing cholangitis** (PSC)

**3. Mixed Pattern:**
- **ALT/AST + ALP** both elevated
- **Causes:**
  - **Alcoholic liver disease** (AST > ALT, ratio > 2, GGT elevated)
  - **Drug-induced**
  - **Advanced cirrhosis**
  - **Infiltrative disease** (sarcoidosis, amyloidosis, metastases)

**AST:ALT Ratio:**

| Ratio | Interpretation |
|-------|---------------|
| **< 1** (ALT > AST) | Viral hepatitis, NAFLD |
| **1-2** | Cirrhosis, alcoholic hepatitis (early) |
| **> 2** (AST >> ALT) | **Alcoholic liver disease**, cirrhosis |
| **> 3** | Wilson's disease (consider in young) |

**GGT Interpretation:**
- **GGT elevated:** Confirms liver origin of elevated ALP
- **GGT normal + elevated ALP:** Bone origin (pregnancy, Paget's disease)

**Bilirubin Elevation:**

**Unconjugated (Indirect) Hyperbilirubinemia:**
- **Hemolysis** (increased bilirubin production)
- **Gilbert's syndrome** (mild, benign, unconjugated < 50 µmol/L)
- **Crigler-Najjar syndrome** (rare, severe)

**Conjugated (Direct) Hyperbilirubinemia:**
- **Biliary obstruction** (stone, stricture, cancer)
- **Hepatitis** (viral, alcoholic, drug-induced)
- **Cirrhosis**
- **Dubin-Johnson syndrome** (rare, benign)

**Synthetic Function:**
- **Albumin:** Half-life 20 days (chronic liver disease)
- **PT/INR:** Half-life hours- days (acute liver disease)
- **Both low:** Chronic liver disease with decompensation

**Alcohol vs. Non-Alcoholic Liver Disease:**

| Finding | Alcoholic | NAFLD/NASH |
|---------|-----------|------------|
| **AST:ALT** | > 2:1 | < 1:1 |
| **ALT** | < 300 U/L | Can be > 300 U/L |
| **GGT** | Markedly elevated | Mildly elevated |
| **MCV** | Elevated (macrocytosis) | Normal |
| **Clinical** | Alcohol use | Obesity, diabetes |

**Specific Abnormalities:**

**Isolated Elevated ALP:**
- **Pregnancy** (placental ALP)
- **Bone disease** (Paget's, osteomalacia, metastases)
- **Gilbert's syndrome** (benign)

**Isolated Elevated Bilirubin:**
- **Gilbert's syndrome** (unconjugated, mild, benign)
- **Hemolysis** (unconjugated, elevated LDH, low haptoglobin)
- **Rotor syndrome**, **Dubin-Johnson syndrome** (conjugated, benign)

**Isolated Elevated ALT:**
- **NAFLD** (most common)
- **Hepatitis** (viral, autoimmune)
- **Drug-induced**
- **Hemochromatosis** (iron overload)

**When to Refer:**
- **ALT/AST > 5x normal** (acute liver injury)
- **ALP > 2x normal** (biliary obstruction)
- **Bilirubin > 50 µmol/L** with other abnormal LFTs
- **Synthetic dysfunction** (low albumin, elevated INR)
- **Persistent abnormalities** (> 3 months)

**Sources:** NICE NG49, British Society of Gastroenterology 2024, ACG 2023"""

        return DomainQueryResult(
            domain_name="gastroenterology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "gastroenterology_hepatology",
                "focus": "lft_interpretation",
                "sources": ["NICE NG49", "BSG 2024", "ACG 2023"]
            }
        )

    def _manage_liver_disease(self, query: str, context: dict) -> DomainQueryResult:
        """Manage liver disease"""
        answer = """**Chronic Liver Disease Management**

**Etiology:**
- **Alcoholic liver disease** (40%)
- **NAFLD/NASH** (30% - increasing)
- **Viral hepatitis** (B, C)
- **Autoimmune hepatitis**
- **Hemochromatosis**, **Wilson's disease**, **Alpha-1 antitrypsin deficiency**

**Staging of Liver Fibrosis:**

**Metavir Score:**
- **F0:** No fibrosis
- **F1:** Portal fibrosis without septa
- **F2:** Portal fibrosis with few septa
- **F3:** Numerous septa without cirrhosis
- **F4:** Cirrhosis

**Assessment Tools:**
- **Fibroscan** (transient elastography)
- **APRI score:** (AST / Platelets) × 100
- **FIB-4 score:** (Age × AST) / (Platelets × √ALT)

**Complications of Cirrhosis:**

**1. Ascites:**
- **SAAG (Serum Ascites Albumin Gradient):**
  - **SAAG ≥ 1.1:** Portal hypertension (cirrhosis, heart failure)
  - **SAAG < 1.1:** Malignancy, tuberculosis, pancreatitis
- **Treatment:**
  - **Sodium restriction** (< 2 g/day)
  - **Spironolactone** 100-400 mg daily (aldosterone antagonist)
  - **Furosemide** 20-80 mg daily (add if diuretic-resistant)
  - **Therapeutic paracentesis** (if refractory, give albumin 6.8g/L removed)
  - **Consider TIPS** (transjugular intrahepatic portosystemic shunt)

**2. Variceal Bleeding:**
- **Primary prophylaxis:** Non-selective beta-blockers (propranolol, nadolol)
- **Acute bleeding:** IV terlipressin, IV antibiotics, urgent endoscopy
- **Secondary prophylaxis:** Beta-blockers + endoscopic band ligation

**3. Hepatic Encephalopathy:**
- **Grades:**
  - **1:** Mild confusion, sleep inversion
  - **2:** Drowsiness, disorientation, asterixis
  - **3:** Marked confusion, incoherent
  - **4:** Coma
- **Treatment:**
  - **Lactulose** 15-30 mL TID-QID (titrate to 2-3 soft stools/day)
  - **Rifaximin** 550 mg BID (add if refractory)
  - **Treat precipitants:** Infection, GI bleed, constipation, sedatives

**4. Hepatorenal Syndrome (HRS):**
- **Definition:** Renal failure in cirrhosis without intrinsic renal disease
- **Type 1:** Rapid doubling of creatinine to > 2.5 mg/dL (2 weeks)
- **Type 2:** Moderate, stable renal failure
- **Treatment:** Midodrine + octreotide + albumin, consider liver transplant

**5. Hepatocellular Carcinoma (HCC):**
- **Surveillance:** Ultrasound ± AFP every 6 months (all cirrhotics)
- **Risk factors:** HCV, HBV, alcohol, NAFLD, hemochromatosis
- **Treatment:** Resection, transplant, RFA, TACE, sorafenib (advanced)

**Management Principles:**

**General Measures:**
- **Alcohol cessation** (if alcoholic)
- **Weight loss** (if NAFLD/NASH)
- **Hepatitis B vaccination** (if not immune)
- **Avoid hepatotoxins:** NSAIDs, statins (adjust dose), acetaminophen < 2 g/day

**Vaccinations:**
- **Hepatitis A** (if seronegative)
- **Hepatitis B** (if seronegative)
- **Influenza** (annual)
- **Pneumococcal** (every 5 years)
- **COVID-19** (as per guidelines)

**Nutrition:**
- **Adequate protein** (unless encephalopathy, then moderate restriction)
- **Sodium restriction** (< 2 g/day if ascites)
- **Avoid raw shellfish** (Vibrio vulnificus risk)

**Drug Dosing:**
- **Reduce dose** for drugs metabolized by liver (avoid in severe cirrhosis)
- **Avoid:** NSAIDs, ACE inhibitors (if renal dysfunction)
- **Caution:** Sedatives, opioids (encephalopathy risk)

**When to Refer for Liver Transplant Evaluation:**
- **MELD score ≥ 15** (Model for End-Stage Liver Disease)
- **Complications:** Refractory ascites, encephalopathy, variceal bleeding
- **HCC** within Milan criteria (single tumor ≤ 5 cm, or ≤ 3 tumors ≤ 3 cm)
- **Quality of life** significantly affected

**Sources:** NICE NG49, AASLD 2023, EASL 2023"""

        return DomainQueryResult(
            domain_name="gastroenterology",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "gastroenterology_hepatology",
                "focus": "liver_disease",
                "sources": ["NICE NG49", "AASLD 2023", "EASL 2023"]
            }
        )

    def _manage_hepatitis(self, query: str, context: dict) -> DomainQueryResult:
        """Manage hepatitis"""
        answer = """**Hepatitis Management**

**Viral Hepatitis:**

**Hepatitis A (HAV):**
- **Transmission:** Fecal-oral (contaminated food/water)
- **Clinical:** Acute, never chronic, fulminant hepatitis rare
- **Treatment:** Supportive, no specific therapy
- **Prevention:** HAV vaccine (high-risk groups), hand hygiene

**Hepatitis B (HBV):**
- **Transmission:** Blood, sexual, perinatal
- **Acute vs Chronic:**
  - **Chronic:** > 90% if neonatal, 5-10% if adult
- **Serology:**
  - **HBsAg:** Current infection (acute or chronic)
  - **Anti-HBc:** Past or current infection
  - **Anti-HBs:** Immunity (vaccination or past infection)
  - **HBeAg:** High infectivity, active replication
  - **HBV DNA:** Viral load (treatment monitoring)
- **Treatment Indications (Chronic):**
  - **HBV DNA > 2,000 IU/mL** (HBeAg-negative)
  - **HBV DNA > 20,000 IU/mL** (HBeAg-positive)
  - **ALT elevated**, significant fibrosis (F3/F4)
  - **Decompensated cirrhosis** (treat regardless of viral load)
- **First-line:**
  - **Entecavir** 0.5 mg daily (or 1 mg if lamivudine-experienced)
  - **Tenofovir TAF** 25 mg daily (or TDF 300 mg daily)
- **Duration:** Long-term (usually lifelong)
- **Monitoring:** ALT, HBV DNA every 3-6 months
- **Prevention:** HBV vaccine (universal vaccination)

**Hepatitis C (HCV):**
- **Transmission:** Blood (IVDU, blood transfusion before 1992, tattoos)
- **Chronic:** 80% (acute rarely symptomatic)
- **Genotyping:** 1-6 (genotype 1 most common in UK/US)
- **Treatment:** **Direct-acting antivirals (DAAs)**
  - **Sofosbuvir/velpatasvir** (Epclusa) 400/100 mg daily for 12 weeks
  - **Glecaprevir/pibrentasvir** (Mavyret) for 8-12 weeks
  - **Cure rate (SVR12):** > 95%
- **Indications:** All chronic HCV (treat all, regardless of fibrosis)
- **Monitoring:** HCV RNA at 12 weeks post-treatment (SVR12 = cure)
- **Prevention:** No vaccine, harm reduction (clean needles, safe sex)

**Hepatitis D (HDV):**
- **Defective virus** (requires HBV coinfection)
- **Transmission:** Blood, sexual
- **Clinical:** More severe than HBV alone, rapid progression to cirrhosis
- **Treatment:** Pegylated interferon (cure rate ~ 30%), bulevirtide (new)

**Hepatitis E (HEV):**
- **Transmission:** Fecal-oral (undercooked pork, deer meat)
- **Clinical:** Acute, self-limited (except in pregnancy, immunocompromised)
- **Treatment:** Supportive, ribavirin (if chronic)

**Autoimmune Hepatitis:**
- **Type 1:** ANA, ASMA positive (women, older adults)
- **Type 2:** Anti-LKM1 positive (children, young adults)
- **Clinical:** Acute or chronic, can present as fulminant hepatitis
- **Treatment:**
  - **Prednisolone** 1 mg/kg/day (induction)
  - **Azathioprine** 1-2 mg/kg/day (maintenance, steroid-sparing)
  - **Goal:** Remission (normal ALT, IgG)
  - **Relapse:** Common (50-90%), require long-term low-dose steroids

**Alcoholic Hepatitis:**
- **Clinical:** Jaundice, fever, leukocytosis, AST > ALT (ratio > 2)
- **Severe (Maddrey's Discriminant Function ≥ 32):**
  - **Prednisolone** 40 mg daily for 28 days (or pentoxifylline if contraindicated)
  - **Mortality:** 30-50% without treatment
- **Treatment:** Alcohol cessation, nutritional support

**Drug-Induced Liver Injury (DILI):**
- **Common culprits:**
  - **Acetaminophen** (dose-dependent, NAC antidote)
  - **Antibiotics** (amoxicillin-clavulanate, nitrofurantoin)
  - **NSAIDs** (diclofenac, ibuprofen)
  - **Statins** (rare, usually mild)
  - **Anti-epileptics** (valproate, phenytoin)
  - **Herbal supplements** (green tea extract, kava)
- **Pattern:** Hepatocellular (ALT >> AST), cholestatic (ALP >> ALT), mixed
- **Treatment:** Stop offending drug, supportive care

**Sources:** NICE CG165, AASLD 2023, EASL 2023"""

        return DomainQueryResult(
            domain_name="gastroenterology",
            answer=answer,
            confidence=0.89,
            metadata={
                "specialty": "gastroenterology_hepatology",
                "focus": "hepatitis",
                "sources": ["NICE CG165", "AASLD 2023", "EASL 2023"]
            }
        )

    def _assess_pancreatitis(self, query: str, context: dict) -> DomainQueryResult:
        """Assess pancreatitis"""
        answer = """**Pancreatitis Assessment**

**Acute Pancreatitis:**

**Definition:** Inflammation of the pancreas (acute onset)

**Etiology:**
- **Gallstones** (40-50%) - most common
- **Alcohol** (25-35%)
- **Hypertriglyceridemia** (> 1,000 mg/dL or 11 mmol/L)
- **ERCP** (post-procedure)
- **Drugs:** Azathioprine, valproate, sulfonamides, diuretics
- **Trauma**, **autoimmune pancreatitis**, **infection** (mumps, CMV)
- **Idiopathic** (10%)

**Diagnosis (2 of 3 criteria):**
1. **Characteristic abdominal pain** (epigastric, radiates through to back)
2. **Amylase/Lipase > 3x upper limit of normal**
   - **Amylase:** Rises 4-8 hours, normalizes in 3-5 days
   - **Lipase:** More specific, rises 4-8 hours, normalizes in 8-14 days
3. **Imaging findings** (CT abdomen, characteristic inflammation)

**Severity Assessment:**

**Ranson's Criteria (at admission, 48 hours):**

| At Admission | At 48 Hours |
|--------------|-------------|
| Age > 55 | Hct ↓ > 10% |
| WBC > 16,000 | BUN ↑ > 5 mg/dL |
| Glucose > 11 mmol/L | Calcium < 2 mmol/L |
| AST > 250 U/L | PaO2 < 60 mmHg |
| LDH > 350 U/L | Base deficit > 4 |
| Amylase > 5x ULN | Fluid sequestration > 6 L |

**Severity:**
- **0-2:** Mild (< 5% mortality)
- **3-5:** Moderate (10-20% mortality)
- **6-11:** Severe (> 50% mortality)

**Modified Glasgow Score (Imrie):**
- Similar to Ranson's, UK guidelines

**CT Severity Index (CTSI):**
- Grade A-E (0-10 points)
- **≥ 7 points:** Severe pancreatitis, high necrosis risk

**Management:**

**Initial Resuscitation:**
- **IV fluids:** Aggressive hydration (LR or NS, 250-500 mL/hour)
- **Goal:** Urine output > 0.5 mL/kg/hour
- **Analgesia:** IV opioids (morphine, fentanyl)
- **Anti-emetics:** Ondansetron, metoclopramide
- **Nutrition:** Early oral feeding if tolerated, else NG feeding (avoid TPN)

**Specific Measures:**

**Gallstone Pancreatitis:**
- **ERCP** (within 72 hours) if:
  - **Cholangitis** (fever, jaundice, pain)
  - **Persistent biliary obstruction** (bilirubin, ALP not improving)
- **Cholecystectomy** (same admission) once pancreatitis resolved

**Severe Pancreatitis:**
- **ICU admission** (organ failure, necrosis)
- **Antibiotics** (only if infected necrosis proven)
- **Necrosectomy** (infected pancreatic necrosis not responding to antibiotics)

**Complications:**
- **Necrosis** (sterile vs. infected)
- **Organ failure** (respiratory, renal, cardiovascular)
- **Pseudocyst** (fluid collection, > 4 weeks)
- **Abscess** (infected collection)
- **Systemic complications** (ARDS, AKI, DIC)

**Chronic Pancreatitis:**

**Etiology:**
- **Alcohol** (most common in developed countries)
- **Tropical pancreatitis** (developing countries)
- **Genetic** (CFTR, PRSS1 mutations)
- **Autoimmune**
- **Idiopathic**

**Clinical Features:**
- **Recurrent episodes** of acute pancreatitis
- **Chronic abdominal pain** (epigastric, radiates through to back)
- **Steatorrhea** (fatty stool, malabsorption)
- **Diabetes mellitus** (pancreatic destruction)
- **Calcifications** on imaging

**Diagnosis:**
- **CT abdomen:** Calcifications, ductal dilation, atrophy
- **MRCP:** Ductal abnormalities (chain-of-lakes)
- **Fecal elastase:** < 200 µg/g (exocrine insufficiency)

**Treatment:**
- **Pain control:** Pregabalin, TCAs, celiac plexus block
- **Pancreatic enzymes:** Creon 25,000-75,000 units with meals
- **Diabetes:** Insulin (often required)
- **Surgical:** Frey's procedure, Whipple (if severe, refractory)
- **Alcohol cessation:** Critical to prevent progression

**Sources:** NICE CG104, American Pancreatic Association 2023, RCP 2024"""

        return DomainQueryResult(
            domain_name="gastroenterology",
            answer=answer,
            confidence=0.88,
            metadata={
                "specialty": "gastroenterology_pancreas",
                "focus": "pancreatitis",
                "sources": ["NICE CG104", "APA 2023", "RCP 2024"]
            }
        )

    def _manage_ibd(self, query: str, context: dict) -> DomainQueryResult:
        """Manage inflammatory bowel disease"""
        answer = """**Inflammatory Bowel Disease (IBD) Management**

**Types:**

**Crohn's Disease:**
- **Transmural inflammation** (can affect entire bowel wall)
- **Skip lesions** (normal areas between inflamed areas)
- **Can affect any part** of GI tract (mouth to anus)
- **Common:** Terminal ileum, colon
- **Complications:** Strictures, fistulas, abscesses

**Ulcerative Colitis (UC):**
- **Mucosal inflammation only** (superficial)
- **Continuous inflammation** (no skip lesions)
- **Limited to colon** (rectum to entire colon)
- ** bloody diarrhea**, mucus, urgency
- **Complications:** Toxic megacolon, colon cancer

**Indeterminate Colitis:**
- Features of both Crohn's and UC
- Diagnosis becomes clearer over time

**Clinical Presentation:**

**Crohn's Disease:**
- **Abdominal pain** (RLQ, periumbilical)
- **Diarrhea** (non-bloody, but can be bloody)
- **Weight loss**, malnutrition
- **Perianal disease** (fissures, fistulas, abscesses)
- **Systemic:** Fever, fatigue, arthralgia, erythema nodosum

**Ulcerative Colitis:**
- **Bloody diarrhea** (hallmark)
- **Urgency**, tenesmus
- **Mucus discharge**
- **Lower abdominal pain**
- **Systemic:** Fever, weight loss (severe disease)

**Diagnosis:**

**Endoscopic:**
- **Colonoscopy with biopsy** (gold standard)
- **Crohn's:** Aphthous ulcers, cobblestoning, skip lesions
- **UC:** Continuous erythema, ulceration, friability, pseudopolyps

**Radiologic:**
- **MRI enterography** (Crohn's - small bowel involvement)
- **CT abdomen** (acute complications, perforation)

**Laboratory:**
- **Fecal calprotectin** (inflammatory marker, > 100 µg/g suggests IBD)
- **CRP, ESR** (elevated in active disease)
- **pANCA** (UC), **ASCA** (Crohn's) (limited utility)
- **Exclude infection:** C. difficile, stool culture, ova & parasites

**Disease Severity:**

**Ulcerative Colitis (Mayo Score):**
- **Mild:** < 4 stools/day, no systemic symptoms
- **Moderate:** 4-6 stools/day, mild systemic symptoms
- **Severe:** > 6 stools/day, fever, tachycardia, anemia, ESR > 30

**Crohn's Disease (CDAI):**
- **Remission:** CDAI < 150
- **Mild-moderate:** CDAI 150-450
- **Severe:** CDAI > 450 (or complications: fistula, abscess)

**Treatment:**

**Mild-Moderate Disease:**

**Ulcerative Colitis:**
- **5-ASA agents:**
  - **Mesalamine** (oral 2.4-4.8 g/day, suppository/enema for distal disease)
  - **Sulfasalazine** (if cost limitation, monitor for sulfa allergy)
- **Topical therapy:** Mesalamine enema/suppository (distal disease)

**Crohn's Disease:**
- **Budesonide** (ileal/ascending colon disease, less systemic)
- **5-ASA** (limited efficacy)

**Moderate-Severe Disease:**

**Steroids:**
- **Prednisolone** 40-60 mg daily (induction, not maintenance)
- **Taper** over 6-8 weeks once remission achieved
- **Budesonide** (ileal disease, fewer side effects)

**Immunomodulators:**
- **Azathioprine** 2-2.5 mg/kg/day (take 6-12 weeks to work)
- **6-Mercaptopurine** 1-1.5 mg/kg/day
- **Methotrexate** 15-25 mg weekly (Crohn's)
- **Monitoring:** FBC, LFTs (azathioprine: TPMT testing first)

**Biologics:**
- **Anti-TNF:** Infliximab, adalimumab (moderate-severe, fistulizing)
- **Anti-integrin:** Vedolizumab (gut-selective)
- **Anti-IL12/23:** Ustekinumab
- **Anti-IL23:** Risankizumab

**Small Molecules:**
- **JAK inhibitors:** Tofacitinib, upadacitinib (UC, moderate-severe)
- **S1P receptor modulators:** Ozanimod

**Acute Severe Ulcerative Colitis:**

**Management:**
- **IV steroids:** Methylprednisolone 60 mg daily
- **IV fluids**, **electrolyte replacement**
- **Avoid:** Antidiarrheals (risk of toxic megacolon)
- **Monitor:** Daily abdominal X-ray (toxic megacolon), CRP
- **Rescue therapy** (if no improvement in 3-5 days):
  - **Infliximab** 5 mg/kg (day 0, 2, 6)
  - **Cyclosporine** 2 mg/kg (IV)
- **Colectomy** (if medical therapy fails)

**Complications:**

**Crohn's:**
- **Strictures:** Balloon dilation, surgical resection
- **Fistulas:** Antibiotics (metronidazole, ciprofloxacin), anti-TNF, surgery
- **Abscesses:** Percutaneous drainage, antibiotics

**Ulcerative Colitis:**
- **Toxic megacolon:** IV steroids, surgical consult (colectomy)
- **Colorectal cancer:** Surveillance colonoscopy (every 1-3 years)

**Maintenance Therapy:**
- **5-ASA** (mild disease)
- **Azathioprine/6-MP** (moderate-severe)
- **Biologics** (moderate-severe, steroid-dependent)

**Sources:** NICE CG130, ECCO Guidelines 2023, British Society of Gastroenterology 2024"""

        return DomainQueryResult(
            domain_name="gastroenterology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "gastroenterology_ibd",
                "focus": "ibd_management",
                "sources": ["NICE CG130", "ECCO 2023", "BSG 2024"]
            }
        )

    def _manage_ibs(self, query: str, context: dict) -> DomainQueryResult:
        """Manage irritable bowel syndrome"""
        answer = """**Irritable Bowel Syndrome (IBS) Management**

**Definition:**
- **Chronic, recurrent** abdominal pain associated with defecation or change in bowel habits
- **Functional disorder** (no structural/biochemical abnormality)

**Rome IV Diagnostic Criteria:**
- **Recurrent abdominal pain** (at least 1 day/week in last 3 months)
- **Associated with ≥ 2 of:**
  1. **Defecation** (pain improves or worsens with bowel movement)
  2. **Change in stool frequency**
  3. **Change in stool form/appearance**
- **Onset > 6 months ago**

**IBS Subtypes:**
- **IBS-D:** Diarrhea-predominant (> 25% loose stools)
- **IBS-C:** Constipation-predominant (> 25% hard stools)
- **IBS-M:** Mixed (both diarrhea and constipation)
- **IBS-U:** Unclassified (insufficient data)

**Epidemiology:**
- **Prevalence:** 10-15% (more common in women)
- **Age:** 20-40 years (can occur at any age)
- **Chronic:** Symptoms persist for years, wax and wane

**Clinical Features:**
- **Abdominal pain/discomfort** (cramping, bloating, relieved by defecation)
- **Altered bowel habits** (diarrhea, constipation, or alternating)
- **Bloating, distension**, flatulence
- **Mucus in stool** (no blood)
- **Systemic symptoms:** Fatigue, headache, dysmenorrhea, dyspareunia
- **Psychiatric comorbidity:** Anxiety, depression (40-60%)

**Red Flags (Exclude organic disease):**
- **Rectal bleeding** (not attributable to hemorrhoids)
- **Unintentional weight loss**
- **Nocturnal symptoms** (wake from sleep to defecate)
- **Family history** of colon cancer, IBD, celiac disease
- **Age > 50** with new symptoms (colonoscopy required)
- **Fever**, anemia

**Diagnosis:**
- **Clinical** (Rome IV criteria)
- **Limited investigations:**
  - **Fecal calprotectin** (distinguish from IBD)
  - **Celiac serology** (tTG IgA)
  - **CBC** (anemia, infection)
  - **CRP, ESR** (inflammation)
- **Colonoscopy** (if red flags, age > 50, or uncertain diagnosis)

**Management:**

**General Measures:**
- **Reassurance** (benign condition, not life-threatening)
- **Education** (identify triggers, stress management)
- **Regular exercise** (improves symptoms)
- **Adequate sleep** (7-9 hours/night)

**Dietary Modifications:**

**First-line:**
- **Regular meals**, avoid skipping meals
- **Reduce:** Alcohol, caffeine, spicy foods, fatty foods
- **Increase:** Fiber (gradual, 20-30 g/day)
- **Hydration** (2-3 L/day)
- **Probiotics** (some evidence for certain strains)

**Low FODMAP Diet:**
- **Fermentable Oligosaccharides, Disaccharides, Monosaccharides, Polyols**
- **Elimination phase** (2-6 weeks): Restrict high FODMAP foods
- **Reintroduction phase:** Gradually reintroduce to identify triggers
- **High FODMAP foods to avoid:**
  - **Fructans:** Wheat, onions, garlic
  - **Lactose:** Milk, yogurt, soft cheese
  - **Fructose:** Fruits (apple, pear, watermelon), honey
  - **Polyols:** Stone fruits, mushrooms, artificial sweeteners (sorbitol, mannitol)
  - **Galactans:** Legumes (beans, lentils)

**Pharmacological Therapy:**

**IBS-D (Diarrhea-predominant):**
- **Loperamide** 2-4 mg PRN (antisecretory, slows transit)
- **Colestyramine** 4 g BD (bile acid sequestrant, if postprandial diarrhea)
- **Eluxadoline** 75-100 mg BD (if loperamide ineffective)
- **Rifaximin** 550 mg TID for 14 days (if bloating predominant)
- **Alosetron** (women only, severe IBS-D, specialist initiation)

**IBS-C (Constipation-predominant):**
- **Polyethylene glycol** 17 g daily (laxative)
- **Linaclotide** 290 mcg daily (guanylate cyclase agonist)
- **Plecanatide** 3 mg daily
- **Lubiprostone** 8 mcg BID

**IBS-M (Mixed):**
- **Combination therapy** (antidiarrheal + laxative as needed)

**Abdominal Pain/Bloating:**
- **Antispasmodics** (mebeverine 135 mg TDS, hyoscine butylbromide 10 mg TDS)
- **Peppermint oil** (capsules, 180-200 mg TID)
- **TCAs** (amitriptyline 10-50 mg at night - neuromodulatory, not antidepressant dose)
- **SSRIs** (if anxiety/depression prominent)

**Psychological Therapies:**
- **CBT** (cognitive-behavioral therapy)
- **Gut-directed hypnotherapy**
- **Mindfulness-based stress reduction**
- **Psychodynamic therapy** (if trauma/abuse history)

**Follow-up:**
- **Regular review** (every 3-6 months)
- **Reassessment** if symptoms change (red flags develop)
- **Medication adjustment** (minimize long-term use)

**Sources:** NICE CG61, British Society of Gastroenterology 2024, ACG 2021"""

        return DomainQueryResult(
            domain_name="gastroenterology",
            answer=answer,
            confidence=0.90,
            metadata={
                "specialty": "gastroenterology_functional",
                "focus": "ibs_management",
                "sources": ["NICE CG61", "BSG 2024", "ACG 2021"]
            }
        )

    def _manage_gerd(self, query: str, context: dict) -> DomainQueryResult:
        """Manage GERD"""
        answer = """**GORD (GERD) - Gastroesophageal Reflux Disease Management**

**Definition:**
- **Backflow of gastric contents** into esophagus causing symptoms/mucosal damage
- **GORD** (UK), **GERD** (US)

**Symptoms:**
- **Heartburn** (retrosternal burning, worse after meals, lying down)
- **Acid reflux** (sour taste in mouth, regurgitation)
- **Dysphagia** (difficulty swallowing - alarming symptom, refer urgently)
- **Odynophagia** (painful swallowing - alarming symptom, refer urgently)
- **Atypical symptoms:** Chronic cough, hoarseness, asthma, chest pain

**Diagnosis:**
- **Clinical** (typical symptoms in absence of red flags)
- **PPI trial** (omeprazole 20 mg daily for 4 weeks - if improves, likely GORD)
- **Endoscopy** (if red flags, age > 55, symptoms > 5 years, atypical symptoms)

**Red Flags (Urgent Endoscopy - 2-week wait):**
- **Dysphagia** (progressive)
- **Odynophagia**
- **Weight loss** (unintentional)
- **GI bleeding** (anemia, melaena, hematemesis)
- **Persistent vomiting**
- **Family history** of upper GI cancer
- **Age > 55** with new-onset symptoms

**Management:**

**Lifestyle Modifications (First-line):**
- **Weight loss** (if overweight/obese)
- **Head of bed elevation** (15-20 cm, blocks, not extra pillows)
- **Avoid:** Large meals, eating within 3 hours of bedtime
- **Avoid:** Acidic foods (citrus, tomato), spicy foods, fatty foods
- **Avoid:** Caffeine, alcohol, chocolate (relax LES)
- **Avoid:** Smoking (relax LES)
- **Loose clothing** (avoid tight waistbands)

**Pharmacological Therapy:**

**Antacids/Alginates (Mild/Intermittent Symptoms):**
- **Antacids:** Calcium carbonate, magnesium hydroxide (neutralize acid)
- **Alginates:** Gaviscon (form raft, protects esophagus)
- **Take:** After meals, at bedtime

**H2-Receptor Antagonists (Moderate Symptoms):**
- **Ranitidine** 150 mg BD (off-label, supply issues)
- **Famotidine** 20 mg BD
- **Duration:** 2-4 weeks, then reassess

**Proton Pump Inhibitors (PPIs) (Moderate-Severe Symptoms):**

**First-line PPIs:**
- **Omeprazole** 20 mg daily (before breakfast)
- **Lansoprazole** 15-30 mg daily (before breakfast)
- **Esomeprazole** 20 mg daily (before breakfast)
- **Pantoprazole** 20-40 mg daily (before breakfast)

**Dosing:**
- **Standard:** Once daily (before breakfast)
- **Severe:** Twice daily (before breakfast and evening meal)
- **Refractory:** Increase to twice daily (switch to different PPI)

**Duration:**
- **4-8 weeks** (initial treatment)
- **Reassess:** If improved, taper to lowest effective dose
- **Maintenance:** Consider if symptoms recur off therapy

**Refractory GORD (PPI Failure):**
- **Check compliance** (taking before breakfast)
- **Double dose** PPI (twice daily)
- **Switch PPI** (omeprazole → esomeprazole)
- **Add H2RA** at night (famotidine)
- **Consider:** H. pylori test and treat (if positive)
- **Reflux monitoring:** pH/impedance testing
- **Manometry:** (if anti-reflux surgery considered)

**Complications:**

**Esophagitis:**
- **Grade A-D:** Los Angeles classification
- **Treatment:** PPI 8 weeks, repeat endoscopy to confirm healing

**Barrett's Esophagus:**
- **Definition:** Intestinal metaplasia in distal esophagus (precancerous)
- **Risk factors:** Chronic GORD, age > 50, male, Caucasian, obesity
- **Management:**
  - **PPI** (lifelong, high-dose)
  - **Surveillance endoscopy** every 2-3 years
  - **If dysplasia:** Endoscopic therapy (RFA, ablation)

**Esophageal Stricture:**
- **Dysphagia** to solids, then liquids
- **Treatment:** Endoscopic dilation (repeated if needed)

**Surgical Options:**
- **Laparoscopic fundoplication** (Nissen, Toupet)
- **Indications:**
  - **Refractory GORD** (despite maximal PPI)
  - **Large hiatal hernia**
  - **Preference for surgery** (lifelong PPI)
- **Success rate:** 85-90% at 5 years

**Sources:** NICE CG184, British Society of Gastroenterology 2024, ACG 2022"""

        return DomainQueryResult(
            domain_name="gastroenterology",
            answer=answer,
            confidence=0.89,
            metadata={
                "specialty": "gastroenterology_uppergi",
                "focus": "gerd_management",
                "sources": ["NICE CG184", "BSG 2024", "ACG 2022"]
            }
        )

    def _manage_peptic_ulcer(self, query: str, context: dict) -> DomainQueryResult:
        """Manage peptic ulcer disease"""
        answer = """**Peptic Ulcer Disease Management**

**Definition:**
- **Break in mucosa** of stomach/duodenum (≥ 3 mm)
- **Gastric ulcer** (stomach), **Duodenal ulcer** (duodenum)

**Etiology:**
- **H. pylori infection** (70-90%)
- **NSAIDs/aspirin** (10-30%)
- **Stress ulcers** (critical illness, burns)
- **Zollinger-Ellison syndrome** (gastrinoma, rare)

**Clinical Presentation:**

**Duodenal Ulcer:**
- **Epigastric pain** (burning, gnawing)
- **Pain → Food** (worse with empty stomach, improves with meals)
- **Night pain** (wakes patient from sleep)
- **Periodicity** (episodes of pain followed by remission)

**Gastric Ulcer:**
- **Epigastric pain** (worse with food)
- **Nausea, vomiting**, weight loss
- **Anemia** (chronic blood loss)

**Complications:**
- **GI bleeding** (hematemesis, melaena)
- **Perforation** (sudden severe pain, board-like abdomen)
- **Gastric outlet obstruction** (vomiting, weight loss)
- **Penetration** (into pancreas, biliary tree)

**Diagnosis:**
- **Endoscopy** (gold standard, visualize ulcer, biopsy gastric ulcers to exclude malignancy)
- **H. pylori testing:** Urea breath test, stool antigen, biopsy (CLOtest)
- **NOT** serology (not useful, remains positive after eradication)

**Management:**

**H. pylori Eradication (if positive):**

**First-line (Triple Therapy):**
- **PPI** (omeprazole 20 mg) BD
- **Amoxicillin** 1 g BD
- **Clarithromycin** 500 mg BD
- **Duration:** 14 days
- **Eradication rate:** 85-90%

**Second-line (if first-line fails):**
- **PPI** BD
- **Metronidazole** 400 mg TDS
- **Clarithromycin** 500 mg BD
- **Duration:** 14 days

**Alternative (Penicillin Allergy):**
- **PPI** BD
- **Clarithromycin** 500 mg BD
- **Metronidazole** 400 mg TDS
- **Duration:** 14 days

**Confirm Eradication:**
- **Urea breath test** or **stool antigen** (≥ 4 weeks after completing therapy, off PPI 2 weeks)

**NSAID-Associated Ulcers:**

**Primary Prevention (if NSAID required):**
- **PPI** (omeprazole 20 mg daily)
- **COX-2 selective inhibitor** (celecoxib, etoricoxib)
- **Misoprostol** (if PPI contraindicated)

**Treatment:**
- **Stop NSAID** (if possible)
- **PPI** (omeprazole 20-40 mg daily) for 4-8 weeks
- **Continue PPI** (if NSAID must be continued)

**Idiopathic Ulcers (H. pylori negative, not on NSAIDs):**
- **PPI** (omeprazole 20-40 mg daily)
- **Continue long-term PPI** (high recurrence rate)

**Follow-up:**
- **Gastric ulcer:** Repeat endoscopy in 6-8 weeks (exclude malignancy, confirm healing)
- **Duodenal ulcer:** NOT routinely repeat endoscoped (if healed on PPI, H. pylori negative)

**Red Flags (Urgent Referral):**
- **Weight loss**, dysphagia (gastric cancer)
- **Persistent vomiting** (gastric outlet obstruction)
- **Family history** of upper GI cancer
- **Age > 55** (urgent endoscopy)

**Sources:** NICE CG184, Maastricht VI/Florence Consensus 2022, ACG 2022"""

        return DomainQueryResult(
            domain_name="gastroenterology",
            answer=answer,
            confidence=0.88,
            metadata={
                "specialty": "gastroenterology_uppergi",
                "focus": "peptic_ulcer",
                "sources": ["NICE CG184", "Maastricht VI 2022", "ACG 2022"]
            }
        )

    def _assess_coeliac(self, query: str, context: dict) -> DomainQueryResult:
        """Assess coeliac disease"""
        answer = """**Coeliac Disease Assessment**

**Definition:**
- **Autoimmune condition** triggered by gluten ingestion
- **Genetic predisposition** (HLA-DQ2/DQ8)
- **Small bowel villous atrophy** → malabsorption

**Epidemiology:**
- **Prevalence:** 1% (many undiagnosed)
- **Age:** Any age (including elderly)
- **Gender:** Female predominance (2:1)
- **Association:** Type 1 diabetes, autoimmune thyroiditis, Down syndrome

**Clinical Presentation:**

**Classical (Malabsorption):**
- **Diarrhea**, steatorrhea (fatty, floating stool)
- **Abdominal distension**, bloating, flatulence
- **Weight loss**, failure to thrive (children)
- **Nutritional deficiencies:** Iron, folate, B12, vitamin D

**Non-Classical (Extra-intestinal):**
- **Fatigue**, lethargy (iron deficiency anemia)
- **Dermatitis herpetiformis** (blistering rash)
- **Neurological:** Peripheral neuropathy, ataxia, migraine
- **Recurrent miscarriage**, infertility
- **Elevated transaminases** (liver enzymes)
- **Osteoporosis** (calcium malabsorption)

**Silent (Asymptomatic):**
- **Incidental finding:** Iron deficiency, osteoporosis
- **Screening:** High-risk groups (type 1 diabetes, first-degree relatives)

**Diagnosis:**

**Serology (while on gluten-containing diet):**
- **tTG IgA** (tissue transglutaminase IgA) - first-line, highly sensitive/specific
- **Total IgA** (to exclude IgA deficiency - 2-3% of coeliacs)
- **If IgA deficient:** tTG IgG, DGP IgG (deamidated gliadin peptide)
- **EMA IgA** (endomysial antibody) - confirmatory, specialist use

**Confirmatory Test:**
- **Duodenal biopsy** (4-6 biopsies from distal duodenum + bulb)
- **Findings:** Villous atrophy, crypt hyperplasia, intraepithelial lymphocytes
- **Marsh classification:** Grade 0-3 (3 = total villous atrophy)

**Diagnosis Criteria:**
- **Positive serology** + **characteristic biopsy** = coeliac disease
- **If serology negative** + **biopsy positive** → consider seronegative coeliac (rare)

**Gluten Challenge:**
- **If already gluten-free:** Restart gluten (3 g/day, equivalent to 2 slices of bread) for 6 weeks before testing

**Treatment:**

**Lifelong Gluten-Free Diet (GFD):**

**Foods to Avoid (Contain Gluten):**
- **Wheat** (bread, pasta, couscous, seitan)
- **Barley** (malt, beer, food additives)
- **Rye** (bread, crackers)
- **Triticale** (wheat-rye hybrid)
- **Processed foods** (sauces, gravies, soups - read labels)

**Naturally Gluten-Free:**
- **Rice**, **corn**, **quinoa**, **potato**
- **Meat, fish, eggs**
- **Fruits, vegetables**
- **Dairy** (most)
- **Legumes, nuts, seeds**

**Gluten-Free Alternatives:**
- **Gluten-free bread**, **pasta**, **flour** (rice, almond, coconut)
- **Oats** (certified gluten-free - cross-contamination risk)

**Dietitian Referral:**
- **Essential** for education, support, monitoring
- **Coeliac UK** (charity, resources)

**Monitoring:**
- **tTG IgA** (at diagnosis, 6-12 months, then annually)
- **Dietician review** (annual)
- **Bone density** (DEXA - baseline, repeat if abnormal)
- **Vaccination:** Pneumococcal (if hyposplenism), annual influenza

**Complications:**
- **Osteoporosis** (calcium + vitamin D supplementation)
- **Hyposplenism** (atrophic spleen, increased infection risk)
- **Refractory coeliac disease** (rare, no response to GFD, specialist management)
- **Intestinal lymphoma** (rare, increased risk if untreated)

**Sources:** NICE NG20, British Society of Gastroenterology 2024, Coeliac UK 2023"""

        return DomainQueryResult(
            domain_name="gastroenterology",
            answer=answer,
            confidence=0.91,
            metadata={
                "specialty": "gastroenterology_smallbowel",
                "focus": "coeliac_disease",
                "sources": ["NICE NG20", "BSG 2024", "Coeliac UK 2023"]
            }
        )

    def _handle_diarrhea(self, query: str, context: dict) -> DomainQueryResult:
        """Handle diarrhea queries"""
        answer = """**Diarrhea Assessment**

**Definition:**
- **Acute:** < 14 days
- **Persistent:** 14-30 days
- **Chronic:** > 30 days

**Acute Diarrhea (< 14 days):**

**Etiology:**
- **Infectious (90%):**
  - **Viral:** Norovirus, rotavirus (most common)
  - **Bacterial:** Salmonella, Campylobacter, Shigella, E. coli
  - **Parasitic:** Giardia, Cryptosporidium, Entamoeba
- **Non-infectious:** Medications, toxins, ischemia, inflammation

**Assessment:**
- **History:** Travel, food exposure, sick contacts, medications
- **Red flags:** Bloody diarrhea, fever, signs of dehydration, immunocompromised
- **Stool tests:** Culture, ova & parasites, C. difficile toxin (if indicated)

**Management:**

**Rehydration (Critical):**
- **Oral rehydration solution** (ORS) - if able to tolerate orally
- **IV fluids** (if severe dehydration, unable to tolerate oral)
- **Target:** Urine output normal, no orthostatic symptoms

**Symptomatic:**
- **Loperamide** 4 mg initially, then 2 mg after each loose stool (max 16 mg/day)
- **Avoid** if bloody diarrhea, high fever, suspected infection (increases risk of complications)

**Antibiotics (if indicated):**
- **Traveler's diarrhea:** Azithromycin 1 g single dose (or 500 mg daily for 3 days)
- **C. difficile:** Oral vancomycin 125 mg QID for 10 days
- **Giardia:** Metronidazole 2 g daily for 3 days

**Chronic Diarrhea (> 30 days):**

**Etiology:**
- **Functional:** IBS-D (most common)
- **Inflammatory:** IBD (Crohn's, UC)
- **Malabsorptive:** Coeliac disease, lactase deficiency, pancreatic insufficiency
- **Infectious:** Parasites (Giardia, Cryptosporidium)
- **Medication-induced:** Laxatives, PPIs, metformin, antibiotics
- **Endocrine:** Hyperthyroidism, diabetes (autonomic neuropathy)
- **Neoplastic:** Colon cancer, carcinoid syndrome

**Evaluation:**
- **Fecal calprotectin** (distinguish IBD vs. functional)
- **Celiac serology** (tTG IgA)
- **TSH** (exclude hyperthyroidism)
- **Colonoscopy** (if age > 50, red flags, or uncertain diagnosis)

**Sources:** NICE CG84, BMJ Best Practice 2024"""

        return DomainQueryResult(
            domain_name="gastroenterology",
            answer=answer,
            confidence=0.87,
            metadata={
                "specialty": "gastroenterology",
                "focus": "diarrhea",
                "sources": ["NICE CG84", "BMJ Best Practice 2024"]
            }
        )

    def _handle_constipation(self, query: str, context: dict) -> DomainQueryResult:
        """Handle constipation queries"""
        answer = """**Constipation Assessment**

**Definition:**
- **Infrequent bowel movements** (< 3 per week)
- **Hard, lumpy stools**, straining, incomplete evacuation
- **Chronic:** Symptoms > 3 months

**Red Flags (Urgent Referral):**
- **Rectal bleeding** (unexplained)
- **Weight loss** (unintentional)
- **Family history** of colon/ovarian cancer
- **Change in bowel habits** (> 6 weeks, age > 60)
- **Anemia** (unexplained)
- **Abdominal mass**, **rectal mass**
- **New onset constipation** (age > 50)

**Common Causes:**
- **Primary (Functional):** Inadequate fiber, dehydration, inactivity
- **Secondary:** Medications (opioids, calcium channel blockers, iron), hypothyroidism, hypercalcemia, IBS-C, pelvic floor dysfunction

**Management:**

**First-line:**
- **Increase fiber** (20-30 g/day): Fruits, vegetables, whole grains
- **Adequate fluids** (2-3 L/day)
- **Regular exercise** (30 min daily)
- **Bowel routine:** Same time each day (after breakfast, gastrocolic reflex)

**Laxatives (Stepwise Approach):**

**Osmotic Laxatives:**
- **Polyethylene glycol** 17 g daily (adjust to effect)
- **Lactulose** 15-30 mL BD (can cause bloating)
- **Mechanism:** Draw water into bowel, soften stool

**Stimulant Laxatives:**
- **Senna** 2-4 tablets at night (onset 8-12 hours)
- **Bisacodyl** 5-10 mg at night or PR (onset 6-12 hours)
- **Mechanism:** Stimulate colonic motility
- **Use:** If osmotic laxatives inadequate

**Stool Softener:**
- **Docusate** 100 mg BD (limited evidence as monotherapy)

**Rectal Route (if oral ineffective):**
- **Phosphate enema** (PR)
- **Bisacodyl suppository** (PR)

**Chronic Constipation Management:**
- **Linaclotide** 290 mcg daily (IBS-C, chronic constipation)
- **Plecanatide** 3 mg daily
- **Lubiprostone** 8 mcg BID

**Pelvic Floor Dysfunction:**
- **Biofeedback therapy** (first-line)
- **Anorectal manometry** (diagnosis)

**Sources:** NICE CG99, BMJ Best Practice 2024"""

        return DomainQueryResult(
            domain_name="gastroenterology",
            answer=answer,
            confidence=0.86,
            metadata={
                "specialty": "gastroenterology",
                "focus": "constipation",
                "sources": ["NICE CG99", "BMJ Best Practice 2024"]
            }
        )

    def _interpret_endoscopy(self, query: str, context: dict) -> DomainQueryResult:
        """Interpret endoscopy findings"""
        answer = """**Endoscopy Report Interpretation**

**Common Upper GI Endoscopy Findings:**

**Reflux Esophagitis:**
- **Los Angeles Classification:**
  - **Grade A:** One/more mucosal breaks < 5 mm (confined to mucosal folds)
  - **Grade B:** One/more mucosal breaks > 5 mm (confined to mucosal folds)
  - **Grade C:** Mucosal breaks continuous between tops of 2+ mucosal folds
  - **Grade D:** Mucosal breaks involving ≥ 75% of esophageal circumference

**Barrett's Esophagus:**
- **Salmon-colored mucosa** in distal esophagus
- **Biopsy:** Intestinal metaplasia (goblet cells)
- **Management:** PPI, surveillance endoscopy every 2-3 years

**Peptic Ulcer:**
- **Gastric ulcer:** Biopsy required (exclude malignancy)
- **Duodenal ulcer:** Biopsy NOT routinely required
- **Forrest Classification:** Bleeding risk (Ia = spurting, highest risk)

**H. pylori:**
- **CLOtest:** Rapid urease test (biopsy)
- **Positive:** Eradication therapy required

**Gastritis:**
- **Erythema** (redness, inflammation)
- **Erosive gastritis** (small mucosal breaks)
- **H. pylori gastritis:** Chronic active gastritis

**Cancer:**
- **Mass, ulcer, narrowing** (biopsy mandatory)
- **Early:** Confined to mucosa/submucosa (curable with surgery)
- **Advanced:** Deep invasion, metastatic (palliative)

**Common Lower GI Endoscopy (Colonoscopy) Findings:**

**Diverticulosis:**
- **Multiple sac-like protrusions** (colon wall)
- **Common:** Sigmoid colon (age-related)
- **Management:** High-fiber diet, avoid nuts/seeds if symptomatic

**Polyps:**
- **Hyperplastic:** Benign, no cancer risk (small, distal)
- **Adenomatous:** Premalignant (remove, surveillance)
  - **Tubular adenoma:** Low risk
  - **Villous adenoma:** High risk
  - **Serrated adenoma:** Intermediate risk
- **Size:** < 1 cm (low risk), > 1 cm (high risk)
- **Number:** 1-2 (low risk), ≥ 3 (high risk)
- **Surveillance:** Based on risk (1-10 years)

**Colorectal Cancer:**
- **Mass, ulcer, narrowing** (biopsy mandatory)
- **Early:** Confined to mucosa/submucosa (curable with surgery)
- **Advanced:** Deep invasion, metastatic (palliative)

**Inflammatory Bowel Disease:**
- **Ulcerative Colitis:** Continuous inflammation, friability, ulceration, pseudopolyps (distal to proximal)
- **Crohn's Disease:** Aphthous ulcers, cobblestoning, skip lesions, strictures

**Angiodysplasia:**
- **Dilated, tortuous blood vessels** (bleeding risk)
- **Common:** Right colon, elderly
- **Treatment:** Endoscopic therapy (APC, clips)

**Hemorrhoids:**
- **Internal:** Above dentate line (not painful, bleeding)
- **External:** Below dentate line (painful, thrombosis)
- **Grades:** I-IV (IV = prolapsed, manual reduction required)

**Normal Findings:**
- **No pathology** (functional disorder, IBS)
- **Small biopsy:** Microscopic colitis (if chronic diarrhea)

**Sources:** British Society of Gastroenterology 2024, NICE 2024"""

        return DomainQueryResult(
            domain_name="gastroenterology",
            answer=answer,
            confidence=0.88,
            metadata={
                "specialty": "gastroenterology_procedures",
                "focus": "endoscopy_interpretation",
                "sources": ["BSG 2024", "NICE 2024"]
            }
        )

    def _handle_general_gastro(self, query: str, context: dict) -> DomainQueryResult:
        """General gastroenterology information"""
        answer = """**Gastroenterology Overview**

**GI System:**
- **Esophagus** (swallowing, reflux)
- **Stomach** (peptic ulcer, gastritis)
- **Small bowel** (coeliac, Crohn's)
- **Large bowel** (UC, diverticulosis, cancer)
- **Liver** (hepatitis, cirrhosis)
- **Pancreas** (pancreatitis)
- **Biliary** (gallstones)

**Common GI Conditions:**

**Upper GI:**
- **GORD/GERD:** Heartburn, reflux
- **Peptic ulcer:** H. pylori, NSAIDs
- **Gastritis:** Inflammation of stomach lining

**Lower GI:**
- **IBS:** Functional disorder (bloating, altered bowel habits)
- **IBD:** Inflammatory (Crohn's, UC)
- **Diverticulosis:** Age-related (complications: diverticulitis, bleeding)

**Liver:**
- **NAFLD/NASH:** Fatty liver (obesity, diabetes)
- **Alcoholic liver disease:** Cirrhosis
- **Viral hepatitis:** B, C (blood-borne)

**Pancreas:**
- **Acute pancreatitis:** Gallstones, alcohol
- **Chronic pancreatitis:** Pain, malabsorption

**When to Refer Urgently (2-week wait):**
- Unintentional weight loss
- Rectal bleeding (age > 50, or change in bowel habits)
- Iron deficiency anemia
- Dysphagia, odynophagia
- Abdominal mass, palpable gallbladder + jaundice

**Sources:** NICE guidelines, British Society of Gastroenterology"""

        return DomainQueryResult(
            domain_name="gastroenterology",
            answer=answer,
            confidence=0.85,
            metadata={
                "specialty": "gastroenterology",
                "focus": "general_information",
                "sources": ["NICE", "BSG"]
            }
        )

def create_gastroenterology_domain():
    """Factory function to create gastroenterology domain instance"""
    return GastroenterologyDomain()
