"""
General Surgery Domain for GPDISC

Comprehensive general surgery consultation covering:
- Acute abdominal emergencies (appendicitis, cholecystitis, bowel obstruction, perforated viscus)
- Upper gastrointestinal surgery (gastric, duodenal, bariatric)
- Colorectal surgery (colon, rectum, anus)
- Breast surgery (benign and malignant)
- Hernia surgery (inguinal, femoral, umbilical, incisional)
- Thyroid and parathyroid surgery
- Postoperative complications (wound infection, anastomotic leak, ileus)

Evidence-based guidelines:
- NICE NGxx guidelines
- Association of Surgeons of Great Britain and Ireland (ASGBI)
- American College of Surgeons (ACS)
"""

from typing import Dict, Any, List
from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult
import logging

logger = logging.getLogger(__name__)


class GeneralSurgeryDomain(BaseDomainModule):
    """
    General Surgery domain for comprehensive surgical consultation
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="general_surgery",
            version="1.0.0",
            dependencies=[],
            description="Comprehensive general surgery: acute abdomen, upper GI, colorectal, breast, hernia, endocrine surgery",
            keywords=[
                "general surgery", "acute abdomen", "abdominal pain", "surgical emergency",
                "appendicitis", "appendix", "mcburney's point", "rlq pain",
                "cholecystitis", "gallbladder", "biliary colic", "jaundice",
                "bowel obstruction", "intestinal obstruction", "volvulus", "hernia obstruction",
                "perforated viscus", "perforated ulcer", "peritonitis", "septic abdomen",
                "diverticulitis", "sigmoid volvulus", "colitis", "inflammatory bowel disease",
                "breast lump", "breast cancer", "mastectomy", "lumpectomy", "fibroadenoma",
                "hernia", "inguinal hernia", "femoral hernia", "umbilical hernia", "incisional hernia",
                "thyroid", "thyroid nodule", "goitre", "thyroidectomy", "parathyroid",
                "postoperative", "wound infection", "anastomotic leak", "ileus"
            ],
            capabilities=[
                "acute_abdomen_assessment",
                "appendicitis_diagnosis",
                "cholecystitis_management",
                "bowel_obstruction_management",
                "breast_disease_evaluation",
                "hernia_assessment",
                "thyroid_nodule_evaluation",
                "postoperative_complication_management"
            ]
        )

    def process_query(self, query: str, context: Dict[str, Any] = None) -> DomainQueryResult:
        """
        Process general surgery query with emergency detection
        """
        query_lower = query.lower()

        # SURGICAL EMERGENCIES - HIGHEST PRIORITY

        # Perforated viscus
        if any(term in query_lower for term in ["perforated viscus", "perforated ulcer", "perforated bowel",
                                                   "peritonitis", "septic abdomen", "acute abdomen rigid"]):
            return self._handle_perforated_viscus(query, context)

        # Complete bowel obstruction
        if any(term in query_lower for term in ["bowel obstruction", "intestinal obstruction", "complete obstruction",
                                                   "volvulus", "sigmoid volvulus", "caecal volvulus"]):
            return self._handle_bowel_obstruction(query, context)

        # Appendicitis
        if any(term in query_lower for term in ["appendicitis", "appendix", "mcburney's point",
                                                   "rlq pain", "right lower quadrant pain"]):
            return self._handle_appendicitis(query, context)

        # Cholecystitis
        if any(term in query_lower for term in ["cholecystitis", "gallbladder", "biliary colic",
                                                   "gallstones", "choledocholithiasis", "jaundice"]):
            return self._handle_cholecystitis(query, context)

        # Diverticulitis
        if any(term in query_lower for term in ["diverticulitis", "diverticular disease", "sigmoid diverticulitis",
                                                   "left iliac fossa pain", "llq pain"]):
            return self._handle_diverticulitis(query, context)

        # BREAST SURGERY

        if any(term in query_lower for term in ["breast lump", "breast mass", "breast cancer",
                                                   "mastectomy", "lumpectomy", "fibroadenoma",
                                                   "breast pain", "nipple discharge"]):
            return self._handle_breast_disease(query, context)

        # HERNIA

        if any(term in query_lower for term in ["hernia", "inguinal hernia", "femoral hernia",
                                                   "umbilical hernia", "incisional hernia",
                                                   "groin lump", "bulge"]):
            return self._handle_hernia(query, context)

        # THYROID

        if any(term in query_lower for term in ["thyroid", "thyroid nodule", "goitre", "thyroidectomy",
                                                   "parathyroid", "hyperparathyroidism", "calcium",
                                                   "neck lump"]):
            return self._handle_thyroid(query, context)

        # POSTOPERATIVE COMPLICATIONS

        if any(term in query_lower for term in ["wound infection", "surgical site infection", "ssi",
                                                   "anastomotic leak", "ileus", "postoperative ileus",
                                                   "abdominal sepsis", "surgical complication"]):
            return self._handle_postoperative_complications(query, context)

        # GENERAL SURGERY
        return self._handle_general_surgery(query, context)

    def _handle_perforated_viscus(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle perforated viscus"""
        return DomainQueryResult(
            domain_name="general_surgery",
            answer="""**PERFORATED VISCUS - SURGICAL EMERGENCY**

**IMMEDIATE ACTION:**
- **URGENT surgical referral** (within hours)
- **Resuscitate** (IV fluids, antibiotics, analgesia)
- **NOT for conservative management** (surgery required)

**CAUSES:**
- **Perforated peptic ulcer** (most common) - duodenum > stomach
- **Perforated appendix** (appendicitis complication)
- **Perforated diverticulum** (diverticulitis complication)
- **Perforated colon cancer** (obstruction + perforation)
- **Iatrogenic** (endoscopic, surgical complication)

**CLINICAL FEATURES:**
- **Sudden onset severe abdominal pain**
- **Board-like abdomen** (rigidity)
- **Absent bowel sounds**
- **Fever, tachycardia**
- **Patient lies still** (unlike peritonitis from pancreatitis - writhes)
- **History:** peptic ulcer disease, appendicitis, diverticulitis, colon cancer

**INVESTIGATIONS:**

**Blood tests:**
- **FBC** (leukocytosis, anaemia)
- **CRP** (marked elevation)
- **U&E** (dehydration, renal impairment)
- **Group and save** (cross-match 4-6 units)
- **Arterial blood gas** (metabolic acidosis)

**Imaging:**
- **Erect CXR** (free air under diaphragm - upright)
- **CT abdomen** (localise perforation, identify cause)

**IMMEDIATE MANAGEMENT:**

**1. Resuscitation:**
- **IV fluids:** Hartmann's or 0.9% NaCl (1-2 L rapid bolus, then 150-250 mL/hr)
- **Analgesia:** (Opioids - cautious, masks abdominal signs) - **NYSBID** (No NSAIDs)
- **Anti-emetics:** (Metoclopramide 10 mg IV/IM, Ondansetron 4-8 mg IV)
- **Antibiotics:** (immediate - before incision)
   - **Ceftriaxone 2 g IV** + **Metronidazole 500 mg IV**
   - **Or:** Co-amoxiclav 1.2 g IV + **Gentamicin 1.5 mg/kg IV**
- **Nasogastric tube:** (decompress stomach, reduce contamination)

**2. Surgical intervention:**
- **Laparotomy** (midline incision)
- **Find perforation**
- **Definitive surgery:** (see below)

**DEFINITIVE SURGERY:**

**Perforated duodenal ulcer:**
- **Simple closure** (primary repair) - omental patch (Graham patch)
- **If large perforation:** (distal gastrectomy - rare)
- **Vagotomy:** (highly selective truncal vagotomy)
- **Postoperative:** (H. pylori eradication, PPI)

**Perforated gastric ulcer:**
- **Simple closure** (if small, viable)
- **Wedge resection** (if large,怀疑 malignancy)
- **Gastrectomy** (if large,怀疑 cancer, complication)

**Perforated appendix:**
- **Appendicectomy** (remove appendix)
- **Washout** (peritoneal washout with warm saline)
- **Diverting ileostomy:** (if faecal peritonitis, rare)

**Perforated sigmoid colon:**
- **Hartmann's procedure:** (segmental resection, end colostomy, rectal stump)
   - **Reversal:** (colostomy closure, anastomosis - 3-6 months later)
- **Primary anastomosis:** (if faecal contamination minimal, patient stable, no comorbidities)
- **Subtotal colectomy:** (if total colonic diverticulosis, Hirschsprung's)

**POSTOPERATIVE CARE:**

**HDU/ITU admission:** (for monitoring)
- **Observations:** (BP, HR, RR, temp, urine output)
- **Monitoring:** (abdominal girth, wound drain, NG tube output)
- **Analgesia:** (PCA - Morphine)
- **Antibiotics:** (continue 5 days)
- **Nutrition:** (keep NBM, then gradually introduce fluids)

**COMPLICATIONS:**
- **Wound infection:** (10-20%)
- **Intra-abdominal abscess:** (5-10%)
- **Anastomotic leak:** (1-5% - catastrophic)
- **Ileus:** (postoperative ileus - common)
- **Sepsis:** (if delayed treatment)
- **Multi-organ failure:** (if delayed treatment, severe sepsis)

**PROGNOSIS:**
- **Mortality:** (5-30% - higher if delayed treatment, elderly, comorbidities)
- **Morbidity:** (30-50% - complications)

**Sources:** NICE CG184, ASGBI Guidelines, ESC Guidelines 2016"""
        )

    def _handle_bowel_obstruction(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle bowel obstruction"""
        return DomainQueryResult(
            domain_name="general_surgery",
            answer="""**BOWEL OBSTRUCTION - SURGICAL EMERGENCY**

**DEFINITION:**
- **Mechanical or functional blockage** of intestinal lumen
- **Can be partial or complete**
- **Can be simple or strangulated** (vascular compromise - surgical emergency)

**CAUSES:**

**Small bowel (75%):**
- **Adhesions** (post-surgical - most common)
- **Hernia** (incisional, inguinal, femoral - strangulation risk)
- **Malignancy** (small bowel tumour, metastasis)
- **Volvulus** (sigmoid > caecal - twisting of mesentery)
- **Intussusception** (pediatric - ileocaecal)

**Large bowel (25%):**
- **Colorectal cancer** (most common in adults)
- **Diverticular stricture**
- **Volvulus** (sigmoid, caecal)
- **Hirschsprung's disease** (congenital aganglionosis)
- **Fecal impaction**

**CLINICAL FEATURES:**

**Symptoms:**
- **Abdominal pain** (colicky - comes and goes)
- **Vomiting** (bilious, then faeculent if complete)
- **Absolute constipation** (complete obstruction) or **diarrhoea** (partial obstruction - "overflow")
- **Abdominal distension**
- **Failure to pass flatus**

**Signs:**
- **Abdominal distension**
- **Tender abdomen**
- **Visible peristalsis** (if thin)
- **Hyperactive bowel sounds** (early) → **absent bowel sounds** (late)
- **Signs of strangulation:** (red flags - see below)

**RED FLAGS (STRANGULATION - SURGICAL EMERGENCY):**
- **Severe, constant pain** (not colicky)
- **Fever, tachycardia** (signs of ischaemia, sepsis)
- **Rebound tenderness** (peritonitis)
- **Leucocytosis** (inflammatory markers)
- **Metabolic acidosis** (ischaemia)
- **Raised lactate** (>2 mmol/L)

**INVESTIGATIONS:**

**Blood tests:**
- **FBC** (leukocytosis, anaemia)
- **U&E** (dehydration, renal impairment)
- **CRP** (inflammatory markers)
- **Lactate** (ischaemia)
- **Group and save** (if surgery likely)

**Imaging:**
- **CT abdomen** (gold standard - localise obstruction, identify cause, transition point, strangulation)
- **AXR** (supine and erect - dilated loops of small bowel, air-fluid levels, no gas in rectum)
- **CT contrast** (oral or water-soluble contrast if partial obstruction)

**MANAGEMENT:**

**INITIAL:**
- **NBM** (nil by mouth)
- **IV fluids:** (Hartmann's or 0.9% NaCl - correct dehydration, electrolytes)
- **NG tube:** (decompress stomach, reduce vomiting, prevent aspiration)
- **Urinary catheter:** (monitor urine output)
- **Analgesia:** (avoid NSAIDs/morphine - masks signs, causes ileus)

**DEFINITIVE TREATMENT:**

**Adhesiolysis (adhesions):**
- **Laparoscopic** or open adhesiolysis
- **Resection:** (if bowel gangrenous, non-viable)

**Hernia repair:**
- **Emergency hernia repair**
- **Bowel resection:** (if gangrenous)

**Small bowel resection:**
- **Indications:** (malignancy, ischemia, gangrene)
- **Anastomosis:** (primary or protected - loop ileostomy)
- **Stoma:** (protect anastomosis - temporary loop ileostomy)

**Large bowel obstruction:**

**Left-sided (sigmoid, descending colon):**
- **Obstructing resection:** (Hartmann's procedure - segmental resection, end colostomy, rectal stump)
- **Primary anastomosis:** (on-table washout, no faecal contamination, patient stable)
- **Stent:** (colonic stent - palliative, bridging to surgery)

**Right-sided (caecum, ascending colon):**
- **Right hemicolectomy:** (primary anastomosis ileocolic)
- **Stoma:** (ileostomy - if emergency, patient unstable)

**Sigmoid volvulus:**
- **Endoscopic detorsion:** (sigmoidoscope, insufflate, reduce volvulus)
- **Sigmoid colectomy:** (if recurrent, gangrenous)
- **Stoma:** (if perforated, gangrenous)

**Caecal volvulus:**
- **Right hemicolectomy:** (primary anastomosis)
- **Stoma:** (if gangrenous, patient unstable)

**NON-OPERATIVE MANAGEMENT:**
- **Dissolve obstruction:** (Gastrografin enema - partial obstruction, no strangulation)
- **Endoscopic stenting:** (colonic stent - malignant obstruction - palliative)
- **Intestinal decompression tube:** (long tube - palliative)

**POSTOPERATIVE CARE:**
- **HDU:** (monitoring)
- **Observations:** (BP, HR, RR, temp, urine output)
- **NG tube:** (until flatus passed)
- **IV fluids:** (until tolerating oral fluids)
- **Gradual reintroduction of fluids:** (once flatus passed, bowel sounds return)
- **Analgesia:** (PCA - reduce ileus)
- **Thrombo-prophylaxis:** (LMWH)

**COMPLICATIONS:**
- **Bowel ischaemia/gangrene:** (anastomotic leak, sepsis, multi-organ failure)
- **Anastomotic leak:** (1-5% - catastrophic)
- **Wound infection:** (5-10%)
- **Ileus:** (postoperative ileus - common)
- **Sepsis:** (if perforation, gangrene)
- **Recurrence:** (adhesions - 30-50%)

**PROGNOSIS:**
- **Mortality:** (5-15% - higher if delayed treatment, strangulation, elderly, comorbidities)
- **Strangulation:** (if not treated within 6 hours - gangrene, perforation, sepsis, death)

**Sources:** NICE CG182, ASGBI Guidelines, ESC Guidelines 2020"""
        )

    def _handle_appendicitis(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle appendicitis"""
        return DomainQueryResult(
            domain_name="general_surgery",
            answer="""**APPENDICITIS**

**DEFINITION:**
- **Inflammation of appendix** (most common surgical emergency)
- **Incidence:** 7-12% lifetime risk
- **Peak incidence:** adolescence (10-20 years)

**PATHOLOGY:**
- **Obstruction of appendiceal lumen** (fecalith, lymphoid hyperplasia)
- **Bacterial overgrowth** (E. coli, Bacteroides)
- **Ischaemia** → **necrosis** → **perforation**

**CLINICAL FEATURES:**

**Symptoms:**
- **Abdominal pain** (periumbilical → RLQ migration - classic)
- **Anorexia** (present in 90%)
- **Nausea, vomiting** (present in 75%)
- **Low-grade fever** (<38.5°C)

**Signs:**
- **RLQ tenderness** (McBurney's point - 1/3 distance from umbilicus to ASIS)
- **Rebound tenderness** (blumberg sign)
- **Rovsing's sign** (LLQ pain on palpation of RLQ)
- **Psoas sign** (pain on extension of hip - retroperitoneal appendix)
- **Obturator sign** (pain on internal rotation of hip - pelvic appendix)

**ATYPICAL PRESENTATION:**
- **Pelvic appendix:** (suprapubic pain, urinary frequency, diarrhoea)
- **Retrocaecal appendix:** (flank pain, back pain)
- **Long appendix:** (RLQ, or right upper quadrant)

**DIFFERENTIAL DIAGNOSIS:**
- **Mesenteric adenitis** (usually younger children, URTI prodrome)
- **Gastroenteritis** (diarrhoea predominant)
- **Ovarian pathology** (cyst, torsion, PID)
- **Ectopic pregnancy** (always rule out in women of childbearing age)
- **Crohn's disease** (terminal ileitis)

**INVESTIGATIONS:**

**Blood tests:**
- **FBC** (leukocytosis 10-20×10⁹/L, neutrophilia)
- **CRP** (elevated >10 mg/L)
- **U&E** (dehydration)

**Imaging:**
- **Ultrasound** (first-line in children, young adults, pregnant women)
   - **Non-compressible, blind-ending, tubular structure** >6 mm diameter
   - **Appendicolith** (shadowing, posterior acoustic shadowing)
   - **Peri-appendiceal fat stranding** (inflammation)
- **CT abdomen** (adults, equivocal ultrasound)
   - **Appendiceal diameter** (>6 mm), wall thickening (>3 mm)
   - **Periappendiceal fat stranding**
   - **Appendicolith**
   - **Abscess** (perforated appendix with walled-off abscess)

**URGENT APPENDICECTOMY:**

**Indications:**
- **Confirmed appendicitis** (imaging or clinical diagnosis)
- **High clinical suspicion** (do not delay for imaging if classic presentation)

**Laparoscopic vs. Open:**
- **Laparoscopic** (gold standard - 3 ports, camera, grasper, stapler/dissector)
   - **Advantages:** (shorter recovery, less pain, smaller scar, lower infection rate)
   - **Contraindications:** (previous extensive abdominal surgery, late pregnancy, contraindication to pneumoperitoneum)
- **Open** (if laparoscopic not possible, or if conversion required)
   - **Conversion:** (5-10% - usually due to adhesions, inflammation, bleeding)

**ANTIBIOTICS:**
- **Pre-operative:** (within 1 hour of skin incision)
   - **Cefuroxime 1.5 g IV** + **Metronidazole 500 mg IV**
   - **Or:** Co-amoxiclav 2.2 g IV
- **Post-operative:** (continue 3-5 days, or stop after 24 hours if uncomplicated appendicitis)

**COMPLICATED APPENDICITIS:**

**Perforated appendix with generalised peritonitis:**
- **Urgent appendicectomy**
- **Peritoneal washout** (warm saline)
- **Antibiotics:** (continue 5-7 days)

**Appendiceal mass/phlegmon:**
- **Conservative management** (IV antibiotics, NBM, analgesia)
- **Interval appendicectomy:** (6-12 weeks later)

**Appendiceal abscess:**
- **CT-guided drainage** (if accessible)
- **Interval appendicectomy:** (6-12 weeks later)

**POSTOPERATIVE CARE:**
- **Day case:** (uncomplicated appendicitis - discharge same day)
- **Analgesia:** (regular paracetamol ± NSAID, weak opioid if needed)
- **Early mobilisation**
- **Diet:** (gradual reintroduction as tolerated)

**COMPLICATIONS:**
- **Wound infection:** (5-10%)
- **Intra-abdominal abscess:** (1-5%)
- **Ileus:** (postoperative ileus - common)
- **Appendix stump leak:** (rare - catastrophic)
- **Injury to adjacent structures:** (ureter, iliac vessels, bowel)

**PROGNOSIS:**
- **Mortality:** (<0.1% uncomplicated, <1% perforated)
- **Return to normal activities:** (1-2 weeks)
- **Recurrence:** (stump appendicitis - rare if appendiceal base divided)

**Sources:** NICE CG190, ASGBI Guidelines 2022"""
        )

    def _handle_cholecystitis(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle cholecystitis"""
        return DomainQueryResult(
            domain_name="general_surgery",
            answer="""**CHOLECYSTITIS**

**DEFINITION:**
- **Inflammation of gallbladder** (usually due to gallstones)
- **Incidence:** (more common in women, "fat, female, forty, fertile")
- **Types:** acute, chronic, acalculous

**PATHOLOGY:**
- **Cystic duct obstruction** (gallstone, calculus)
- **Biliary stasis** (fasting, parenteral nutrition)
- **Bacterial infection** (E. coli, Klebsiella, Enterococcus)
- **Chemical irritation** (pancreatic enzymes reflux)

**CLINICAL FEATURES:**

**Symptoms:**
- **RUQ pain** (severe, constant, may radiate to right shoulder/scapula)
- **Nausea, vomiting** (common)
- **Fever** (low-grade in acute, high-grade if empyema)
- **Jaundice** (15% - Mirizzi syndrome, choledocholithiasis)

**Signs:**
- **RUQ tenderness**
- **Murphy's sign** (inspiratory arrest on deep palpation in RUQ)
- **Guarding, rebound** (localised peritonitis)
- **Gallbladder palpable** (rare - 10-30%)
- **Jaundice** (if common bile duct obstruction)

**DIFFERENTIAL DIAGNOSIS:**
- **Biliary colic:** (pain resolves, no fever, no Murphy's sign)
- **Peptic ulcer disease:** (epigastric pain, RUQ pain)
- **Pancreatitis:** (epigastric pain, radiates through to back, amylase elevated)
- **Pneumonia:** (lower lobe pneumonia)
- **Myocardial ischaemia:** (atypical presentation)

**INVESTIGATIONS:**

**Blood tests:**
- **FBC** (leukocytosis 12-15×10⁹/L)
- **CRP** (elevated >100 mg/L)
- **LFTs:** (raised bilirubin, ALP, GGT, transaminases)
- **Amylase/Lipase:** (exclude pancreatitis, raised in 30-40% of cholecystitis)

**Imaging:**
- **Ultrasound** (first-line)
   - **Gallstones** (echogenic foci with acoustic shadowing)
   - **Gallbladder wall thickening** (>4 mm)
   - **Pericholecystic fluid** (localised inflammation)
   - **Sonographic Murphy's sign** (maximal tenderness over gallbladder)
   - **Common bile duct diameter** (>6 mm = dilated)
- **CT abdomen** (if ultrasound equivocal, complications suspected)
   - **Gallbladder wall thickening, pericholecystic fluid, gas (emphysematous cholecystitis)

**MANAGEMENT:**

**ACUTE CALCULOUS CHOLECYSTITIS:**

**Conservative:**
- **NBM** (nil by mouth)
- **IV fluids** (Hartmann's or 0.9% NaCl)
- **Analgesia:** (NSAIDs - Diclofenac 75 mg IM/IV PRN, opioids if severe)
- **Antibiotics:** (same regimen as surgery - see below)

**Definitive:**
- **Laparoscopic cholecystectomy** (gold standard - urgent, within 24-72 hours)
   - **Early surgery:** (reduces recurrence, complications, hospital stay)
   - **Contraindications:** (severe comorbidities, unfit for surgery)
- **Open cholecystectomy:** (if laparoscopic not possible - previous surgery, adhesions, bleeding diathesis)

**ANTIBIOTICS:**
- **Cefuroxime 1.5 g IV** + **Metronidazole 500 mg IV** (TDS)
- **Or:** Co-amoxiclav 1.2 g IV TDS
- **Duration:** (5 days if perforated/gangrenous, 1 dose pre-op if uncomplicated cholecystectomy)
- **Indications:** (gangrenous, perforated, empyema, high-risk patient)

**CHOLEDOCHOLITHIASIS (Common Bile Duct Stones):**
- **Jaundice** (obstructive jaundice)
- **Cholangitis** (Charcot's triad - fever, jaundice, RUQ pain; Reynolds' pentad - plus shock, confusion)
- **Pancreatitis** (gallstone pancreatitis)
- **Investigation:**
   - **MRCP** (gold standard - non-invasive)
   - **ERCP** (therapeutic - sphincterotomy, stone extraction)
   - **Intraoperative cholangiogram** (if concern, no pre-op MRCP)

**ACUTE ACALCULOUS CHOLECYSTITIS:**
- **No gallstones** (10% of acute cholecystitis)
- **Risk factors:** (critical illness, trauma, burns, fasting, parenteral nutrition, HIV)
- **Diagnosis of exclusion:** (ultrasound shows thickened gallbladder, no stones)
- **Management:** (broad-spectrum antibiotics, percutaneous cholecystostomy if fails medical management)
- **Cholecystectomy:** (once recovered, 6-8 weeks later)

**GANGRENOUS CHOLECYSTITIS:**
- **Severe inflammation**, necrosis of gallbladder wall
- **Risk factors:** (diabetes, elderly, delayed presentation)
- **Signs:** (high fever, sepsis, RUQ mass, crepitus)
- **Management:** (urgent cholecystectomy, open approach, antibiotics)
- **Complications:** (abscess, perforation, sepsis, multi-organ failure)

**EMPYEMA:** (pus in gallbladder)
- **Signs:** (high fever, RUQ mass, sepsis)
- **Management:** (urgent cholecystectomy, antibiotics)

**PERFORATION:** (rare - 10%)
- **Signs:** (generalised peritonitis, sepsis, shock)
- **Management:** (urgent cholecystectomy, peritoneal washout, antibiotics)

**POSTOPERATIVE CARE:**
- **Day case:** (laparoscopic cholecystectomy - discharge same day)
- **Analgesia:** (paracetamol, NSAID)
- **Diet:** (low fat initially, then gradual reintroduction)
- **Complications:** (bile leak, bile duct injury, bleeding, retained stones)

**BILE DUCT INJURY:**
- **Incidence:** (0.3-0.5%)
- **Types:** (cystic duct leak, common bile duct injury)
- **Management:** (ERCP stent, hepaticojejunostomy)
- **Prevention:** (critical view of safety - identify cystic duct, common bile duct)

**Sources:** NICE CG188, ASGBI Guidelines 2021"""
        )

    def _handle_diverticulitis(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle diverticulitis"""
        return DomainQueryResult(
            domain_name="general_surgery",
            answer="""**DIVERTICULITIS**

**DEFINITION:**
- **Inflammation of colonic diverticula** (pouches in colon wall)
- **Incidence:** (increases with age - 60% by age 80)
- **Location:** (sigmoid colon most common - 95%)

**PATHOLOGY:**
- **Diverticulosis** (pouches present)
- **Microperforation** of diverticulum → inflammation
- **Obstruction** of diverticulum neck → bacterial overgrowth

**CLINICAL FEATURES:**

**Symptoms:**
- **LLQ pain** (left iliac fossa)
- **Fever** (low-grade)
- **Change in bowel habit** (diarrhoea, constipation)
- **Rectal bleeding** (haematochezia - 25%)

**Signs:**
- **LLQ tenderness**
- **Abdominal distension**
- **Left lower quadrant mass** (inflammatory phlegmon)

**HINCHEY CLASSIFICATION:**

**Stage I:** (pericolic inflammation/phlegmon - abscess confined to mesocolon)
**Stage II:** (pelvic abscess)
**Stage III:** (generalised peritonitis)
**Stage IV:** (fecal peritonitis)

**INVESTIGATIONS:**

**Blood tests:**
- **FBC** (leukocytosis)
- **CRP** (elevated)
- **U&E** (dehydration, renal impairment)

**Imaging:**
- **CT abdomen** (gold standard)
   - **Diverticulosis** (multiple diverticula)
   - **Bowel wall thickening** (>4 mm)
   - **Fat stranding** (inflammation)
   - **Abscess** (phlegmon, collection)
   - **Free air** (perforation)
- **Colonoscopy** (after acute episode resolved - 6-8 weeks)
   - **Indications:** (rule out colorectal cancer, assess extent of diverticulosis)

**MANAGEMENT:**

**UNCOMPLICATED DIVERTICULITIS:**

**Mild (Hinchey I):**
- **Outpatient management**
- **Antibiotics:** (Co-amoxiclav 625 mg TDS PO for 7 days)
- **Diet:** (gradually reintroduce as tolerated)
- **Review:** (if worsening)

**Moderate (Hinchey I-II):**
- **Hospital admission**
- **NBM** (if severe)
- **IV fluids:** (Hartmann's or 0-balance)
- **IV antibiotics:** (Co-amoxiclav 1.2 g TDS + **Gentamicin** 5 mg/kg OD)
- **Analgesia:** (paracetamol, avoid opioids)
- **Diet:** (tolerate oral fluids, then low residue diet)

**COMPLICATED DIVERTICULITIS (Hinchey II-IV):**

**Abscess (Hinchey II):**
- **IV antibiotics** (as above)
- **CT-guided drainage** (if accessible)
- **Surgical drainage** (if percutaneous drainage fails)

**Generalised peritonitis (Hinchey III):**
- **Emergency surgery**
- **Hartmann's procedure:** (sigmoid colectomy, end colostomy, rectal stump)
   - **Advantages:** (avoids anastomosis in inflamed, contaminated field)
   - **Reversal:** (colostomy closure 3-6 months later)
- **Primary anastomosis:** (on-table washout, no faecal contamination, patient stable)
   - **Protecting ileostomy:** (loop ileostomy)

**Fecal peritonitis (Hinchey IV):**
- **Emergency surgery**
- **Hartmann's procedure**
- **On-table washout**
- **Second-look laparotomy** (24-48 hours later - DAIR - Damage control, Assessment, Investigation, Resuscitation, Reconstruct)

**CHRONIC DIVERTICULITIS:**
- **Recurrent diverticulitis** (≥2 episodes)
- **Complications:** (stricture, fistula, obstruction)
- **Management:** (elective sigmoid colectomy with primary anastomosis)

**PREVENTION:**
- **High-fibre diet** (30 g/day)
- **Adequate hydration** (2-3 L/day)
- **Avoid:** (seeds, nuts - if diverticulosis)

**POSTOPERATIVE CARE:**
- **HDU:** (monitoring)
- **Observations:** (BP, HR, RR, temp, urine output)
- **NG tube:** (if ileus)
- **IV fluids:** (until tolerating oral fluids)
- **Gradual reintroduction of diet:** (low residue → normal)

**COMPLICATIONS:**
- **Anastomotic leak:** (3-10% - catastrophic)
- **Wound infection:** (5-10%)
- **Ileus:** (postoperative ileus - common)
- **Sepsis:** (if perforation, delayed treatment)
- **Colostomy complications:** (prolapse, retraction, stenosis)
- **Recurrent diverticulitis:** (5-10%)

**PROGNOSIS:**
- **Mortality:** (1-2% uncomplicated, 5-15% perforated)
- **Recurrence:** (30% after conservative treatment, 5% after sigmoid colectomy)

**Sources:** NICE CG147, ASGBI Guidelines 2021"""
        )

    def _handle_breast_disease(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle breast disease"""
        return DomainQueryResult(
            domain_name="general_surgery",
            answer="""**BREAST DISEASE**

**BREAST LUMP:**

**CAUSES:**
- **Benign:** (fibroadenoma, breast cyst, hamartoma, fat necrosis)
- **Malignant:** (breast cancer - 1 in 8 women lifetime risk)

**ASSESSMENT:**

**TRIPLE ASSESSMENT:**
1. **Clinical examination:** (inspection, palpation - characteristics of lump)
2. **Imaging:** (ultrasound <30 years, ultrasound + mammogram ≥30 years)
3. **Tissue diagnosis:** (core needle biopsy, FNA - fine needle aspiration)

**BENIGN CONDITIONS:**

**Fibroadenoma:**
- **Most common benign breast tumour**
- **Peak incidence:** (20-30 years)
- **Management:** (observation if <2-3 cm, excision if >3 cm or patient request)
- **Recurrence:** (if incompletely excised)

**Breast cyst:**
- **Fluid-filled sac**
- **Management:** (aspiration if symptomatic, confirm collapse)
- **If blood-stained:** (send for cytology - exclude malignancy)

**Fibrocystic change:**
- **Benign** (not a disease - physiological)
- **Management:** (reassurance, support bra, analgesia if needed)

**BREAST CANCER:**

**Risk factors:**
- **Increasing age**
- **Family history:** (BRCA1/2 mutations)
- **Reproductive:** (early menarche, late menopause, nulliparity, late first pregnancy)
- **Hormone replacement therapy:** (combined HRT)
- **Alcohol:** (moderate intake increases risk)

**Clinical features:**
- **Lump** (painless, hard, irregular)
- **Skin changes:** (dimpling, peau d'orange)
- **Nipple changes:** (inversion, discharge, retraction, eczema)
- **Lymphadenopathy:** (axillary nodes - palpable)

**Investigations:**
- **Mammogram:** (BI-RADS 1-5)
- **Ultrasound:** (solid vs. cystic)
- **Core biopsy:** (diagnosis, histology, grade, ER/PR/HER2)
- **MRI:** (if dense breasts, extent of disease)

**Management:**
- **Multidisciplinary team:** (surgeon, oncologist, radiologist, pathologist, breast nurse)
- **Surgery:** (lumpectomy vs. mastectomy + sentinel lymph node biopsy)
- **Axillary surgery:** (sentinel lymph node biopsy → axillary dissection if positive)
- **Oncoplastic surgery:** (immediate reconstruction, good cosmetic outcome)
- **Reconstruction:** (implant, LD flap, DIEP flap, TRAM flap)
- **Radiotherapy:** (post-mastectomy or breast-conserving surgery)
- **Chemotherapy:** (adjuvant if >1 node positive, high-grade)
- **Hormonal therapy:** (tamoxifen, aromatase inhibitors - ER/PR positive)
- **Targeted therapy:** (trastuzumab, pertuzumab - HER2 positive)

**FIBROADENOMA:**

**Features:**
- **Mobile:** (moves freely within breast)
- **Firm/rubbery:** (smooth, rubbery)
- **Well-circumscribed**
- **Age:** 15-35 years

**Investigation:**
- **Ultrasound:** (well-circumscribed, solid, 1-5 cm)
- **Core biopsy:** (confirm diagnosis)
- **Excision:** (if symptomatic, >3 cm, patient request, patient preference)

**BREAST PAIN:**

**Cyclical mastalgia:**
- **Hormonal** (worse premenstrually, bilateral, diffuse)
- **Management:** (reassurance, supportive bra, Evening Primrose Oil, Danazol)
- **Exclude:** (pregnancy, breast cancer)

**Non-cyclical mastalgia:**
- **Localised pain**
- **Investigate:** (ultrasound, mammogram)
- **Management:** (treat cause - cyst aspiration, excision)

**NIPPLE DISCHARGE:**
- **Physiological:** (pregnancy, lactation, menopausal)
- **Pathological:** (intraduct papilloma, duct ectasia, cancer)
- **Colour:**
   - **Green/yellow:** (benign - duct ectasia, intraductal papilloma)
   - **Blood-stained:** (suspicious - exclude cancer)
- **Investigation:** (mammogram, cytology, ultrasound, ductography)
- **Management:** (treat cause - microdochectomy, excision)

**GYNAECOMASTIA:**
- **Benign breast enlargement** in men
- **Causes:** (pubertal, steroid use, liver disease, testicular failure, drugs - spironolactone)
- **Management:** (exclude underlying cause, reassure, excision if severe, persistent)

**Sources:** NICE CG164, ABS Guidelines 2023"""
        )

    def _handle_hernia(self, query: str, context: Dict[str, Any]) -> DomainQueryuncture:
        """Handle hernia"""
        return DomainQueryResult(
            domain_name="general_surgery",
            answer="""**HERNIA**

**DEFINITION:**
- **Abnormal protrusion** of viscus through fascial defect

**TYPES:**

**Groin Hernias (80%):**
- **Inguinal:** (direct - medial to inferior epigastric vessels; indirect - through deep inguinal ring)
- **Femoral:** (below inguinal ligament, lateral to pubic tubercle)

**Abdominal Wall Hernias (20%):**
- **Umbilical:** (congenital or acquired)
- **Incisional:** (previous surgical incision)
- **Epigastric:** (through linea alba)
- **Spigelian:** (semilunar line - rare)

**Other:**
- **Parastomal:** (around stoma site)
- **Obturator:** (obturator foramen - rare)
- **Lumbar:** (through posterior abdominal wall - rare)

**INGUINAL HERNIA:**

**Direct:**
- **Pathology:** (transversalis fascia defect in Hesselbach's triangle)
- **Medial to inferior epigastric vessels** (important intraoperative landmark)
- **Less common** (20% of inguinal hernias)

**Indirect:**
- **Pathology:** (patent processus vaginalis - congenital sac)
- **Through deep inguinal ring** (into inguinal canal)
- **More common** (80% of inguinal hernias)
- **More common** in men, right side

**CLINICAL FEATURES:**
- **Groin lump** (reducible with gentle pressure)
- **Pain** (dragging sensation, aggravated by activity)
- **Swelling** (worse with standing, coughing)
- **Reducible:** (can push back in)

**STRANGULATION:**
- **IRREVERSIBLE** (cannot reduce - surgical emergency)
- **SIGNS:**
   - **Severe pain**
   - **Tender, red, tense**
   - **Nausea, vomiting**
   - **Obstipation** (if bowel trapped)
   - **Ischaemia** (gangrene within 6 hours)

**INVESTIGATIONS:**
- **Clinical diagnosis** (usually sufficient)
- **Ultrasound** (if diagnostic uncertainty, groin mass, recurrence)

**MANAGEMENT:**

**Watchful waiting:** (all patients)
- **Indications:** (asymptomatic/minimal symptoms, patient preference)
- **Contraindications:** (strangulation, obstructed hernia, symptomatic patient)

**Elective repair:** (open or laparoscopic)
- **Indications:** (symptomatic, patient request)
- **Timing:** (day case, within 2-3 months of diagnosis)
- **Techniques:**
   - **Open:** (Lichtenstein tension-free mesh repair - gold standard)
   - **Laparoscopic:** (TEP, TAPP - quicker recovery, more expensive)
   - **Suture repair:** (pediatric, small hernias)

**Emergency repair:** (strangulated, obstructed)
- **Urgent surgery** (within hours)
- **Open approach** (to assess bowel viability)
- **Resection:** (if gangrenous)

**FEMORAL HERNIA:**
- **Below inguinal ligament** (lateral to pubic tubercle)
- **More common in** (elderly women)
- **Higher risk of strangulation** (requires urgent repair)
- **Surgery:** (laparoscopic or open - mesh repair)

**UMBILICAL HERNIA:**
- **Congenital:** (paediatric - close spontaneously by age 2)
- **Adult:** (acquired - midline defect)
- **Management:** (excision + primary repair or mesh repair)

**INCISIONAL HERNIA:**
- **Previous surgical incision** (midline, laparoscopic port)
- **Risk factors:** (wound infection, obesity, chronic cough, steroids)
- **Prevention:** (careful fascial closure, avoid infection)
- **Management:** (mesh repair)

**RECURRENCE:**
- **1-3%** (after primary repair)
- **Higher risk:** (infection, smoking, COPD, collagen disorders)
- **Management:** (mesh repair, redo surgery)

**Sources:** NICE NG168, EHS Guidelines 2018"""
        )

    def _handle_thyroid(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle thyroid"""
        return DomainQueryResult(
            domain_name="general_surgery",
            answer="""**THYROID DISORDERS**

**THYROID NODULE:**

**ASSESSMENT:**

**Risk factors for malignancy:**
- **Male** (higher risk than female)
- **Age** (<20 or >60 years)
- **Family history** (thyroid cancer)
- **Radiation exposure**
- **Compressive symptoms** (dysphonia, dysphagia)

**INVESTIGATIONS:**

**TSH** (Thyroid Stimulating Hormone):
- **Normal:** (0.4-4.0 mU/L)
- **Suppressed:** (<0.1 mU/L) → suggests autonomous nodule (toxic adenoma)
- **Elevated:** (>10 mU/L) → suggests hypothyroidism (colloid nodule)

**Ultrasound:**
- **Solid vs. cystic**
- **Hypoechoic vs. hyperechoic**
- **Microcalcifications** (suspicious for malignancy)
- **Size** (>1 cm = investigate)

**U-RADS (Ultrasound Risk Stratification):**
- **U1:** (benign - no follow-up)
- **U2:** (benign - follow-up in 2 years)
- **U3:** (indeterminate - FNA or follow-up in 1 year)
- **U4:** (suspicious - FNA)
- **U5:** (highly suspicious - FNA)

**FNA (Fine Needle Aspiration):**
- **Indication:** (U4 or U5, or if patient prefers)
- **Cytology:** (benign, suspicious, malignant, non-diagnostic)
- **Sensitivity:** (85-95%)
- **Specificity:** (50-100%)

**MALIGNANCY RISK (THYROID NODULE):**
- **<5%:** (most nodules are benign)
- **5-15%:** (if suspicious features on ultrasound)
- **>50%:** (if highly suspicious features on ultrasound)

**MANAGEMENT:**

**Benign nodule:**
- **Observation:** (repeat ultrasound in 1-2 years)
- **Aspirate:** (if cystic, symptomatic)

**Suspicious nodule:**
- **FNA:** (cytology)
- **Hemithyroidectomy:** (lobectomy) if cytology suspicious or indeterminate

**TOXIC ADENOMA:**
- **Autonomous nodule** (secretes thyroid hormone independent of TSH)
- **Suppressed TSH**
- **Clinical features:** (symptoms of thyrotoxicosis - palpitations, weight loss, anxiety)
- **Investigations:** (suppressed TSH, elevated T3/T4, uptake scan)
- **Management:** (surgery - lobectomy or thyroidectomy)

**MULTINODULAR GOITRE:**
- **Enlarged thyroid** with multiple nodules
- **Investigations:** (TSH, ultrasound, FNA if suspicious features)
- **Management:** (observation, hemithyroidectomy if compressive symptoms, suspicious features)

**HASHIMOTO THYROIDITIS:**
- **Autoimmune thyroiditis**
- **Hypothyroid** (elevated TSH, low T4)
- **Antibodies:** (TPO antibodies - anti-thyroid peroxidase)
- **Management:** (thyroxine replacement)

**GRAVES' DISEASE:**
- **Autoimmune hyperthyroidism**
- **Clinical features:** (thyrotoxicosis, ophthalmopathy, dermopathy)
- **Investigations:** (suppressed TSH, elevated T3/T4, TSH receptor antibodies)
- **Management:** (antithyroid drugs - Carbimazole, PTU; radioiodine; thyroidectomy; beta-blockers)

**THYROID CANCER:**
- **Papillary** (most common - 80%)
- **Follicular** (15%)
- **Medullary** (rare - calcitonin-producing)
- **Anaplastic** (rare - very aggressive)
- **Management:** (total thyroidectomy + central compartment neck dissection ± lateral neck dissection, radioiodine ablation, TSH suppression)

**PARATHYROID DISORDERS:**

**HYPERPARATHYROIDISM:**
- **Primary:** (adenoma - 80%)
- **Secondary:** (renal failure, vitamin D deficiency)
- **Clinical features:** (stones, bones, groans, moans, fatigue)
- **Biochemistry:** (elevated calcium, low/normal phosphate, elevated PTH)
- **Investigations:** (serum calcium, phosphate, PTH, ultrasound, sestamibi scan)
- **Management:** (parathyroidectomy - focused or bilateral)

**HYPOPARATHYROIDISM:**
- **Causes:** (post-thyroidectomy, autoimmune, congenital, magnesium deficiency)
- **Clinical features:** (tetany, cramps, paraesthesia, seizures)
- **Biochemistry:** (low calcium, high phosphate, low PTH)
- **Management:** (calcium + vitamin D, magnesium, calcitriol)

**Sources:** NICE NG145, BTA Guidelines 2018"""
        )

    def _handle_postoperative_complications(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle postoperative complications"""
        return DomainQueryResult(
            domain_name="general_surgery",
            answer="""**POSTOPERATIVE COMPLICATIONS**

**SURGICAL SITE INFECTION (SSI):**

**Risk factors:**
- **Patient:** (diabetes, smoking, obesity, immunosuppression, malnutrition)
- **Surgery:** (emergency, dirty/infected, prolonged, contaminated)
- **Postoperative:** (prolonged ICU stay, blood transfusion)

**Prevention:**
- **Prophylactic antibiotics:** (single dose within 60 minutes of incision)
- **Preoperative shower:** (antiseptic soap)
- **Hair removal:** (do not shave - clip if necessary)
- **Skin preparation:** (alcohol/chlorhexidine - let dry)
- **Drapes:** (sterile)
- **Wound protection:** (dressings)

**Diagnosis:**
- **Erythema** (cellulitis)
- **Purulent discharge**
- **Wound dehiscence**
- **Culture:** (wound swab)

**Treatment:**
- **Cellulitis:** (antibiotics - Co-amoxiclav 500/125 mg TDS PO)
- **Abscess:** (incision and drainage)
- **Dehiscence:** (packing, secondary closure or healing by secondary intention)
- **Severe:** (return to theatre for washout)

**ANASTOMOTIC LEAK:**

**INCIDENCE:**
- **Esophagogastrostomy:** (5-20%)
- **Pancreaticojejunostomy:** (5-10%)
- **Small bowel:** (1-5%)
- **Large bowel:** (1-5%)
- **Rectal:** (5-15%)

**Risk factors:**
- **Ischaemia:** (poor blood supply, anastomotic tension)
- **Technical:** (poor technique, inadequate inversion)
- **Patient:** (diabetes, malnutrition, steroids, smoking, hypotension)
- **Emergency surgery:** (perforated viscus, obstruction)
- **Contamination:** (faecal peritonitis)

**Diagnosis:**
- **Clinical suspicion:** (sepsis, abdominal pain, fever, tachycardia)
- **CT scan:** (extraluminal air, abscess)
- **Water-soluble contrast:** (enema, swallow study)

**Management:**
- **Surgical re-exploration** (urgent - septic, peritonitis)
- **Source control:** (repair anastomosis if recent, diversion if friable)
- **Defunctioning stoma:** (end ileostomy, colostomy)
- **ICU admission:** (monitoring, inotropes)
- **Antibiotics:** (broad-spectrum)

**ILEUS:**

**Definition:**
- **Transient paralysis** of bowel (no mechanical obstruction)
- **Incidence:** (common after abdominal surgery)

**Causes:**
- **Neurogenic:** (sympathetic overdrive, pain, opioids)
- **Inflammatory:** (manipulation, peritonitis)
- **Metabolic:** (electrolyte abnormalities: hypokalaemia, hyponatraemia)
- **Drugs:** (opioids, anticholinergics, calcium channel blockers)

**Diagnosis:**
- **Clinical:** (distended abdomen, absent bowel sounds, flatus, stool)
- **CT scan:** (exclude mechanical obstruction)

**Management:**
- **Supportive:** (NBM until resolves, NG tube if vomiting)
- **Optimise:** (fluid and electrolytes, correct hypokalaemia)
- **Mobilise:** (ambulate, chair)
- **Analgesia:** (reduce opioids, use NSAIDs/regional anaesthesia)
- **Prokinetics:** (Metoclopramide 10 mg IV TDS, Erythromycin 250 mg IV TDS)
- **Magnesium Sulfate:** (1-2 g IV - if refractory)

**POSTOPERATIVE BLEEDING:**

**Early bleeding:**
- **Technical:** (inadequate haemostasis, slipped ligature)
- **Coagulopathy:** (anticoagulation, thrombocytopenia)
- **Signs:** (drains bleeding, abdominal distension, hypotension, tachycardia)

**Late bleeding:**
- **Slipped ligature** (day 5-10)
- **Ulceration:** (anastomotic ulcer)
- **Infection:** (abscess eroding vessel)

**Management:**
- **Observation:** (if minor bleeding, patient stable)
- **Fluid resuscitation:** (IV fluids, blood transfusion)
- **Correct coagulopathy:** (vitamin K, FFP, platelets)
- **Return to theatre:** (if massive or ongoing bleeding, patient unstable)

**DEEP VEIN THROMBOSIS (DVT):**

**Risk factors:**
- **Virchow's triad:** (venous stasis, endothelial injury, hypercoagulability)
- **Surgery:** (abdominal, pelvic, orthopaedic)
- **Patient:** (obesity, cancer, OCP, pregnancy, previous DVT)
- **Immobility:** (prolonged bed rest)

**Prevention:**
- **Mechanical:** (graduated compression stockings, intermittent pneumatic compression)
- **Chemical:** (LMWH - prophylactic dose)
- **Early mobilisation**

**Diagnosis:**
- **Clinical:** (unilateral leg swelling, pain, redness, warmth, Homan's sign)
- **Doppler ultrasound:** (compression ultrasound - gold standard)
- **D-dimer:** (if DVT unlikely, negative rules out)

**Treatment:**
- **LMWH:** (therapeutic dose - Tinzaparin, Dalteparin, Enoxaparin)
- **Duration:** (3 months for provoked DVT, at least 3-6 months for unprovoked DVT)
- **DOACs:** (Rivaroxaban, Apixaban - if provoked, extended treatment)

**Sources:** NICE NG174, NICE NG182"""
        )

    def _handle_general_surgery(self, query: str, context: Dict[str, Any]) -> DomainQueryResult:
        """Handle general surgery query"""
        return DomainQueryResult(
            domain_name="general_surgery",
            answer="""**GENERAL SURGERY - General Consultation**

General surgery covers a wide range of surgical conditions.

**ACUTE ABDOMEN:**
- **Appendicitis**
- **Cholecystitis**
- **Bowel obstruction**
- **Perforated viscus**
- **Diverticulitis**

**UPPER GI SURGERY:**
- **Gastroduodenal ulcer**
- **Gastric cancer**
- **Bariatric surgery** (sleeve gastrectomy, Roux-en-Y gastric bypass)
- **Anti-reflux surgery** (fundoplication)

**COLORECTAL SURGERY:**
- **Colorectal cancer**
- **Inflammatory bowel disease** (Crohn's disease, ulcerative colitis)
- **Diverticular disease**
- **Colostomy/ileostomy**

**BREAST SURGERY:**
- **Breast cancer** (lumpectomy, mastectomy, reconstruction)
- **Benign disease** (fibroadenoma, cysts, mastalgia)
- **Nipple discharge**

**HERNIA SURGERY:**
- **Inguinal hernia** (most common)
- **Femoral hernia** (high strangulation risk)
- **Umbilical hernia**
- **Incisional hernia**

**ENDOCRINE SURGERY:**
- **Thyroid surgery** (lobectomy, thyroidectomy, parathyroidectomy)
- **Parathyroid surgery** (adenoma, hyperplasia)

**MINIMAL ACCESS SURGERY:**
- **Laparoscopic** (keyhole surgery - most common operations)
- **Robotic** (emerging technology)

**POSTOPERATIVE CARE:**
- **Wound care**
- **Pain management**
- **Early mobilisation**
- **Thromboprophylaxis**

**Sources:** NICE Guidelines, ASGBI Guidelines"""
        )


def create_general_surgery_domain():
    """Factory function to create general surgery domain"""
    return GeneralSurgeryDomain()
