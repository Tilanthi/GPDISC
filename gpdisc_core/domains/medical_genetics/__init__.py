"""
GPDISC Medical Genetics Domain

Medical genetics domain covering genetic counseling, inherited disorders,
prenatal genetic testing, pharmacogenomics, cancer genetics, pediatric
and adult-onset genetic conditions.

Evidence Base: ACMG, BSGM, NICE Guidelines, GeneReviews, NIH Genetics
"""

from gpdisc_core.domains import BaseDomainModule, DomainConfig, DomainQueryResult
from typing import Optional, Dict, Any, List
import re


class MedicalGeneticsDomain(BaseDomainModule):
    """
    Medical Genetics Domain - Genetic consultation and counseling

    Covers:
    - Genetic counseling and risk assessment
    - Mendelian inheritance patterns
    - Chromosomal abnormalities
    - Mitochondrial disorders
    - Pharmacogenomics
    - Prenatal genetic testing
    - Cancer genetics (BRCA, Lynch syndrome, etc.)
    - Pediatric genetic disorders
    - Adult-onset genetic conditions
    - Carrier screening
    - Preimplantation genetic diagnosis (PGD/PGS)
    """

    def get_default_config(self) -> DomainConfig:
        return DomainConfig(
            domain_name="medical_genetics",
            version="1.0.0",
            dependencies=[],
            description="Medical genetics, genetic counseling, inherited disorders, prenatal genetic testing, pharmacogenomics, cancer genetics",
            keywords=[
                # General genetics terms
                "genetics", "genetic", "inherited", "inheritance", "hereditary", "familial",
                "gene", "dna", "chromosome", "mutation", "variant", "polymorphism",

                # Genetic counseling
                "genetic counseling", "genetic counselor", "genetic risk", "carrier",
                "carrier screening", "carrier test", "recessive", "dominant", "x-linked",

                # Mendelian disorders
                "cystic fibrosis", "cf", "huntington", "huntington disease", "hd",
                "muscular dystrophy", "dmd", "dca", "sickle cell", "thalassemia",
                "hemophilia", "fragile x", "tay sachs", "gaucher",

                # Chromosomal disorders
                "down syndrome", "trisomy 21", "trisomy 18", "edwards syndrome",
                "trisomy 13", "patau syndrome", "turner syndrome", "klinefelter",
                "chromosomal abnormality", "aneuploidy", "translocation", "deletion",
                "duplication", "microdeletion", "microduplication",

                # Mitochondrial disorders
                "mitochondrial", "mtdna", "merrf", "melas", "leigh syndrome",
                "maternal inheritance",

                # Prenatal testing
                "prenatal testing", "nipt", "amniocentesis", "chorionic villus",
                "cvs", "nuchal translucency", "quad screen", "triple test",

                # Cancer genetics
                "brca", "brca1", "brca2", "lynch syndrome", "hnpcc",
                "familial adenomatous polyposis", "fap", "hereditary cancer",
                "cancer genetics", "cancer predisposition", "oncogene",

                # Pharmacogenomics
                "pharmacogenomics", "pharmacogenetics", "drug metabolism",
                "cyp450", "cyp2d6", "cyp2c19", "tpmt", "dpd", "ugt1a1",
                "drug response", "adverse drug reaction",

                # Pediatric genetics
                "pediatric genetics", "dysmorphology", "syndrome", "congenital",
                "developmental delay", "intellectual disability", "autism genetics",
                "genetic syndrome", "rare disease", "orphan disease",

                # Adult-onset disorders
                "adult-onset", "late-onset", "predictive testing", "presymptomatic",
                "genetic predisposition", "genetic susceptibility",

                # Reproductive genetics
                "preimplantation", "pgd", "pgs", "ivf genetics", "reproductive genetics",

                # Testing terminology
                "genetic testing", "genetic test", "gene panel", "whole exome",
                "whole genome", "exome sequencing", "genome sequencing", "sequencing",
                "microarray", "karyotype", "fish", "genetic screening",

                # Ethics and consent
                "genetic consent", "genetic ethics", "genetic discrimination",
                "genetic privacy", "genetic information", "direct to consumer",
                "23andme", "ancestry dna", "genetic ancestry"
            ],
            capabilities=[
                "genetic_counseling", "inheritance_risk_assessment", "carrier_screening",
                "prenatal_genetic_testing_guidance", "cancer_genetics_assessment",
                "pharmacogenomics_consultation", "pediatric_genetics_evaluation",
                "adult_onset_genetic_testing", "genetic_test_interpretation",
                "family_history_analysis", "variant_interpretation"
            ]
        )

    def process_query(self, query: str, context: dict = None) -> DomainQueryResult:
        """
        Process medical genetics queries with appropriate routing
        """
        query_lower = query.lower()

        # EMERGENCY: Urgent genetic findings requiring immediate action
        if any(term in query_lower for term in ["emergency", "urgent", "immediately needed"]):
            return self._handle_genetic_emergency(query, context)

        # Prenatal genetic testing
        if any(term in query_lower for term in [
            "prenatal", "nipt", "amniocentesis", "cvs", "chorionic villus",
            "nuchal", "trisomy", "down syndrome", "pregnant genetics"
        ]):
            return self._handle_prenatal_genetics_query(query, context)

        # Cancer genetics
        if any(term in query_lower for term in [
            "brca", "lynch", "fap", "cancer genetics", "hereditary cancer",
            "familial cancer", "cancer predisposition", "cancer gene"
        ]):
            return self._handle_cancer_genetics_query(query, context)

        # Pharmacogenomics
        if any(term in query_lower for term in [
            "pharmacogenomics", "pharmacogenetics", "drug metabolism",
            "cyp450", "cyp2d6", "cyp2c19", "tpmt", "drug response", "gene interaction"
        ]):
            return self._handle_pharmacogenomics_query(query, context)

        # Pediatric genetics / dysmorphology
        if any(term in query_lower for term in [
            "pediatric genetics", "dysmorphology", "syndrome", "congenital",
            "developmental delay", "intellectual disability", "autism genetics",
            "dysmorphic", "dysmorphology"
        ]):
            return self._handle_pediatric_genetics_query(query, context)

        # Mendelian disorders
        if any(term in query_lower for term in [
            "cystic fibrosis", "cf", "huntington", "muscular dystrophy",
            "sickle cell", "thalassemia", "hemophilia", "fragile x",
            "tay sachs", "gaucher", "recessive", "carrier"
        ]):
            return self._handle_mendelian_disorders_query(query, context)

        # Chromosomal disorders
        if any(term in query_lower for term in [
            "down syndrome", "trisomy", "turner", "klinefelter",
            "chromosomal abnormality", "aneuploidy", "translocation",
            "deletion", "duplication", "microdeletion", "karyotype"
        ]):
            return self._handle_chromosomal_disorders_query(query, context)

        # Mitochondrial disorders
        if any(term in query_lower for term in [
            "mitochondrial", "mtdna", "merrf", "melas", "leigh",
            "maternal inheritance"
        ]):
            return self._handle_mitochondrial_disorders_query(query, context)

        # Adult-onset/predictive testing
        if any(term in query_lower for term in [
            "predictive testing", "presymptomatic", "adult-onset",
            "late-onset", "genetic predisposition"
        ]):
            return self._handle_adult_onset_query(query, context)

        # Reproductive genetics (PGD/PGS)
        if any(term in query_lower for term in [
            "preimplantation", "pgd", "pgs", "ivf genetics"
        ]):
            return self._handle_reproductive_genetics_query(query, context)

        # Genetic test results interpretation
        if any(term in query_lower for term in [
            "genetic test result", "variant", "mutation", "polymorphism",
            "pathogenic", "benign", "vus", "variant of uncertain significance"
        ]):
            return self._handle_test_interpretation_query(query, context)

        # General genetic counseling
        else:
            return self._handle_general_genetics_query(query, context)

    def _handle_genetic_emergency(self, query: str, context: dict) -> DomainQueryResult:
        """
        Handle urgent genetic findings requiring immediate action

        Includes: critical prenatal findings, cancer predisposition requiring immediate surveillance
        """
        query_lower = query.lower()

        # Critical prenatal findings
        if any(term in query_lower for term in ["trisomy", "down syndrome", "cvs", "amniocentesis"]):
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "CRITICAL GENETICS FINDING - IMMEDIATE GENETICS REFERRAL REQUIRED\n\n"
                    "CRITICAL prenatal genetic findings require URGENT genetics specialist consultation:\n\n"
                    "1. IMMEDIATE ACTIONS:\n"
                    "   - Refer to clinical genetics service URGENTLY (same day/next day)\n"
                    "   - Inform patient of need for specialist review\n"
                    "   - Document all findings and communication clearly\n"
                    "   - Arrange genetic counselor support for patient\n\n"
                    "2. CRITICAL FINDINGS:\n"
                    "   - Trisomy 21 (Down syndrome)\n"
                    "   - Trisomy 18 (Edwards syndrome)\n"
                    "   - Trisomy 13 (Patau syndrome)\n"
                    "   - Sex chromosome aneuploidies\n"
                    "   - Significant microdeletions/duplications\n\n"
                    "3. DO NOT DELAY:\n"
                    "   - These findings require specialist genetic counseling\n"
                    "   - Patient needs detailed discussion of implications\n"
                    "   - Further testing may be required\n"
                    "   - Management planning needed\n\n"
                    "4. SUPPORT:\n"
                    "   - Provide written information\n"
                    "   - Offer psychological support\n"
                    "   - Contact patient support groups if appropriate\n\n"
                    "5. DOCUMENTATION:\n"
                    "   - Document all discussions\n"
                    "   - Record patient understanding\n"
                    "   - Note follow-up arrangements\n\n"
                    "URGENT REFERRAL to Clinical Genetics Department required.\n\n"
                    "Sources: NICE NG161, BSGM Prenatal Guidelines"
                ),
                confidence=0.95,
                metadata={
                    "urgency": "emergency",
                    "category": "critical_prenatal_finding",
                    "requires_immediate_referral": True,
                    "sources": ["NICE NG161", "BSGM Prenatal Guidelines", "ACMG Practice Guidelines"]
                }
            )

        # Cancer predisposition requiring immediate action
        elif any(term in query_lower for term in ["brca", "lynch", "cancer gene", "hereditary cancer"]):
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "URGENT: HEREDITARY CANCER PREDISPOSITION IDENTIFIED\n\n"
                    "URGENT referral to cancer genetics service required:\n\n"
                    "1. IMMEDIATE ACTIONS:\n"
                    "   - Refer to cancer genetics/familial cancer clinic URGENTLY\n"
                    "   - Document family history thoroughly (3-generation pedigree)\n"
                    "   - Do not start preventive interventions until genetics review\n\n"
                    "2. HIGH-RISK FINDINGS:\n"
                    "   - BRCA1/BRCA2 pathogenic variants\n"
                    "   - Lynch syndrome (MLH1, MSH2, MSH6, PMS2, EPCAM)\n"
                    "   - Other high-penetrance cancer genes\n\n"
                    "3. MANAGEMENT (until specialist review):\n"
                    "   - Inform patient of finding\n"
                    "   - Explain need for specialist assessment\n"
                    "   - Discuss implications for family members\n"
                    "   - Do not make decisions about surgery/medication yet\n\n"
                    "4. FAMILY IMPLICATIONS:\n"
                    "   - Result may have implications for relatives\n"
                    "   - Genetics team will coordinate cascade testing\n"
                    "   - Patient should inform family when appropriate\n\n"
                    "URGENT REFERRAL to Familial Cancer/Cancer Genetics Service required.\n\n"
                    "Sources: NICE NG164, NICE CG164, ESMO Guidelines"
                ),
                confidence=0.95,
                metadata={
                    "urgency": "urgent",
                    "category": "hereditary_cancer_risk",
                    "requires_immediate_referral": True,
                    "sources": ["NICE NG164", "NICE CG164", "ESMO Clinical Practice Guidelines"]
                }
            )

        else:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "URGENT GENETICS CONSULTATION REQUIRED\n\n"
                    "Urgent genetics referral recommended. Please provide specific details "
                    "about the genetic finding or test result for appropriate guidance.\n\n"
                    "URGENT referral to Clinical Genetics service required.\n\n"
                    "Sources: BSGM, ACMG Practice Guidelines"
                ),
                confidence=0.85,
                metadata={
                    "urgency": "urgent",
                    "category": "urgent_genetics_consultation",
                    "sources": ["BSGM Guidelines", "ACMG Practice Guidelines"]
                }
            )

    def _handle_prenatal_genetics_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle prenatal genetic testing queries"""
        query_lower = query.lower()

        # NIPT (Non-Invasive Prenatal Testing)
        if "nipt" in query_lower or "non-invasive prenatal" in query_lower:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "PRENATAL GENETICS: Non-Invasive Prenatal Testing (NIPT)\n\n"
                    "NIPT is a screening test for common chromosomal abnormalities:\n\n"
                    "1. WHAT NIPT TESTS FOR:\n"
                    "   - Trisomy 21 (Down syndrome) - detection rate ~99%\n"
                    "   - Trisomy 18 (Edwards syndrome) - detection rate ~97%\n"
                    "   - Trisomy 13 (Patau syndrome) - detection rate ~90%\n"
                    "   - Sex chromosome abnormalities (optional)\n"
                    "   - Some microdeletions (extended panels)\n\n"
                    "2. WHEN OFFERED:\n"
                    "   - From 10 weeks gestation\n"
                    "   - Can be done as first-line or contingent screening\n"
                    "   - Available to all pregnant women (NICE NG161)\n\n"
                    "3. HOW IT WORKS:\n"
                    "   - Maternal blood test\n"
                    "   - Analyzes cell-free fetal DNA in maternal plasma\n"
                    "   - No risk of miscarriage\n\n"
                    "4. INTERPRETATION:\n"
                    "   - HIGH RISK: Offer diagnostic testing (CVS/amniocentesis)\n"
                    "   - LOW RISK: No further testing required for these conditions\n"
                    "   - NO RESULT/FAILED: Repeat test or offer alternative screening\n\n"
                    "5. LIMITATIONS:\n"
                    "   - Screening test, not diagnostic\n"
                    "   - False positives and false negatives occur\n"
                    "   - Does not detect all genetic conditions\n"
                    "   - May be less reliable in obesity, multiple pregnancies\n\n"
                    "6. CONFIRMED TESTING REQUIRED:\n"
                    "   - Positive NIPT requires CVS or amniocentesis for confirmation\n"
                    "   - Do not make irreversible decisions based on NIPT alone\n\n"
                    "Discuss with Fetal Medicine/Clinical Genetics if positive result.\n\n"
                    "Sources: NICE NG161, BSGM, RCOG Green-top Guideline"
                ),
                confidence=0.95,
                metadata={
                    "category": "prenatal_screening",
                    "test_type": "nipt",
                    "sources": ["NICE NG161", "BSGM Guidelines", "RCOG Green-top Guideline"]
                }
            )

        # Amniocentesis
        elif "amniocentesis" in query_lower:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "PRENATAL GENETICS: Amniocentesis (Diagnostic Test)\n\n"
                    "Amniocentesis is a diagnostic test for chromosomal and genetic abnormalities:\n\n"
                    "1. PROCEDURE:\n"
                    "   - Typically performed at 15-20 weeks gestation\n"
                    "   - Ultrasound-guided needle aspiration of amniotic fluid\n"
                    "   - Outpatient procedure, takes 10-15 minutes\n\n"
                    "2. WHAT CAN BE TESTED:\n"
                    "   - Karyotype (chromosome analysis): T21, T18, T13, sex chromosome abnormalities\n"
                    "   - Chromosomal microarray (CMA): microdeletions/duplications\n"
                    "   - Specific genetic tests (if indicated): CF, SMA, etc.\n"
                    "   - Whole exome sequencing (in selected cases)\n\n"
                    "3. RESULTS:\n"
                    "   - Rapid aneuploidy (FISH/QF-PCR): 2-3 days for T21, T18, T13\n"
                    "   - Full karyotype: 10-14 days\n"
                    "   - Microarray: 1-2 weeks\n"
                    "   - Specific molecular tests: varies (days to weeks)\n\n"
                    "4. RISKS:\n"
                    "   - Miscarriage risk: ~0.1-0.3% (1 in 300-1000)\n"
                    "   - Amniotic fluid leakage: ~1-2%\n"
                    "   - Infection: <1%\n"
                    "   - Needle injury to fetus: rare\n\n"
                    "5. INDICATIONS:\n"
                    "   - Abnormal screening test (NIPT, combined test)\n"
                    "   - Abnormal ultrasound findings\n"
                    "   - Previous child with chromosomal abnormality\n"
                    "   - Parental balanced translocation\n"
                    "   - Known or suspected genetic condition\n\n"
                    "6. COUNSELING REQUIRED:\n"
                    "   - Discuss benefits, limitations, risks\n"
                    "   - Discuss what conditions are being tested for\n"
                    "   - Discuss implications of abnormal results\n"
                    "   - Written information should be provided\n\n"
                    "Refer to Fetal Medicine service for procedure and counseling.\n\n"
                    "Sources: NICE NG161, RCOG Green-top Guideline, BSGM"
                ),
                confidence=0.95,
                metadata={
                    "category": "prenatal_diagnostic",
                    "test_type": "amniocentesis",
                    "miscarriage_risk": "0.1-0.3%",
                    "sources": ["NICE NG161", "RCOG Green-top Guideline", "BSGM"]
                }
            )

        # CVS (Chorionic Villus Sampling)
        elif "cvs" in query_lower or "chorionic villus" in query_lower:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "PRENATAL GENETICS: Chorionic Villus Sampling (CVS)\n\n"
                    "CVS is a diagnostic test performed earlier than amniocentesis:\n\n"
                    "1. PROCEDURE:\n"
                    "   - Typically performed at 11-14 weeks gestation\n"
                    "   - Transcervical or transabdominal biopsy of chorionic villi\n"
                    "   - Ultrasound-guided, outpatient procedure\n\n"
                    "2. WHAT CAN BE TESTED:\n"
                    "   - Karyotype (chromosome analysis)\n"
                    "   - Chromosomal microarray (CMA)\n"
                    "   - Specific genetic tests (CF, SMA, etc.)\n"
                    "   - Whole exome sequencing (selected cases)\n\n"
                    "3. RESULTS:\n"
                    "   - Rapid aneuploidy: 2-3 days\n"
                    "   - Full karyotype: 10-14 days\n"
                    "   - Microarray: 1-2 weeks\n\n"
                    "4. ADVANTAGES:\n"
                    "   - Earlier diagnosis than amniocentesis\n"
                    "   - More time for decision-making\n"
                    "   - Earlier reassurance if normal\n\n"
                    "5. RISKS:\n"
                    "   - Miscarriage risk: ~0.5-1% (1 in 100-200)\n"
                    "   - Slightly higher risk than amniocentesis\n"
                    "   - Mosaicism (confined placental): ~1-2%\n"
                    "   - May require amniocentesis for clarification\n\n"
                    "6. INDICATIONS:\n"
                    "   - Abnormal first-trimester screening\n"
                    "   - Abtrasound abnormalities at 11-14 weeks\n"
                    "   - Previous child with chromosomal abnormality\n"
                    "   - Known parental translocation\n"
                    "   - Need for earlier diagnosis\n\n"
                    "7. COUNSELING REQUIRED:\n"
                    "   - Discuss higher miscarriage risk vs. amniocentesis\n"
                    "   - Discuss possibility of mosaicism\n"
                    "   - Discuss possibility of need for amniocentesis\n\n"
                    "Refer to Fetal Medicine service for CVS and counseling.\n\n"
                    "Sources: NICE NG161, RCOG Green-top Guideline, BSGM"
                ),
                confidence=0.95,
                metadata={
                    "category": "prenatal_diagnostic",
                    "test_type": "cvs",
                    "miscarriage_risk": "0.5-1%",
                    "sources": ["NICE NG161", "RCOG Green-top Guideline", "BSGM"]
                }
            )

        # Down syndrome / Trisomy 21
        elif any(term in query_lower for term in ["down syndrome", "trisomy 21", "trisomy21"]):
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "PRENATAL GENETICS: Down Syndrome (Trisomy 21)\n\n"
                    "Down syndrome is caused by an extra copy of chromosome 21:\n\n"
                    "1. TYPES:\n"
                    "   - Trisomy 21 (95%): Three copies of chromosome 21\n"
                    "   - Translocation (3-4%): Extra chromosome 21 attached to another chromosome\n"
                    "   - Mosaic (1-2%): Some cells have extra chromosome 21\n\n"
                    "2. DETECTION:\n"
                    "   - NIPT: Detection rate ~99%\n"
                    "   - Combined test (11-14 weeks): Detection rate ~85-90%\n"
                    "   - CVS/amniocentesis: Diagnostic confirmation\n\n"
                    "3. CLINICAL FEATURES:\n"
                    "   - Intellectual disability (mild to moderate)\n"
                    "   - Characteristic facial features\n"
                    "   - Hypotonia (low muscle tone) in infancy\n"
                    "   - Single palmar crease\n"
                    "   - Congenital heart defects (~40-50%)\n"
                    "   - Increased risk of leukemia, Alzheimer disease\n"
                    "   - Hypothyroidism, hearing loss, vision problems\n\n"
                    "4. LIFE EXPECTANCY:\n"
                    "   - Median life expectancy: ~60 years (improved with medical care)\n"
                    "   - Many adults live into their 60s and 70s\n\n"
                    "5. MANAGEMENT:\n"
                    "   - Early intervention programs\n"
                    "   - Special education support\n"
                    "   - Regular medical surveillance (cardiac, thyroid, hearing, vision)\n"
                    "   - Support services and organizations\n\n"
                    "6. RECURRENCE RISK:\n"
                    "   - General population: ~1 in 800\n"
                    "   - After one affected child: ~1 in 100 (if not translocation)\n"
                    "   - If parental translocation: varies (up to 10-15%)\n\n"
                    "7. GENETIC COUNSELING:\n"
                    "   - Offer karyotype to determine type\n"
                    "   - Parental studies if translocation suspected\n"
                    "   - Discuss prognosis and support available\n"
                    "   - Provide written information and support contacts\n\n"
                    "Refer to Clinical Genetics for detailed counseling and recurrence risk assessment.\n\n"
                    "Sources: NICE NG161, GeneReviews, Down Syndrome Medical Interest Group"
                ),
                confidence=0.95,
                metadata={
                    "category": "chromosomal_disorder",
                    "condition": "down_syndrome",
                    "sources": ["NICE NG161", "GeneReviews", "DSMIG UK Guidelines"]
                }
            )

        # General prenatal testing
        else:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "PRENATAL GENETIC TESTING\n\n"
                    "Prenatal genetic testing options include:\n\n"
                    "1. SCREENING TESTS (No miscarriage risk):\n"
                    "   - NIPT (from 10 weeks): T21, T18, T13, sex chromosome abnormalities\n"
                    "   - Combined test (11-14 weeks): NT scan + PAPP-A + beta-hCG\n"
                    "   - Quadruple test (14-20 weeks): Alternative if first trimester missed\n\n"
                    "2. DIAGNOSTIC TESTS (Small miscarriage risk):\n"
                    "   - CVS (11-14 weeks): Earlier diagnosis\n"
                    "   - Amniocentesis (15-20 weeks): Later but lower miscarriage risk\n\n"
                    "3. WHAT CAN BE TESTED:\n"
                    "   - Chromosomal abnormalities (T21, T18, T13, sex chromosomes)\n"
                    "   - Microdeletions/duplications (via CMA)\n"
                    "   - Specific single-gene disorders (if indicated)\n"
                    "   - Whole exome sequencing (selected cases)\n\n"
                    "4. WHO SHOULD BE OFFERED TESTING:\n"
                    "   - All women should be offered screening (NICE NG161)\n"
                    "   - Diagnostic testing offered if:\n"
                    "     * Abnormal screening result\n"
                    "     * Abnormal ultrasound findings\n"
                    "     * Previous child with genetic condition\n"
                    "     * Known or suspected familial condition\n\n"
                    "5. COUNSELING REQUIRED:\n"
                    "   - Discuss what conditions are being tested for\n"
                    "   - Discuss detection rates and limitations\n"
                    "   - Discuss implications of results\n"
                    "   - Allow informed choice\n\n"
                    "Refer to Fetal Medicine/Clinical Genetics for prenatal counseling.\n\n"
                    "Sources: NICE NG161, BSGM, RCOG"
                ),
                confidence=0.90,
                metadata={
                    "category": "prenatal_testing",
                    "sources": ["NICE NG161", "BSGM", "RCOG Green-top Guidelines"]
                }
            )

    def _handle_cancer_genetics_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle cancer genetics queries"""
        query_lower = query.lower()

        # BRCA1/BRCA2
        if "brca" in query_lower:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "CANCER GENETICS: BRCA1 and BRCA2 Pathogenic Variants\n\n"
                    "BRCA1/BRCA2 pathogenic variants confer high risk of breast, ovarian, and other cancers:\n\n"
                    "1. CANCER RISKS:\n"
                    "   BRCA1:\n"
                    "   - Breast cancer: 60-75% (lifetime risk)\n"
                    "   - Ovarian cancer: 40-60%\n"
                    "   - Fallopian tube cancer: Increased\n"
                    "   - Prostate cancer (men): Moderate increased risk\n"
                    "   - Pancreatic cancer: Slight increased risk\n\n"
                    "   BRCA2:\n"
                    "   - Breast cancer: 50-70%\n"
                    "   - Ovarian cancer: 10-30%\n"
                    "   - Prostate cancer (men): Increased risk (~20%)\n"
                    "   - Pancreatic cancer: Increased risk\n"
                    "   - Melanoma: Possible increased risk\n\n"
                    "2. MANAGEMENT OPTIONS:\n"
                    "   Breast cancer risk reduction:\n"
                    "   - Enhanced surveillance (annual MRI + mammogram)\n"
                    "   - Risk-reducing mastectomy (90-95% risk reduction)\n"
                    "   - Chemoprevention (tamoxifen, raloxifene)\n\n"
                    "   Ovarian cancer risk reduction:\n"
                    "   - Risk-reducing salpingo-oophorectomy (recommended 35-40 years for BRCA1, 40-45 for BRCA2)\n"
                    "   - Consideration of earlier surgery after completion of family\n"
                    "   - No proven effective screening for ovarian cancer\n\n"
                    "3. WHO SHOULD BE TESTED:\n"
                    "   - Breast cancer diagnosed <50 years\n"
                    "   - Triple-negative breast cancer <60 years\n"
                    "   - Male breast cancer\n"
                    "   - Ovarian cancer (any age)\n"
                    "   - Multiple family members with breast/ovarian cancer\n"
                    "   - Ashkenazi Jewish ancestry (higher carrier frequency)\n"
                    "   - Known BRCA variant in family\n\n"
                    "4. FAMILY IMPLICATIONS:\n"
                    "   - Autosomal dominant inheritance (50% to each child)\n"
                    "   - Cascade testing recommended for at-risk relatives\n"
                    "   - Both maternal and paternal family history important\n\n"
                    "5. GENETIC COUNSELING:\n"
                    "   - Pre-test and post-test counseling essential\n"
                    "   - Discuss implications for patient and family\n"
                    "   - Discuss insurance, employment, psychological implications\n"
                    "   - Discuss reproductive options (PGD)\n\n"
                    "URGENT REFERRAL to Cancer Genetics/Familial Cancer service required.\n\n"
                    "Sources: NICE NG164, NICE CG164, ESMO Guidelines"
                ),
                confidence=0.95,
                metadata={
                    "category": "cancer_genetics",
                    "condition": "brca",
                    "inheritance": "autosomal_dominant",
                    "sources": ["NICE NG164", "NICE CG164", "ESMO Clinical Practice Guidelines"]
                }
            )

        # Lynch Syndrome (HNPCC)
        elif any(term in query_lower for term in ["lynch", "hnpcc", "hereditary nonpolyposis"]):
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "CANCER GENETICS: Lynch Syndrome (Hereditary Non-Polyposis Colorectal Cancer)\n\n"
                    "Lynch syndrome is caused by pathogenic variants in DNA mismatch repair genes:\n\n"
                    "1. GENES INVOLVED:\n"
                    "   - MLH1 (most common)\n"
                    "   - MSH2\n"
                    "   - MSH6\n"
                    "   - PMS2\n"
                    "   - EPCAM deletion (affects MSH2 expression)\n\n"
                    "2. CANCER RISKS (lifetime):\n"
                    "   Colorectal cancer:\n"
                    "   - MLH1/MSH2: 40-80%\n"
                    "   - MSH6: 10-44%\n"
                    "   - PMS2: 15-20%\n\n"
                    "   Endometrial cancer (women):\n"
                    "   - MLH1/MSH2: 40-60%\n"
                    "   - MSH6: 16-71%\n"
                    "   - PMS2: 15-20%\n\n"
                    "   Other cancers (ovarian, gastric, urinary tract, brain, skin)\n\n"
                    "3. DIAGNOSIS:\n"
                    "   - Tumor testing (MSI or IHC) on colorectal/endometrial cancer\n"
                    "   - If abnormal: Germline genetic testing for Lynch syndrome\n"
                    "   - Universal testing of colorectal cancers now recommended\n\n"
                    "4. SURVEILLANCE:\n"
                    "   Colorectal:\n"
                    "   - Colonoscopy every 1-2 years starting age 25 (or 5 years before earliest case)\n"
                    "   - Consider aspirin chemoprevention (600mg daily for 2+ years)\n\n"
                    "   Endometrial/Ovarian (women):\n"
                    "   - Consider annual endometrial biopsy\n"
                    "   - Discuss risk-reducing hysterectomy/oophorectomy after childbearing\n"
                    "   - No proven effective screening for ovarian cancer\n\n"
                    "   Other:\n"
                    "   - Consider gastric surveillance (if family history)\n"
                    "   - Urinary tract surveillance (if MSH2)\n\n"
                    "5. WHO SHOULD BE TESTED:\n"
                    "   - Colorectal cancer <50 years\n"
                    "   - Endometrial cancer <50 years\n"
                    "   - Multiple Lynch-related cancers\n"
                    "   - Amsterdam or Bethesda criteria met\n"
                    "   - Abnormal tumor testing (MSI-H or dMMR)\n"
                    "   - Known Lynch syndrome in family\n\n"
                    "6. FAMILY IMPLICATIONS:\n"
                    "   - Autosomal dominant (50% to each child)\n"
                    "   - Cascade testing essential\n"
                    "   - Predictive testing available from age 18-25\n\n"
                    "URGENT REFERRAL to Cancer Genetics/Familial Cancer service required.\n\n"
                    "Sources: NICE DG27, BSG指南, ESMO Guidelines"
                ),
                confidence=0.95,
                metadata={
                    "category": "cancer_genetics",
                    "condition": "lynch_syndrome",
                    "inheritance": "autosomal_dominant",
                    "sources": ["NICE DG27", "British Society of Gastroenterology", "ESMO Guidelines"]
                }
            )

        # General cancer genetics
        else:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "CANCER GENETICS: Hereditary Cancer Predisposition\n\n"
                    "Hereditary cancer syndromes account for 5-10% of all cancers:\n\n"
                    "1. COMMON HEREDITARY CANCER SYNDROMES:\n"
                    "   - BRCA1/BRCA2: Breast, ovarian, prostate, pancreatic cancer\n"
                    "   - Lynch syndrome: Colorectal, endometrial, ovarian cancer\n"
                    "   - FAP: Familial adenomatous polyposis (colorectal cancer)\n"
                    "   - MEN: Multiple endocrine neoplasia\n"
                    "   - VHL: Von Hippel-Lindau (renal, CNS, pancreatic tumors)\n"
                    "   - Many other rare syndromes\n\n"
                    "2. RED FLAGS FOR HEREDITARY CANCER:\n"
                    "   - Cancer diagnosed at young age (<50 years)\n"
                    "   - Multiple primary cancers in same individual\n"
                    "   - Same cancer in multiple close relatives\n"
                    "   - Clustering of related cancers (breast/ovarian, colon/endometrial)\n"
                    "   - Rare cancers (medullary thyroid, adrenocortical carcinoma)\n"
                    "   - Bilateral cancers (bilateral breast cancer)\n"
                    "   - Multiple generations affected\n\n"
                    "3. GENETIC TESTING PROCESS:\n"
                    "   - Detailed family history (3-generation pedigree)\n"
                    "   - Risk assessment using validated models\n"
                    "   - Genetic counseling before testing\n"
                    "   - Targeted genetic testing or panel testing\n"
                    "   - Post-test counseling and management planning\n\n"
                    "4. MANAGEMENT PRINCIPLES:\n"
                    "   - Enhanced surveillance\n"
                    "   - Risk-reducing surgery\n"
                    "   - Chemoprevention\n"
                    "   - Lifestyle modification\n"
                    "   - Reproductive options (PGD)\n\n"
                    "5. FAMILY IMPLICATIONS:\n"
                    "   - Cascade testing for at-risk relatives\n"
                    "   - Predictive testing for asymptomatic relatives\n"
                    "   - Insurance and employment considerations\n\n"
                    "Refer to Cancer Genetics/Familial Cancer service for assessment.\n\n"
                    "Sources: NICE NG164, NICE CG164, ESMO Guidelines"
                ),
                confidence=0.90,
                metadata={
                    "category": "cancer_genetics",
                    "sources": ["NICE NG164", "NICE CG164", "ESMO Clinical Practice Guidelines"]
                }
            )

    def _handle_pharmacogenomics_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle pharmacogenomics queries"""
        return DomainQueryResult(
            domain_name="medical_genetics",
            answer=(
                "PHARMACOGENOMICS: Genetic Variation in Drug Response\n\n"
                "Pharmacogenomics studies how genes affect drug response:\n\n"
                "1. CLINICALLY SIGNIFICANT PHARMACOGENOMIC MARKERS:\n\n"
                "   CYP2D6 (Codeine, Tramadol, Tamoxifen, Antidepressants):\n"
                "   - Poor metabolizers (PM): No activation of prodrugs (codeine ineffective)\n"
                "   - Ultra-rapid metabolizers (UM): Toxicity from active drugs\n"
                "   - Action: Avoid codeine/tramadol in PMs/UMs, consider alternatives\n\n"
                "   CYP2C19 (Clopidogrel, PPIs, Antidepressants):\n"
                "   - Poor metabolizers: Clopidogrel ineffective (no activation)\n"
                "   - Action: Consider alternative antiplatelet (prasugrel, ticagrelor)\n\n"
                "   TPMT (Thiopurines: Azathioprine, 6-MP, 6-TG):\n"
                "   - Deficient activity: High risk of myelosuppression\n"
                "   - Action: Dose reduce or avoid thiopurines in deficient patients\n\n"
                "   NUDT15 (Thiopurines):\n"
                "   - Variants: High risk of myelosuppression (especially in Asians)\n"
                "   - Action: Similar to TPMT, dose adjust or avoid\n\n"
                "   UGT1A1 (Irinotecan):\n"
                "   - *28 allele: Increased toxicity (neutropenia, diarrhea)\n"
                "   - Action: Dose reduce irinotecan in homozygous *28\n\n"
                "   SLCO1B1 (Statins):\n"
                "   - *5 allele: Increased statin-induced myopathy risk\n"
                "   - Action: Consider lower dose or alternative statin\n\n"
                "   HLA-B*57:01 (Abacavir):\n"
                "   - Positive: Hypersensitivity reaction risk\n"
                "   - Action: Do NOT prescribe abacavir (mandatory testing)\n\n"
                "   HLA-B*15:02 (Carbamazepine):\n"
                "   - Positive: Stevens-Johnson syndrome risk (especially Asians)\n"
                "   - Action: Avoid carbamazepine, use alternative\n\n"
                "   DPYD (Fluoropyrimidines: 5-FU, Capecitabine):\n"
                "   - Deficient: Severe/lethal toxicity risk\n"
                "   - Action: Dose reduce or avoid fluoropyrimidines\n\n"
                "2. TESTING CONSIDERATIONS:\n"
                "   - Pre-treatment testing recommended for: Abacavir, Carbamazepine (Asians),\n"
                "     Thiopurines, Fluoropyrimidines, Irinotecan (in some centers)\n"
                "   - Consider testing for: CYP2D6 (opioid prescribing), CYP2C19 (clopidogrel)\n"
                "   - Many tests not routinely available yet\n"
                "   - Cost-effectiveness varies by test and indication\n\n"
                "3. LIMITATIONS:\n"
                "   - Not all drug-gene interactions have clinical guidelines\n"
                "   - Environmental factors also affect drug response\n"
                "   - Polypharmacy can cause complex interactions\n"
                "   - Clinical judgment still essential\n\n"
                "4. RESOURCES:\n"
                "   - CPIC (Clinical Pharmacogenetics Implementation Consortium)\n"
                "   - DPWG (Dutch Pharmacogenetics Working Group)\n"
                "   - FDA table of pharmacogenomic biomarkers\n\n"
                "Consult Clinical Pharmacist or Clinical Genetics for complex cases.\n\n"
                "Sources: CPIC Guidelines, DPWG Guidelines, FDA, BNF"
            ),
            confidence=0.90,
            metadata={
                "category": "pharmacogenomics",
                "sources": ["CPIC Guidelines", "DPWG Guidelines", "FDA Biomarker Table", "BNF"]
            }
        )

    def _handle_pediatric_genetics_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle pediatric genetics and dysmorphology queries"""
        query_lower = query.lower()

        # Developmental delay / intellectual disability
        if any(term in query_lower for term in ["developmental delay", "intellectual disability", "global delay"]):
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "PEDIATRIC GENETICS: Developmental Delay / Intellectual Disability\n\n"
                    "Genetic evaluation of developmental delay/intellectual disability:\n\n"
                    "1. INITIAL EVALUATION:\n"
                    "   - Detailed prenatal and birth history\n"
                    "   - Detailed developmental history\n"
                    "   - Three-generation family history\n"
                    "   - Physical examination (including dysmorphology)\n"
                    "   - Neurological examination\n"
                    "   - Growth parameters (height, weight, OFC)\n\n"
                    "2. FIRST-TIER GENETIC TESTS:\n"
                    "   Chromosomal microarray (CMA):\n"
                    "   - Detects microdeletions/duplications >10-20kb\n"
                    "   - Diagnostic yield: 15-20% (higher with dysmorphic features)\n"
                    "   - Recommended as first-tier test (ACMG, BSGM)\n\n"
                    "   Fragile X testing:\n"
                    "   - Especially in males with intellectual disability\n"
                    "   - Diagnostic yield: 2-6% (males), <1% (females)\n"
                    "   - Recommended if not already done\n\n"
                    "3. SECOND-TIER TESTS (if first-line negative):\n"
                    "   Whole exome sequencing (WES):\n"
                    "   - Diagnostic yield: 30-40% (after negative CMA)\n"
                    "   - Increasingly used as first-line with CMA\n"
                    "   - Requires trio testing (child + both parents)\n\n"
                    "   Whole genome sequencing (WGS):\n"
                    "   - Higher diagnostic yield than WES in some cases\n"
                    "   - Detects non-coding variants, structural variants\n"
                    "   - Increasing availability\n\n"
                    "4. METABOLIC SCREENING:\n"
                    "   - Consider if suggestive features (regression, episodic decompensation)\n"
                    "   - Plasma amino acids, urine organic acids\n"
                    "   - Specific metabolic tests as indicated\n\n"
                    "5. OTHER CONSIDERATIONS:\n"
                    "   - Karyotype (if CMA not done and dysmorphic features)\n"
                    "   - Methylation studies (if imprinting disorder suspected)\n"
                    "   - Specific single-gene tests (if syndrome suspected)\n"
                    "   - EEG (if epilepsy)\n"
                    "   - Neuroimaging (MRI brain)\n\n"
                    "6. ETIOLOGIES:\n"
                    "   - Genetic: 30-50% (with comprehensive testing)\n"
                    "   - Cerebral palsy/perinatal insult: 10-20%\n"
                    "   - Environmental: 5-10%\n"
                    "   - Unknown: Remainder\n\n"
                    "7. MANAGEMENT PRINCIPLES:\n"
                    "   - Early intervention services\n"
                    "   - Special education support\n"
                    "   - Regular surveillance for associated problems\n"
                    "   - Genetic counseling for family\n\n"
                    "Refer to Pediatric Genetics/Clinical Genetics for evaluation.\n\n"
                    "Sources: ACMG Practice Guidelines, BSGM, AAN Guidelines"
                ),
                confidence=0.90,
                metadata={
                    "category": "pediatric_genetics",
                    "condition": "developmental_delay",
                    "first_tier_tests": ["cma", "fragile_x"],
                    "sources": ["ACMG Practice Guidelines", "BSGM", "American Academy of Neurology"]
                }
            )

        # Autism spectrum disorder
        elif "autism" in query_lower:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "PEDIATRIC GENETICS: Autism Spectrum Disorder (ASD)\n\n"
                    "Genetic evaluation of autism spectrum disorder:\n\n"
                    "1. GENETIC ETIOLOGY:\n"
                    "   - Heritability: ~70-90%\n"
                    "   - Many genes involved (polygenic in most cases)\n"
                    "   - Single gene disorders: ~5-10% (Fragile X, Tuberous Sclerosis, etc.)\n"
                    "   - CNVs: ~5-10% (16p11.2, 15q11-13, etc.)\n"
                    "   - Known genetic cause identified in ~15-30% with comprehensive testing\n\n"
                    "2. RECOMMENDED GENETIC TESTING:\n"
                    "   First-tier:\n"
                    "   - Chromosomal microarray (CMA): Diagnostic yield ~5-10%\n"
                    "   - Fragile X testing: Especially in males\n\n"
                    "   Second-tier (if first-tier negative):\n"
                    "   - Whole exome sequencing (WES): Diagnostic yield ~10-30%\n"
                    "   - Consider earlier if dysmorphic features or congenital anomalies\n\n"
                    "3. SPECIFIC SYNDROMES TO CONSIDER:\n"
                    "   - Fragile X syndrome\n"
                    "   - Tuberous sclerosis complex\n"
                    "   - Neurofibromatosis type 1\n"
                    "   - PTEN hamartoma syndrome\n"
                    "   - Rett syndrome (MECP2) - females\n"
                    "   - Angelman/Prader-Willi syndromes\n"
                    "   - Many others\n\n"
                    "4. RED FLAGS FOR SPECIFIC GENETIC SYNDROME:\n"
                    "   - Dysmorphic features\n"
                    "   - Congenital anomalies\n"
                    "   - Regression (loss of skills)\n"
                    "   - Seizures\n"
                    "   - Macro/microcephaly\n"
                    "   - Growth abnormalities\n"
                    "   - Skin findings (hypopigmentation, cafe-au-lait)\n\n"
                    "5. BENEFITS OF GENETIC DIAGNOSIS:\n"
                    "   - Recurrence risk counseling for family\n"
                    "   - End-organ surveillance (e.g., TSC)\n"
                    "   - Prognostic information\n"
                    "   - Ending diagnostic odyssey\n"
                    "   - Support from condition-specific groups\n"
                    "   - Eligibility for services\n\n"
                    "6. FAMILY IMPLICATIONS:\n"
                    "   - Slightly increased recurrence risk (~10-20%)\n"
                    "   - Parental testing may be indicated\n"
                    "   - Genetic counseling recommended\n\n"
                    "Refer to Pediatric Genetics/Clinical Genetics for evaluation.\n\n"
                    "Sources: ACMG Practice Guidelines, BSGM, AAP Guidelines"
                ),
                confidence=0.90,
                metadata={
                    "category": "pediatric_genetics",
                    "condition": "autism",
                    "heritability": "70-90%",
                    "sources": ["ACMG Practice Guidelines", "BSGM", "American Academy of Pediatrics"]
                }
            )

        # General pediatric genetics / dysmorphology
        else:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "PEDIATRIC GENETICS: Dysmorphology and Genetic Syndromes\n\n"
                    "Evaluation of children with possible genetic conditions:\n\n"
                    "1. DYSMORPHOLOGY ASSESSMENT:\n"
                    "   - Detailed physical examination\n"
                    "   - Measurement: Growth parameters, facial proportions\n"
                    "   - Photography (with consent)\n"
                    "   - Recognition of patterns/malformations\n\n"
                    "2. APPROACH TO DIAGNOSIS:\n"
                    "   - Detailed history (prenatal, birth, developmental, family)\n"
                    "   - Three-generation pedigree\n"
                    "   - Physical examination (dysmorphology assessment)\n"
                    "   - Targeted genetic testing based on clinical findings\n"
                    "   - First-tier: Chromosomal microarray (CMA)\n"
                    "   - Second-tier: Whole exome sequencing (WES)\n\n"
                    "3. CATEGORIES OF GENETIC CONDITIONS:\n"
                    "   Chromosomal disorders:\n"
                    "   - Aneuploidies (T21, T18, T13, sex chromosome)\n"
                    "   - Microdeletion syndromes (22q11.2, etc.)\n"
                    "   - Microduplication syndromes\n\n"
                    "   Single-gene disorders:\n"
                    "   - Autosomal dominant (e.g., Neurofibromatosis)\n"
                    "   - Autosomal recessive (e.g., Cystic fibrosis)\n"
                    "   - X-linked (e.g., Fragile X)\n"
                    "   - Mitochondrial\n\n"
                    "   Multifactorial:\n"
                    "   - Combination of genetic and environmental factors\n\n"
                    "4. COMMON SYNDROMES TO RECOGNIZE:\n"
                    "   - Down syndrome (Trisomy 21)\n"
                    "   - Turner syndrome (45,X)\n"
                    "   - Noonan syndrome\n"
                    "   - Neurofibromatosis type 1\n"
                    "   - Tuberous sclerosis\n"
                    "   - Fragile X syndrome\n"
                    "   - 22q11.2 deletion syndrome\n"
                    "   - Many others\n\n"
                    "5. DIAGNOSTIC TOOLS:\n"
                    "   - CMA (first-tier for DD/ID, ASD, dysmorphic features)\n"
                    "   - Karyotype (for suspected aneuploidy)\n"
                    "   - FISH (targeted testing)\n"
                    "   - Single-gene testing (for specific syndromes)\n"
                    "   - Gene panels (e.g., epilepsy panel)\n"
                    "   - WES (if CMA negative)\n"
                    "   - WGS (if WES negative or for specific indications)\n\n"
                    "6. REFERRAL CRITERIA:\n"
                    "   - Developmental delay/intellectual disability\n"
                    "   - Autism spectrum disorder\n"
                    "   - Dysmorphic features\n"
                    "   - Congenital anomalies (multiple)\n"
                    "   - Unusual facial features\n"
                    "   - Growth abnormalities\n"
                    "   - Family history of genetic condition\n\n"
                    "Refer to Pediatric Genetics/Clinical Genetics for evaluation.\n\n"
                    "Sources: ACMG Practice Guidelines, BSGM, GeneReviews"
                ),
                confidence=0.88,
                metadata={
                    "category": "pediatric_genetics",
                    "sources": ["ACMG Practice Guidelines", "BSGM", "GeneReviews"]
                }
            )

    def _handle_mendelian_disorders_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle Mendelian disorder queries"""
        query_lower = query.lower()

        # Cystic fibrosis
        if "cystic fibrosis" in query_lower or " cf" in query_lower:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "MENDELIAN GENETICS: Cystic Fibrosis (CF)\n\n"
                    "Cystic fibrosis is an autosomal recessive disorder caused by pathogenic variants in CFTR:\n\n"
                    "1. INHERITANCE:\n"
                    "   - Autosomal recessive\n"
                    "   - Both parents are carriers (asymptomatic)\n"
                    "   - 25% risk of affected child with each pregnancy\n"
                    "   - Carrier frequency: ~1 in 25 in Northern Europeans\n\n"
                    "2. CLINICAL FEATURES:\n"
                    "   - Chronic lung disease (bronchiectasis, recurrent infections)\n"
                    "   - Pancreatic insufficiency (malabsorption, steatorrhea)\n"
                    "   - Male infertility (absence of vas deferens)\n"
                    "   - Elevated sweat chloride (diagnostic)\n"
                    "   - Sinus disease, liver disease\n\n"
                    "3. DIAGNOSIS:\n"
                    "   - Sweat chloride test (gold standard)\n"
                    "   - CFTR genetic testing (for confirmation and carrier testing)\n"
                    "   - Newborn screening (immunoreactive trypsinogen)\n\n"
                    "4. GENETICS:\n"
                    "   - Over 2000 CFTR variants identified\n"
                    "   - F508del is most common (~70% of CF alleles in Caucasians)\n"
                    "   - Genotype-phenotype correlation (partial)\n"
                    "   - Different classes of variants (I-VI)\n\n"
                    "5. MANAGEMENT:\n"
                    "   - Chest physiotherapy\n"
                    "   - Pancreatic enzyme replacement\n"
                    "   - CFTR modulator therapies (e.g., ivacaftor, lumacaftor/ivacaftor)\n"
                    "   - Lung transplantation in advanced disease\n"
                    "   - Multidisciplinary CF team\n\n"
                    "6. PROGNOSIS:\n"
                    "   - Median survival: ~40-50 years (improving with new therapies)\n"
                    "   - Highly variable based on genotype and treatment\n\n"
                    "7. CARRIER SCREENING:\n"
                    "   - Offered to all couples planning pregnancy (UK, US)\n"
                    "   - Extended carrier panels include CF\n\n"
                    "8. REPRODUCTIVE OPTIONS:\n"
                    "   - Prenatal diagnosis (CVS/amniocentesis)\n"
                    "   - Preimplantation genetic diagnosis (PGD)\n"
                    "   - Use of donor sperm/egg\n"
                    "   - Adoption\n\n"
                    "Refer to Clinical Genetics for genetic counseling and carrier testing.\n\n"
                    "Sources: NICE NG219, GeneReviews, Cystic Fibrosis Trust"
                ),
                confidence=0.95,
                metadata={
                    "category": "mendelian_disorder",
                    "condition": "cystic_fibrosis",
                    "inheritance": "autosomal_recessive",
                    "carrier_frequency": "1 in 25 (Northern Europeans)",
                    "sources": ["NICE NG219", "GeneReviews", "UK Cystic Fibrosis Trust"]
                }
            )

        # Huntington disease
        elif any(term in query_lower for term in ["huntington", "huntington's", "hd"]):
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "MENDELIAN GENETICS: Huntington Disease (HD)\n\n"
                    "Huntington disease is an autosomal dominant neurodegenerative disorder:\n\n"
                    "1. INHERITANCE:\n"
                    "   - Autosomal dominant\n"
                    "   - One affected parent: 50% risk to each child\n"
                    "   - Complete penetrance (if CAG repeat ≥ 36)\n"
                    "   - Anticipation: Earlier onset in subsequent generations\n\n"
                    "2. GENETICS:\n"
                    "   - Caused by CAG repeat expansion in HTT gene\n"
                    "   - Normal: ≤ 26 repeats\n"
                    "   - Intermediate/reduced penetrance: 27-35 repeats\n"
                    "   - Full penetrance: ≥ 36 repeats\n"
                    "   - Larger repeats: Earlier onset, more severe disease\n\n"
                    "3. CLINICAL FEATURES:\n"
                    "   - Movement disorder (chorea, dystonia, rigidity)\n"
                    "   - Cognitive decline (dementia)\n"
                    "   - Psychiatric symptoms (depression, psychosis, personality change)\n"
                    "   - Age of onset: typically 30-50 years\n\n"
                    "4. DIAGNOSIS:\n"
                    "   - Clinical diagnosis based on features\n"
                    "   - Genetic testing confirms diagnosis\n"
                    "   - Neuroimaging (caudate atrophy)\n\n"
                    "5. PREDICTIVE TESTING:\n"
                    "   - Available for at-risk asymptomatic adults\n"
                    "   - Extensive pre- and post-test counseling required\n"
                    "   - Not recommended for minors (<18 years)\n"
                    "   - Considerations: psychological, insurance, family, employment\n\n"
                    "6. PRENATAL TESTING:\n"
                    "   - Available for at-risk pregnancies\n"
                    "   - Usually requires affected parent to have known mutation\n"
                    "   - Preimplantation genetic diagnosis (PGD) available\n\n"
                    "7. MANAGEMENT:\n"
                    "   - Symptomatic treatment (chorea, psychiatric symptoms)\n"
                    "   - Multidisciplinary care\n"
                    "   - No disease-modifying treatment yet\n"
                    "   - Clinical trials ongoing\n\n"
                    "8. PROGNOSIS:\n"
                    "   - Progressive disease\n"
                    "   - Death 15-20 years after onset\n\n"
                    "9. GENETIC COUNSELING:\n"
                    "   - Mandatory for predictive testing\n"
                    "   - Discuss implications for patient and family\n"
                    "   - Discuss potential benefits and harms of testing\n"
                    "   - Provide psychological support\n"
                    "   - Discuss implications for children\n\n"
                    "Refer to Clinical Genetics/Huntington Disease clinic for counseling.\n\n"
                    "Sources: NICE NG198, GeneReviews, Huntington Disease Society"
                ),
                confidence=0.95,
                metadata={
                    "category": "mendelian_disorder",
                    "condition": "huntington_disease",
                    "inheritance": "autosomal_dominant",
                    "penetrance": "complete",
                    "sources": ["NICE NG198", "GeneReviews", "Huntington Disease Society"]
                }
            )

        # Muscular dystrophy
        elif any(term in query_lower for term in ["muscular dystrophy", "duchenne", "dmd", "becker", "bmd"]):
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "MENDELIAN GENETICS: Duchenne/Becker Muscular Dystrophy\n\n"
                    "Duchenne (DMD) and Becker (BMD) muscular dystrophies are X-linked recessive disorders:\n\n"
                    "1. INHERITANCE:\n"
                    "   - X-linked recessive\n"
                    "   - Carrier mother: 50% risk to sons (affected), 50% to daughters (carriers)\n"
                    "   - Affected male: All daughters are carriers, sons unaffected\n"
                    "   - 1/3 are de novo mutations (mother not carrier)\n\n"
                    "2. GENETICS:\n"
                    "   - Caused by pathogenic variants in DMD gene (dystrophin)\n"
                    "   - DMD: Out-of-frame variants (no functional dystrophin)\n"
                    "   - BMD: In-frame variants (reduced dystrophin)\n"
                    "   - DMD is more severe, BMD milder\n\n"
                    "3. CLINICAL FEATURES:\n"
                    "   Duchenne (DMD):\n"
                    "   - Onset: 2-5 years\n"
                    "   - Progressive proximal muscle weakness\n"
                    "   - Gower's sign, calf pseudohypertrophy\n"
                    "   - Loss of ambulation: ~12 years\n"
                    "   - Cardiomyopathy, respiratory failure\n"
                    "   - Death: typically 20s-30s (improving with care)\n\n"
                    "   Becker (BMD):\n"
                    "   - Onset: adolescence/adulthood\n"
                    "   - Milder, slower progression\n"
                    "   - May maintain ambulation into 40s-60s\n"
                    "   - Cardiomyopathy risk remains\n\n"
                    "4. DIAGNOSIS:\n"
                    "   - CK (creatine kinase) elevated\n"
                    "   - Genetic testing (MLPA, sequencing) confirms diagnosis\n"
                    "   - Muscle biopsy (if genetic testing negative)\n\n"
                    "5. MANAGEMENT:\n"
                    "   - Corticosteroids (slows progression in DMD)\n"
                    "   - Physical therapy, orthopedic interventions\n"
                    "   - Cardiac and respiratory surveillance\n"
                    "   - Exon skipping therapies (e.g., eteplirsen) for specific mutations\n"
                    "   - Gene therapy trials\n\n"
                    "6. CARRIER TESTING:\n"
                    "   - Offered to female relatives of affected male\n"
                    "   - CK screening (may be elevated in carriers)\n"
                    "   - Genetic testing confirms carrier status\n"
                    "   - Carrier females may have mild cardiomyopathy\n\n"
                    "7. REPRODUCTIVE OPTIONS:\n"
                    "   - Prenatal diagnosis\n"
                    "   - Preimplantation genetic diagnosis (PGD)\n"
                    "   - Use of donor egg\n\n"
                    "8. NEWBORN SCREENING:\n"
                    "   - Some countries screen newborn males for DMD\n"
                    "   - Allows early intervention\n\n"
                    "Refer to Clinical Genetics/Neuromuscular clinic for counseling.\n\n"
                    "Sources: NICE NG235, GeneReviews, Muscular Dystrophy UK"
                ),
                confidence=0.95,
                metadata={
                    "category": "mendelian_disorder",
                    "condition": "muscular_dystrophy",
                    "inheritance": "x-linked_recessive",
                    "sources": ["NICE NG235", "GeneReviews", "Muscular Dystrophy UK"]
                }
            )

        # Sickle cell disease
        elif any(term in query_lower for term in ["sickle cell", "sickle-cell"]):
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "MENDELIAN GENETICS: Sickle Cell Disease\n\n"
                    "Sickle cell disease is an autosomal recessive hemoglobinopathy:\n\n"
                    "1. INHERITANCE:\n"
                    "   - Autosomal recessive\n"
                    "   - Both parents carriers (sickle cell trait)\n"
                    "   - 25% risk of affected child with each pregnancy\n"
                    "   - Carrier frequency: varies by population\n\n"
                    "2. GENETICS:\n"
                    "   - Caused by mutation in β-globin gene (HbS)\n"
                    "   - Homozygous HbSS: Sickle cell anemia (most common/severe)\n"
                    "   - Compound heterozygotes: HbSC, HbS/β-thalassemia, etc.\n"
                    "   - HbAS: Sickle cell trait (carrier, usually asymptomatic)\n\n"
                    "3. CLINICAL FEATURES:\n"
                    "   - Chronic hemolytic anemia\n"
                    "   - Vaso-occlusive crises (pain crises)\n"
                    "   - Increased infection risk (especially pneumococcus)\n"
                    "   - Acute chest syndrome\n"
                    "   - Stroke risk\n"
                    "   - Splenic dysfunction, organ damage\n\n"
                    "4. DIAGNOSIS:\n"
                    "   - Newborn screening (hemoglobin electrophoresis/HPLC)\n"
                    "   - Sickling test\n"
                    "   - Genetic testing (if indicated)\n\n"
                    "5. MANAGEMENT:\n"
                    "   - Penicillin prophylaxis (children)\n"
                    "   - Vaccinations (pneumococcal, meningococcal, Hib, influenza)\n"
                    "   - Hydroxycarbamide (hydroxyurea)\n"
                    "   - Pain management during crises\n"
                    "   - Blood transfusions\n"
                    "   - Hematopoietic stem cell transplantation (curative)\n"
                    "   - Gene therapy trials\n\n"
                    "6. PROGNOSIS:\n"
                    "   - Improved with modern care (many adults living into 50s-60s)\n"
                    "   - Variable based on genotype, access to care\n\n"
                    "7. CARRIER SCREENING:\n"
                    "   - Offered to at-risk populations\n"
                    "   - Sickle cell trait (HbAS) generally asymptomatic\n"
                    "   - Rare complications with extreme dehydration/hypoxia\n\n"
                    "8. REPRODUCTIVE OPTIONS:\n"
                    "   - Prenatal diagnosis (CVS/amniocentesis)\n"
                    "   - Preimplantation genetic diagnosis (PGD)\n\n"
                    "9. POPULATION PREVALENCE:\n"
                    "   - Highest in African, Caribbean, Middle Eastern, Indian populations\n"
                    "   - Carrier frequency: up to 1 in 10 in some African populations\n\n"
                    "Refer to Clinical Genetics/Haematology for counseling.\n\n"
                    "Sources: NICE NG248, GeneReviews, Sickle Cell Society"
                ),
                confidence=0.95,
                metadata={
                    "category": "mendelian_disorder",
                    "condition": "sickle_cell_disease",
                    "inheritance": "autosomal_recessive",
                    "sources": ["NICE NG248", "GeneReviews", "Sickle Cell Society"]
                }
            )

        # Thalassemia
        elif "thalassemia" in query_lower:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "MENDELIAN GENETICS: Thalassemia\n\n"
                    "Thalassemias are autosomal recessive hemoglobinopathies:\n\n"
                    "1. TYPES:\n"
                    "   - Alpha thalassemia: Reduced alpha-globin production\n"
                    "   - Beta thalassemia: Reduced beta-globin production\n"
                    "   - Severity depends on specific mutations\n\n"
                    "2. ALPHA THALASSEMIA:\n"
                    "   - Caused by deletions in alpha-globin genes (HBA1, HBA2)\n"
                    "   - Silent carrier (1 gene deleted): Asymptomatic\n"
                    "   - Alpha thalassemia trait (2 genes deleted): Mild anemia\n"
                    "   - HbH disease (3 genes deleted): Moderate-severe hemolytic anemia\n"
                    "   - Hb Bart's (4 genes deleted): Hydrops fetalis, usually fatal\n\n"
                    "3. BETA THALASSEMIA:\n"
                    "   - Caused by mutations in beta-globin gene (HBB)\n"
                    "   - Minor (trait): Mild microcytic anemia, asymptomatic\n"
                    "   - Intermedia: Moderate anemia, may require transfusions\n"
                    "   - Major (Cooley's anemia): Severe anemia, transfusion-dependent\n\n"
                    "4. CLINICAL FEATURES:\n"
                    "   - Microcytic, hypochromic anemia\n"
                    "   - In severe forms: Growth retardation, bone deformities,\n"
                    "     hepatosplenomegaly, iron overload (from transfusions)\n\n"
                    "5. DIAGNOSIS:\n"
                    "   - CBC: Microcytic anemia\n"
                    "   - Hemoglobin electrophoresis/HPLC\n"
                    "   - Genetic testing (if indicated)\n"
                    "   - Prenatal diagnosis available\n\n"
                    "6. MANAGEMENT:\n"
                    "   - Regular transfusions (in severe forms)\n"
                    "   - Iron chelation therapy\n"
                    "   - Folic acid supplementation\n"
                    "   - Hematopoietic stem cell transplantation (curative)\n"
                    "   - Gene therapy trials\n\n"
                    "7. CARRIER SCREENING:\n"
                    "   - Offered to at-risk populations (Mediterranean, Asian, African)\n"
                    "   - Important for reproductive planning\n"
                    "   - Carrier detection: CBC, Hb electrophoresis\n\n"
                    "8. REPRODUCTIVE OPTIONS:\n"
                    "   - Prenatal diagnosis (CVS/amniocentesis)\n"
                    "   - Preimplantation genetic diagnosis (PGD)\n\n"
                    "9. POPULATION PREVALENCE:\n"
                    "   - Highest in Mediterranean, Middle Eastern, Indian, Southeast Asian\n"
                    "   - Beta thalassemia trait: up to 10% in some populations\n\n"
                    "Refer to Clinical Genetics/Haematology for counseling.\n\n"
                    "Sources: NICE NG209, GeneReviews, Thalassemia International Federation"
                ),
                confidence=0.95,
                metadata={
                    "category": "mendelian_disorder",
                    "condition": "thalassemia",
                    "inheritance": "autosomal_recessive",
                    "sources": ["NICE NG209", "GeneReviews", "Thalassemia International Federation"]
                }
            )

        # Fragile X
        elif any(term in query_lower for term in ["fragile x", "fragile-x"]):
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "MENDELIAN GENETICS: Fragile X Syndrome\n\n"
                    "Fragile X syndrome is an X-linked disorder caused by CGG repeat expansion in FMR1:\n\n"
                    "1. INHERITANCE:\n"
                    "   - X-linked dominant with reduced penetrance\n"
                    "   - Anticipation: Expansion in successive generations\n"
                    "   - Carrier females may have mild symptoms\n\n"
                    "2. GENETICS:\n"
                    "   - CGG repeat expansion in FMR1 gene\n"
                    "   - Normal: 5-44 repeats\n"
                    "   - Intermediate (gray zone): 45-54 repeats\n"
                    "   - Premutation: 55-200 repeats (carrier, risk of FXTAS, FXPOI)\n"
                    "   - Full mutation: >200 repeats (Fragile X syndrome)\n\n"
                    "3. CLINICAL FEATURES (males with full mutation):\n"
                    "   - Intellectual disability (moderate to severe)\n"
                    "   - Characteristic facial features (long face, large ears)\n"
                    "   - Macroorchidism (enlarged testes)\n"
                    "   - Behavioral problems (ADHD, autism features)\n"
                    "   - Speech and language delay\n"
                    "   - Connective tissue abnormalities (hyperextensible joints, flat feet)\n\n"
                    "4. FEMALES WITH FULL MUTATION:\n"
                    "   - Milder intellectual impairment (due to X-inactivation)\n"
                    "   - Learning difficulties, shyness, anxiety\n\n"
                    "5. CARRIER (PREMUTATION) ISSUES:\n"
                    "   - FXTAS (Fragile X-associated tremor/ataxia syndrome): Older carriers\n"
                    "   - FXPOI (primary ovarian insufficiency): Female carriers\n"
                    "   - Usually no intellectual disability\n\n"
                    "6. DIAGNOSIS:\n"
                    "   - DNA testing for CGG repeat expansion\n"
                    "   - Standard testing for males with intellectual disability\n"
                    "   - Family history of intellectual disability or autism\n\n"
                    "7. MANAGEMENT:\n"
                    "   - Early intervention and special education\n"
                    "   - Speech and language therapy\n"
                    "   - Behavioral therapy, educational support\n"
                    "   - Medication for ADHD, anxiety, aggression\n"
                    "   - No cure, supportive care\n\n"
                    "8. CARRIER TESTING:\n"
                    "   - Offered to:\n"
                    "     * Women with family history of Fragile X\n"
                    "     * Women with unexplained POI\n"
                    "     * Prenatal testing (if family history)\n"
                    "   - Cascade testing for relatives\n\n"
                    "9. REPRODUCTIVE OPTIONS:\n"
                    "   - Prenatal diagnosis (CVS/amniocentesis)\n"
                    "   - Preimplantation genetic diagnosis (PGD)\n"
                    "   - Use of donor egg\n\n"
                    "10. ANTICIPATION:\n"
                    "   - Premutation can expand to full mutation in one generation\n"
                    "   - Risk of expansion depends on premutation size\n\n"
                    "Refer to Clinical Genetics for counseling and testing.\n\n"
                    "Sources: GeneReviews, ACMG Practice Guidelines, Fragile X Society"
                ),
                confidence=0.95,
                metadata={
                    "category": "mendelian_disorder",
                    "condition": "fragile_x",
                    "inheritance": "x-linked_dominant",
                    "sources": ["GeneReviews", "ACMG Practice Guidelines", "Fragile X Society"]
                }
            )

        # General Mendelian / carrier screening
        else:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "MENDELIAN GENETICS: Single-Gene Disorders and Carrier Screening\n\n"
                    "Mendelian disorders follow classic inheritance patterns:\n\n"
                    "1. INHERITANCE PATTERNS:\n\n"
                    "   Autosomal Recessive:\n"
                    "   - Both parents carriers (asymptomatic)\n"
                    "   - 25% risk of affected child per pregnancy\n"
                    "   - Examples: CF, sickle cell, thalassemia, spinal muscular atrophy\n"
                    "   - Equal males and females affected\n\n"
                    "   Autosomal Dominant:\n"
                    "   - One affected parent (usually)\n"
                    "   - 50% risk to each child\n"
                    "   - Examples: Huntington, neurofibromatosis, Marfan, achondroplasia\n"
                    "   - Vertical transmission (generation to generation)\n\n"
                    "   X-Linked Recessive:\n"
                    "   - Carrier mother, affected sons\n"
                    "   - 50% of sons affected, 50% of daughters carriers\n"
                    "   - Examples: Duchenne MD, hemophilia, Fragile X\n"
                    "   - No male-to-male transmission\n\n"
                    "   X-Linked Dominant:\n"
                    "   - Affected parent (male or female)\n"
                    "   - Examples: Fragile X, some Rett syndrome cases\n"
                    "   - May be lethal in males\n\n"
                    "   Mitochondrial:\n"
                    "   - Maternal inheritance (mother to all children)\n"
                    "   - Examples: MELAS, MERRF, Leigh syndrome\n\n"
                    "2. CARRIER SCREENING:\n"
                    "   - Offered to all couples planning pregnancy (extended carrier panels)\n"
                    "   - Common conditions on panels:\n"
                    "     * Cystic fibrosis\n"
                    "     * Spinal muscular atrophy\n"
                    "     * Fragile X\n"
                    "     * Sickle cell and related hemoglobinopathies\n"
                    "     * Thalassemias\n"
                    "     * Many others (panel-dependent)\n\n"
                    "3. REPRODUCTIVE OPTIONS FOR CARRIER COUPLES:\n"
                    "   - Prenatal diagnosis (CVS/amniocentesis)\n"
                    "   - Preimplantation genetic diagnosis (PGD)\n"
                    "   - Use of donor gametes\n"
                    "   - Adoption\n"
                    "   - Continue pregnancy with affected child\n\n"
                    "4. GENETIC COUNSELING:\n"
                    "   - Discuss inheritance pattern and recurrence risk\n"
                    "   - Discuss natural history and prognosis\n"
                    "   - Discuss management options\n"
                    "   - Discuss reproductive options\n"
                    "   - Facilitate cascade testing for family\n\n"
                    "Refer to Clinical Genetics for counseling and carrier testing.\n\n"
                    "Sources: ACMG Practice Guidelines, BSGM, GeneReviews"
                ),
                confidence=0.90,
                metadata={
                    "category": "mendelian_genetics",
                    "sources": ["ACMG Practice Guidelines", "BSGM", "GeneReviews"]
                }
            )

    def _handle_chromosomal_disorders_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle chromosomal disorder queries"""
        query_lower = query.lower()

        # Turner syndrome
        if "turner" in query_lower:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "CHROMOSOMAL DISORDER: Turner Syndrome (45,X or variants)\n\n"
                    "Turner syndrome affects females and is caused by complete or partial absence of one X chromosome:\n\n"
                    "1. KARYOTYPES:\n"
                    "   - 45,X (40-50%)\n"
                    "   - Mosaicism (45,X/46,XX or others): 30-40%\n"
                    "   - X chromosome abnormalities: isochromosome Xq, ring X, deletions\n\n"
                    "2. CLINICAL FEATURES:\n"
                    "   - Short stature (most universal feature)\n"
                    "   - Gonadal dysgenesis (streak ovaries)\n"
                    "   - Primary amenorrhea, infertility\n"
                    "   - Webbed neck, low hairline\n"
                    "   - Broad chest, widely spaced nipples\n"
                    "   - Cubitus valgus, lymphedema (especially in newborns)\n"
                    "   - Cardiac anomalies (bicuspid aortic valve, coarctation)\n"
                    "   - Renal anomalies (horseshoe kidney)\n"
                    "   - Normal intelligence (may have specific learning difficulties)\n\n"
                    "3. DIAGNOSIS:\n"
                    "   - Karyotype (45,X or variant)\n"
                    "   - May be diagnosed prenatally (CVS/amniocentesis)\n"
                    "   - May present in childhood (lymphedema, webbed neck)\n"
                    "   - Often presents in adolescence (primary amenorrhea, short stature)\n\n"
                    "4. MANAGEMENT:\n"
                    "   Growth:\n"
                    "   - Growth hormone therapy (increases final height)\n"
                    "   - Start early, monitor IGF-1\n\n"
                    "   Puberty/Estrogen:\n"
                    "   - Estrogen replacement (induce puberty, maintain bone health)\n"
                    "   - Progesterone (after estrogen for menstrual cycle)\n"
                    "   - Usually start around 11-12 years\n\n"
                    "   Fertility:\n"
                    "   - Most infertile (streak ovaries)\n"
                    "   - Egg donation possible\n"
                    "   - Spontaneous pregnancy possible in mosaic Turner\n\n"
                    "   Surveillance:\n"
                    "   - Cardiac (aortic root dissection risk)\n"
                    "   - Renal (ultrasound)\n"
                    "   - Thyroid (autoimmune hypothyroidism risk)\n"
                    "   - Hearing, vision\n"
                    "   - Blood pressure monitoring\n\n"
                    "5. PROGNOSIS:\n"
                    "   - Normal life expectancy (unless cardiac complications)\n"
                    "   - Infertility (usually)\n"
                    "   - Short stature (without GH)\n\n"
                    "6. PSYCHOSOCIAL:\n"
                    "   - Support groups\n"
                    "   - Psychological support\n"
                    "   - Educational support (if learning difficulties)\n\n"
                    "7. RECURRENCE RISK:\n"
                    "   - Usually low (most cases de novo)\n"
                    "   - Slightly increased if maternal X abnormality\n\n"
                    "Refer to Clinical Genetics/Pediatric Endocrinology for management.\n\n"
                    "Sources: NICE NG272, GeneReviews, Turner Syndrome Support"
                ),
                confidence=0.95,
                metadata={
                    "category": "chromosomal_disorder",
                    "condition": "turner_syndrome",
                    "karyotype": "45,X or variants",
                    "sources": ["NICE NG272", "GeneReviews", "Turner Syndrome Society"]
                }
            )

        # Klinefelter syndrome
        elif "klinefelter" in query_lower:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "CHROMOSOMAL DISORDER: Klinefelter Syndrome (47,XXY or variants)\n\n"
                    "Klinefelter syndrome affects males and is caused by one or more extra X chromosomes:\n\n"
                    "1. KARYOTYPES:\n"
                    "   - 47,XXY (80-90%)\n"
                    "   - Mosaicism (46,XY/47,XXY): 10-20%\n"
                    "   - Higher-grade (48,XXXY, 49,XXXXY): More severe phenotype\n\n"
                    "2. CLINICAL FEATURES:\n"
                    "   - Small testes, hypergonadotropic hypogonadism\n"
                    "   - Infertility (azoospermia or severe oligospermia)\n"
                    "   - Tall stature, long limbs\n"
                    "   - Gynecomastia\n"
                    "   - Decreased facial/body hair\n"
                    "   - Learning/behavioral difficulties (language, executive function)\n"
                    "   - Usually normal intelligence\n"
                    "   - Increased risk of: Breast cancer, autoimmune disorders, DVT/PE\n\n"
                    "3. DIAGNOSIS:\n"
                    "   - Karyotype (47,XXY or variant)\n"
                    "   - Hormonal profile (high FSH/LH, low testosterone)\n"
                    "   - May be diagnosed:\n"
                    "     * Prenatally (incidental finding)\n"
                    "     * Infertility evaluation (adults)\n"
                    "     * Developmental/learning concerns\n\n"
                    "4. MANAGEMENT:\n"
                    "   Testosterone Replacement:\n"
                    "   - Induce/maintain puberty\n"
                    "   - Maintain secondary sexual characteristics\n"
                    "   - Bone health, muscle mass, energy, mood\n"
                    "   - Usually start at puberty\n\n"
                    "   Fertility:\n"
                    "   - Most infertile (azoospermia)\n"
                    "   - Testicular sperm extraction (TESE) + ICSI possible (some cases)\n"
                    "   - Mosaic cases: may have sperm in ejaculate\n"
                    "   - Donor sperm/adoption alternatives\n\n"
                    "   Educational Support:\n"
                    "   - Speech and language therapy (especially in childhood)\n"
                    "   - Educational support for learning difficulties\n"
                    "   - Psychological support\n\n"
                    "   Surveillance:\n"
                    "   - Breast examination (increased breast cancer risk)\n"
                    "   - Bone density (if low testosterone)\n"
                    "   - Metabolic profile (increased metabolic syndrome risk)\n"
                    "   - Thyroid (autoimmune risk)\n"
                    "   - Venous thromboembolism awareness\n\n"
                    "5. PROGNOSIS:\n"
                    "   - Normal life expectancy\n"
                    "   - Infertility (most, but not all)\n"
                    "   - Learning difficulties (usually mild)\n\n"
                    "6. PSYCHOSOCIAL:\n"
                    "   - Support groups\n"
                    "   - Psychological support\n"
                    "   - Counseling regarding infertility\n\n"
                    "7. RECURRENCE RISK:\n"
                    "   - Low (most cases de novo)\n"
                    "   - Slightly increased with advanced paternal age\n\n"
                    "Refer to Clinical Genetics/Endocrinology for management.\n\n"
                    "Sources: NICE NG272, GeneReviews, Klinefelter Syndrome Association"
                ),
                confidence=0.95,
                metadata={
                    "category": "chromosomal_disorder",
                    "condition": "klinefelter_syndrome",
                    "karyotype": "47,XXY or variants",
                    "sources": ["NICE NG272", "GeneReviews", "Klinefelter Syndrome Association"]
                }
            )

        # General chromosomal disorders
        else:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "CHROMOSOMAL DISORDERS\n\n"
                    "Chromosomal abnormalities involve changes in chromosome number or structure:\n\n"
                    "1. TYPES:\n\n"
                    "   Aneuploidy (abnormal chromosome number):\n"
                    "   - Trisomy: Extra chromosome (T21, T18, T13)\n"
                    "   - Monosomy: Missing chromosome (45,X - Turner syndrome)\n"
                    "   - Polysomy: Extra chromosomes (47,XXY - Klinefelter)\n\n"
                    "   Structural abnormalities:\n"
                    "   - Deletions: Missing segment (5p-, cri-du-chat)\n"
                    "   - Duplications: Extra segment (duplication)\n"
                    "   - Translocations: Exchange between chromosomes (balanced/unbalanced)\n"
                    "   - Inversions: Chromosome segment reversed\n"
                    "   - Ring chromosomes: Ends fused together\n"
                    "   - Isochromosomes: Mirror image chromosomes\n\n"
                    "   Mosaicism:\n"
                    "   - Two or more cell lines with different karyotypes\n"
                    "   - May result in milder phenotype\n\n"
                    "2. COMMON ANEUPLOIDIES:\n"
                    "   - Trisomy 21 (Down syndrome): Most common viable trisomy\n"
                    "   - Trisomy 18 (Edwards syndrome): Severe, limited survival\n"
                    "   - Trisomy 13 (Patau syndrome): Severe, limited survival\n"
                    "   - Sex chromosome aneuploidies: Turner (45,X), Klinefelter (47,XXY)\n\n"
                    "3. COMMON MICRODELETION SYNDROMES:\n"
                    "   - 22q11.2 deletion (DiGeorge/velocardiofacial syndrome)\n"
                    "   - 5p deletion (cri-du-chat syndrome)\n"
                    "   - 15q11-q13 deletion (Angelman/Prader-Willi)\n"
                    "   - 4p deletion (Wolf-Hirschhorn syndrome)\n"
                    "   - Many others\n\n"
                    "4. DIAGNOSIS:\n"
                    "   - Karyotype: Detects aneuploidies, large structural changes (>5-10 Mb)\n"
                    "   - FISH: Targeted testing for specific abnormalities\n"
                    "   - Chromosomal microarray (CMA): Detects microdeletions/duplications\n"
                    "   - May be diagnosed prenatally (CVS/amniocentesis)\n\n"
                    "5. ETIOLOGY:\n"
                    "   - Most are de novo (not inherited)\n"
                    "   - Some are inherited from parent with balanced translocation\n"
                    "   - Risk increases with maternal age (especially T21, T18, T13)\n\n"
                    "6. RECURRENCE RISK:\n"
                    "   - De novo cases: Low recurrence risk\n"
                    "   - Parental translocation: Risk depends on specific translocation\n\n"
                    "7. MANAGEMENT:\n"
                    "   - Condition-specific management\n"
                    "   - Early intervention, special education\n"
                    "   - Surveillance for associated problems\n"
                    "   - Genetic counseling for family\n\n"
                    "Refer to Clinical Genetics for counseling and testing.\n\n"
                    "Sources: GeneReviews, ACMG Practice Guidelines, BSGM"
                ),
                confidence=0.88,
                metadata={
                    "category": "chromosomal_disorders",
                    "sources": ["GeneReviews", "ACMG Practice Guidelines", "BSGM"]
                }
            )

    def _handle_mitochondrial_disorders_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle mitochondrial disorder queries"""
        return DomainQueryResult(
            domain_name="medical_genetics",
            answer=(
                "MITOCHONDRIAL DISORDERS\n\n"
                "Mitochondrial disorders are caused by mutations in mitochondrial DNA (mtDNA) or nuclear DNA affecting mitochondrial function:\n\n"
                "1. INHERITANCE:\n\n"
                "   Mitochondrial (mtDNA) inheritance:\n"
                "   - Maternal inheritance (mother to all children)\n"
                "   - No paternal transmission of mtDNA\n"
                "   - Heteroplasmy: Mixture of mutant and normal mtDNA\n"
                "   - Threshold effect: Symptoms when mutant load exceeds threshold\n"
                "   - Variable expression due to heteroplasmy and threshold\n\n"
                "   Autosomal recessive (nuclear DNA mutations affecting mitochondria)\n"
                "   Autosomal dominant (rare)\n"
                "   X-linked (rare)\n\n"
                "2. COMMON MITOCHONDRIAL DISORDERS:\n\n"
                "   MELAS (Mitochondrial Encephalomyopathy, Lactic Acidosis, Stroke-like episodes):\n"
                "   - mtDNA mutation (commonly m.3243A>G)\n"
                "   - Stroke-like episodes, encephalopathy, myopathy, diabetes, deafness\n\n"
                "   MERRF (Myoclonic Epilepsy with Ragged Red Fibers):\n"
                "   - mtDNA mutation (commonly m.8344A>G)\n"
                "   - Myoclonus, seizures, ataxia, myopathy\n\n"
                "   Leigh Syndrome (Subacute Necrotizing Encephalomyelopathy):\n"
                "   - Nuclear or mtDNA mutations\n"
                "   - Progressive neurodegeneration, developmental regression, respiratory failure\n"
                "   - Onset in infancy/early childhood\n"
                "   - Poor prognosis\n\n"
                "   Leber Hereditary Optic Neuropathy (LHON):\n"
                "   - mtDNA mutation\n"
                "   - Painless, bilateral vision loss (young adults)\n"
                "   - Males more commonly affected\n\n"
                "   Kearns-Sayre Syndrome:\n"
                "   - Large mtDNA deletion\n"
                "   - Progressive external ophthalmoplegia, pigmentary retinopathy,\n"
                "     cardiac conduction defects, myopathy\n\n"
                "3. CLINICAL FEATURES:\n"
                "   - Multisystem involvement (any organ)\n"
                "   - High-energy tissues most affected: Brain, muscle, heart, liver, kidney\n"
                "   - Common features: Weakness, fatigue, neurologic symptoms, diabetes, deafness\n"
                "   - Lactic acidosis (often present)\n\n"
                "4. DIAGNOSIS:\n"
                "   - Clinical suspicion (multisystem, maternal inheritance pattern)\n"
                "   - Lactic acid (elevated)\n"
                "   - Muscle biopsy (ragged red fibers)\n"
                "   - mtDNA testing (blood, muscle, urine)\n"
                "   - Nuclear gene testing (if mtDNA negative)\n\n"
                "5. MANAGEMENT:\n"
                "   - No cure, supportive care\n"
                "   - Avoid mitochondrial toxins (valproate, aminoglycosides, etc.)\n"
                "   - Coenzyme Q10 (some evidence of benefit)\n"
                "   - Symptomatic treatment (seizures, diabetes, cardiac, etc.)\n"
                "   - Multidisciplinary care\n\n"
                "6. PROGNOSIS:\n"
                "   - Variable, depends on specific disorder and severity\n"
                "   - Some cause early death (Leigh syndrome)\n"
                "   - Others have slower progression (MELAS, MERRF)\n\n"
                "7. RECURRENCE RISK:\n"
                "   - Maternal mtDNA mutations: Variable (heteroplasmy, bottleneck)\n"
                "   - Nuclear DNA mutations: Standard Mendelian risks\n\n"
                "8. REPRODUCTIVE OPTIONS:\n"
                "   - Prenatal diagnosis (limited by heteroplasmy)\n"
                "   - Mitochondrial replacement therapy (\"three-parent IVF\") - experimental\n"
                "   - Use of donor egg\n\n"
                "9. GENETIC COUNSELING:\n"
                "   - Complex due to heteroplasmy, threshold effect\n"
                "   - Pre-test and post-test counseling essential\n"
                "   - Discuss limitations of prenatal testing\n\n"
                "Refer to Clinical Genetics/Mitochondrial Disease clinic for evaluation.\n\n"
                "Sources: GeneReviews, ACMG Practice Guidelines, Mitochondrial Medicine Society"
            ),
            confidence=0.90,
            metadata={
                "category": "mitochondrial_disorders",
                "inheritance": "maternal (mtDNA) or mendelian (nuclear)",
                "sources": ["GeneReviews", "ACMG Practice Guidelines", "Mitochondrial Medicine Society"]
            }
        )

    def _handle_adult_onset_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle adult-onset genetic disorder queries"""
        return DomainQueryResult(
            domain_name="medical_genetics",
            answer=(
                "ADULT-ONSET GENETIC DISORDERS: Predictive and Presymptomatic Testing\n\n"
                "Many genetic disorders manifest in adulthood with no symptoms in childhood:\n\n"
                "1. COMMON ADULT-ONSET GENETIC DISORDERS:\n\n"
                "   Huntington Disease:\n"
                "   - Autosomal dominant\n"
                "   - Progressive neurodegeneration (chorea, dementia, psychiatric)\n"
                "   - Onset: 30-50 years\n"
                "   - No cure, predictive testing available\n\n"
                "   Hereditary Cancer Syndromes:\n"
                "   - BRCA1/BRCA2, Lynch syndrome, FAP, etc.\n"
                "   - Autosomal dominant\n"
                "   - Increased cancer risk\n"
                "   - Enhanced surveillance, risk-reducing surgery\n\n"
                "   Hereditary Hemochromatosis (HFE):\n"
                "   - Autosomal recessive\n"
                "   - Iron overload (liver, heart, pancreas)\n"
                "   - Preventable with phlebotomy\n\n"
                "   Familial Hypercholesterolemia:\n"
                "   - Autosomal dominant\n"
                "   - Severe hypercholesterolemia, premature CAD\n"
                "   - Treatable with statins, PCSK9 inhibitors\n\n"
                "   Polycystic Kidney Disease (ADPKD):\n"
                "   - Autosomal dominant\n"
                "   - Progressive renal cysts, kidney failure\n"
                "   - No cure, management of complications\n\n"
                "   Many others: Various neurodegenerative, cardiac, renal disorders\n\n"
                "2. PREDICTIVE TESTING:\n\n"
                "   Indications:\n"
                "   - Adult with family history of adult-onset genetic disorder\n"
                "   - Asymptomatic, at risk of inheriting mutation\n"
                "   - Usually requires known mutation in family\n\n"
                "   Prerequisites:\n"
                "   - Adult (≥18 years for most conditions)\n"
                "   - Informed consent\n"
                    "   - Extensive genetic counseling (pre- and post-test)\n"
                "   - Consider psychological, insurance, family implications\n"
                "   - No coercion (must be autonomous decision)\n\n"
                "   Issues to Discuss:\n"
                "   - Natural history of disease\n"
                "   - Penetrance, variable expressivity\n"
                "   - Available interventions (surveillance, treatment)\n"
                "   - Psychological impact (knowing vs. not knowing)\n"
                "   - Insurance/employment implications\n"
                "   - Family implications (children, siblings, parents)\n"
                "   - Reproductive options (PGD)\n\n"
                "3. COUNSELING CONSIDERATIONS:\n"
                "   - Right not to know (autonomy)\n"
                "   - Potential for discrimination (genetic discrimination laws vary)\n"
                "   - Impact on family dynamics\n"
                "   - Survivor guilt (if testing negative while relatives positive)\n"
                "   - Anxiety, depression risk\n"
                "   - Planning for future (medical, financial, personal)\n\n"
                "4. BENEFITS OF TESTING:\n"
                "   - End uncertainty\n"
                "   - Inform medical management (surveillance, preventive interventions)\n"
                "   - Reproductive planning (PGD, prenatal diagnosis)\n"
                "   - Inform life planning (career, finances, relationships)\n"
                "   - Allow family members to make informed choices\n\n"
                "5. LIMITATIONS:\n"
                "   - Not all disorders have interventions\n"
                "   - Penetrance may be incomplete\n"
                "   - Cannot predict exact age of onset or severity\n"
                "   - May cause psychological distress\n\n"
                "6. SPECIAL CONSIDERATIONS:\n"
                "   - Huntington disease: Extensive counseling protocol, mandatory in many centers\n"
                "   - Hereditary cancer: Strong benefit (surveillance, prevention)\n"
                "   - Testing for minors: Generally not recommended (adult autonomy)\n"
                "   - Insurance: Genetic discrimination protections vary by country\n\n"
                "7. POST-TEST COUNSELING:\n"
                "   - Discuss results (positive, negative, VUS)\n"
                "   - Psychologist/support if positive\n"
                "   - Discuss medical management plan\n"
                "   - Discuss family implications\n"
                "   - Long-term follow-up\n\n"
                "Refer to Clinical Genetics for counseling and testing.\n\n"
                "Sources: ACMG Practice Guidelines, BSGM, GeneReviews"
            ),
            confidence=0.90,
            metadata={
                "category": "adult_onset_genetics",
                "sources": ["ACMG Practice Guidelines", "BSGM", "GeneReviews"]
            }
        )

    def _handle_reproductive_genetics_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle reproductive genetics queries (PGD/PGS)"""
        return DomainQueryResult(
            domain_name="medical_genetics",
            answer=(
                "REPRODUCTIVE GENETICS: Preimplantation Genetic Diagnosis (PGD/PGS)\n\n"
                "Preimplantation genetic testing allows genetic testing of embryos created by IVF:\n\n"
                "1. TYPES:\n\n"
                "   PGD (Preimplantation Genetic Diagnosis):\n"
                "   - Testing for known single-gene disorder or specific mutation\n"
                "   - For couples at known risk of genetic condition\n"
                "   - Examples: BRCA, CF, SMA, Huntington, Fragile X, etc.\n\n"
                "   PGS (Preimplantation Genetic Screening):\n"
                "   - Aneuploidy screening (testing chromosome number)\n"
                "   - For couples with recurrent miscarriage, IVF failure, advanced maternal age\n"
                "   - Also called PGT-A (Preimplantation Genetic Testing for Aneuploidy)\n\n"
                "2. PROCESS:\n"
                "   - IVF to create embryos\n"
                "   - Embryo biopsy (day 3 or day 5)\n"
                    "   - Genetic testing of biopsied cells\n"
                "   - Embryos without abnormality selected for transfer\n"
                "   - Pregnancy achieved with unaffected embryo\n\n"
                "3. BIOPSY TYPES:\n"
                "   - Polar body biopsy (maternal genetic material only)\n"
                "   - Cleavage stage biopsy (day 3, 1 blastomere)\n"
                "   - Blastocyst biopsy (day 5, trophectoderm cells)\n\n"
                "4. TESTING METHODS:\n"
                "   - FISH (limited number of chromosomes)\n"
                "   - PCR (for single-gene disorders)\n"
                "   - aCGH (array comparative genomic hybridization)\n"
                "   - NGS (next-generation sequencing)\n\n"
                "5. INDICATIONS:\n"
                "   - Known single-gene disorder in family\n"
                "   - Chromosomal rearrangement (balanced translocation)\n"
                "   - Recurrent pregnancy loss\n"
                "   - Repeated IVF failure\n"
                "   - Advanced maternal age\n"
                "   - Previous child with genetic condition\n"
                "   - Carrier of autosomal recessive or X-linked disorder\n\n"
                "6. BENEFITS:\n"
                "   - Avoid pregnancy termination (prenatal diagnosis)\n"
                "   - Prevent transmission of known genetic disorder\n"
                "   - Reduce miscarriage risk (by selecting euploid embryos)\n"
                "   - Improve IVF success rates\n"
                "   - Reduce risk of child with genetic condition\n\n"
                "7. LIMITATIONS:\n"
                "   - Requires IVF (expensive, invasive, not guaranteed success)\n"
                "   - Testing not 100% accurate (false positives/negatives)\n"
                "   - Mosaicism (embryo may have mixed normal/abnormal cells)\n"
                "   - No embryo suitable for transfer (possible outcome)\n"
                "   - May not detect all abnormalities\n"
                "   - Long-term outcomes still being studied\n\n"
                "8. ACCURACY:\n"
                "   - High but not 100%\n"
                "   - Prenatal testing (amniocentesis) still recommended to confirm\n\n"
                "9. ETHICAL CONSIDERATIONS:\n"
                "   - \"Designer babies\" concerns\n"
                "   - Embryo discard (embryos with abnormality)\n"
                "   - Equity/access (expensive, not universally available)\n"
                "   - Selection for non-medical traits (not done, but ethical concern)\n"
                "   - Disability rights perspective\n\n"
                "10. COST AND AVAILABILITY:\n"
                "   - Expensive (IVF + PGD)\n"
                "   - Not universally available\n"
                "   - May be funded by NHS for some conditions (UK)\n\n"
                "11. SUCCESS RATES:\n"
                "   - Live birth rates vary by center, indication, maternal age\n"
                "   - Generally lower than standard IVF (due to embryo selection)\n"
                "   - Selection of euploid embryo improves implantation rate\n\n"
                "12. ALTERNATIVES:\n"
                "   - Prenatal diagnosis (CVS/amniocentesis) with possible termination\n"
                "   - Use of donor gametes\n"
                "   - Adoption\n"
                "   - Accept natural pregnancy risk\n\n"
                "Refer to Fetal Medicine/Clinical Genetics/IVF clinic for counseling.\n\n"
                "Sources: HFEA, BSGM, ASRM, ESHRE Guidelines"
            ),
            confidence=0.92,
            metadata={
                "category": "reproductive_genetics",
                "sources": ["HFEA", "BSGM", "ASRM Guidelines", "ESHRE Guidelines"]
            }
        )

    def _handle_test_interpretation_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle genetic test result interpretation queries"""
        query_lower = query.lower()

        # Variant of uncertain significance
        if "vus" in query_lower or "variant of uncertain" in query_lower or "uncertain significance" in query_lower:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "GENETIC TEST INTERPRETATION: Variant of Uncertain Significance (VUS)\n\n"
                    "A VUS is a genetic variant where clinical significance is not yet known:\n\n"
                    "1. WHAT IT MEANS:\n"
                    "   - Genetic variant found, but significance unclear\n"
                    "   - May be pathogenic or benign\n"
                    "   - Not enough evidence to classify\n"
                    "   - Should NOT be used for clinical decision-making\n\n"
                    "2. FREQUENCY:\n"
                    "   - Common in genetic testing (especially exome/genome sequencing)\n"
                    "   - More common in under-studied genes\n"
                    "   - Less common in well-established genes (BRCA, CFTR, etc.)\n\n"
                    "3. MANAGEMENT OF VUS:\n"
                    "   - Do NOT change management based on VUS\n"
                    "   - Treat as if VUS not present (manage based on family history)\n"
                    "   - Do NOT offer predictive testing for VUS to relatives\n"
                    "   - Reclassification possible over time (research, more data)\n\n"
                    "4. RECLASSIFICATION:\n"
                    "   - VUS may be reclassified as:\n"
                    "     * Pathogenic/likely pathogenic\n"
                    "     * Benign/likely benign\n"
                    "   - May take years or never be reclassified\n"
                    "   - Some laboratories offer reclassification notifications\n\n"
                    "5. FAMILY IMPLICATIONS:\n"
                    "   - Do NOT test relatives for VUS\n"
                    "   - Do NOT make reproductive decisions based on VUS\n"
                    "   - Manage based on family history, not VUS\n\n"
                    "6. PATIENT COMMUNICATION:\n"
                    "   - Explain uncertainty clearly\n"
                    "   - Emphasize not changing management based on VUS\n"
                    "   - Discuss possibility of future reclassification\n"
                    "   - Written information helpful\n\n"
                    "7. EXAMPLES OF VUS:\n"
                    "   - Missense variant of unknown functional impact\n"
                    "   - Variant not previously reported\n"
                    "   - Variant with conflicting evidence\n\n"
                    "8. CLASSIFICATION CRITERIA (ACMG/AMP):\n"
                    "   - Pathogenic: Very strong evidence of pathogenicity\n"
                    "   - Likely pathogenic: Strong evidence of pathogenicity\n"
                    "   - VUS: Insufficient evidence for benign or pathogenic\n"
                    "   - Likely benign: Strong evidence of benign\n"
                    "   - Benign: Very strong evidence of benign\n\n"
                    "9. WHAT TO DO:\n"
                    "   - Discuss with Clinical Genetics\n"
                    "   - Do NOT change clinical management\n"
                    "   - Continue family history-based management\n"
                    "   - Consider recontact in future if reclassified\n\n"
                    "Sources: ACMG/AMP Guidelines, BSGM, GeneReviews"
                ),
                confidence=0.95,
                metadata={
                    "category": "test_interpretation",
                    "result_type": "vus",
                    "clinical_action": "do_not_change_management",
                    "sources": ["ACMG/AMP Guidelines", "BSGM", "GeneReviews"]
                }
            )

        # Pathogenic variant
        elif any(term in query_lower for term in ["pathogenic", "mutation", "positive"]):
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "GENETIC TEST INTERPRETATION: Pathogenic/Likely Pathogenic Variant\n\n"
                    "A pathogenic or likely pathogenic variant is known or expected to cause disease:\n\n"
                    "1. WHAT IT MEANS:\n"
                    "   - Variant known to cause disorder (pathogenic)\n"
                    "   - Variant very likely to cause disorder (likely pathogenic)\n"
                    "   - Can be used for clinical decision-making\n"
                    "   - Actionable result\n\n"
                    "2. IMPLICATIONS:\n"
                    "   - Patient has (or will develop) genetic condition (if fully penetrant)\n"
                    "   - May have implications for management\n"
                    "   - May have implications for family members\n"
                    "   - May have reproductive implications\n\n"
                    "3. MANAGEMENT:\n"
                    "   - Condition-specific management based on result\n"
                    "   - May include:\n"
                    "     * Enhanced surveillance\n"
                    "     * Risk-reducing interventions\n"
                    "     * Medications\n"
                    "     * Lifestyle modifications\n"
                    "     * Referral to specialist\n\n"
                    "4. FAMILY IMPLICATIONS:\n"
                    "   - Cascade testing offered to at-risk relatives\n"
                    "   - Predictive testing for adult-onset conditions\n"
                    "   - Reproductive options for family members\n"
                    "   - Genetic counseling for relatives\n\n"
                    "5. EXAMPLES:\n"
                    "   - BRCA1 pathogenic variant: Hereditary breast/ovarian cancer\n"
                    "   - CFTR pathogenic variants (x2): Cystic fibrosis\n"
                    "   - FMR1 full mutation: Fragile X syndrome\n\n"
                    "6. PATIENT COMMUNICATION:\n"
                    "   - Explain result clearly\n"
                    "   - Discuss implications for patient and family\n"
                    "   - Discuss management options\n"
                    "   - Provide written information\n"
                    "   - Offer psychological support\n"
                    "   - Refer to condition-specific specialist\n\n"
                    "7. CONFIRMATION:\n"
                    "   - Some results may need confirmation (second sample)\n"
                    "   - Especially for unexpected or critical results\n\n"
                    "8. ACTION PLAN:\n"
                    "   - Discuss with Clinical Genetics/specialist\n"
                    "   - Develop management plan\n"
                    "   - Arrange cascade testing for family\n"
                    "   - Provide genetic counseling\n\n"
                    "Sources: ACMG/AMP Guidelines, BSGM, GeneReviews"
                ),
                confidence=0.95,
                metadata={
                    "category": "test_interpretation",
                    "result_type": "pathogenic",
                    "clinical_action": "actionable",
                    "sources": ["ACMG/AMP Guidelines", "BSGM", "GeneReviews"]
                }
            )

        # Benign variant
        elif any(term in query_lower for term in ["benign", "negative", "normal"]):
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "GENETIC TEST INTERPRETATION: Benign/Likely Benign Variant or Negative Result\n\n"
                    "A benign variant or negative result generally indicates no genetic cause found:\n\n"
                    "1. WHAT IT MEANS:\n"
                    "   - Benign/likely benign: Variant does not cause disease\n"
                    "   - Negative: No pathogenic variant found\n"
                    "   - Generally reassuring, but depends on context\n\n"
                    "2. INTERPRETATION:\n"
                    "   - No genetic explanation found for condition\n"
                    "   - Does NOT rule out genetic cause (limited testing, unknown genes)\n"
                    "   - May reduce (but not eliminate) recurrence risk\n\n"
                    "3. MANAGEMENT:\n"
                    "   - Continue clinical management based on phenotype\n"
                    "   - Family history still important\n"
                    "   - May still need surveillance (based on family history)\n\n"
                    "4. LIMITATIONS:\n"
                    "   - Test may not have covered all possible genes\n"
                    "   - Some genetic causes unknown\n"
                    "   - Some variants not detectable by current methods\n"
                    "   - Mosaicism may not be detected in tested tissue\n"
                    "   - Some variants in non-coding regions not detected\n\n"
                    "5. FALSE NEGATIVE RISK:\n"
                    "   - Higher with limited testing (single gene vs. panel vs. exome)\n"
                    "   - Higher with atypical presentation\n"
                    "   - Re-testing may be considered if:\n"
                    "     * New genes discovered\n"
                    "     * Testing technology improves\n"
                    "     * Clinical presentation changes\n\n"
                    "6. FAMILY IMPLICATIONS:\n"
                    "   - May reduce (but not eliminate) recurrence risk\n"
                    "   - Genetic counseling still helpful\n"
                    "   - Family history remains important\n\n"
                    "7. PATIENT COMMUNICATION:\n"
                    "   - Explain result and limitations\n"
                    "   - Discuss possibility of undiscovered genetic cause\n"
                    "   - Discuss that management unchanged\n"
                    "   - Discuss recurrence risk (reduced but not zero)\n"
                    "   - Discuss possibility of future re-testing\n\n"
                    "8. EXAMPLES:\n"
                    "   - Negative BRCA testing: No BRCA pathogenic variant found\n"
                    "   - Negative cystic fibrosis testing: No CFTR pathogenic variants\n"
                    "   - Negative WES: No pathogenic variant found in coding regions\n\n"
                    "9. RE-TESTING:\n"
                    "   - Consider if:\n"
                    "     * New genes discovered for condition\n"
                    "     * Testing methods improve\n"
                    "     * Clinical suspicion remains high\n"
                    "   - Discuss with Clinical Genetics\n\n"
                    "Sources: ACMG/AMP Guidelines, BSGM, GeneReviews"
                ),
                confidence=0.92,
                metadata={
                    "category": "test_interpretation",
                    "result_type": "benign_or_negative",
                    "clinical_action": "continue_clinical_management",
                    "sources": ["ACMG/AMP Guidelines", "BSGM", "GeneReviews"]
                }
            )

        # General test interpretation
        else:
            return DomainQueryResult(
                domain_name="medical_genetics",
                answer=(
                    "GENETIC TEST INTERPRETATION\n\n"
                    "Interpretation of genetic test results depends on the variant and clinical context:\n\n"
                    "1. VARIANT CLASSIFICATIONS (ACMG/AMP):\n"
                    "   - Pathogenic: Known to cause disease\n"
                    "   - Likely pathogenic: Very likely to cause disease\n"
                    "   - VUS (Uncertain significance): Unknown clinical significance\n"
                    "   - Likely benign: Very likely not disease-causing\n"
                    "   - Benign: Known not to cause disease\n\n"
                    "2. ACTIONABLE RESULTS:\n"
                    "   - Pathogenic/likely pathogenic: Use for clinical management\n"
                    "   - Benign/likely benign: Do not use for management (ignore)\n"
                    "   - VUS: Do NOT change management based on VUS\n\n"
                    "3. NEGATIVE RESULTS:\n"
                    "   - No pathogenic variant found\n"
                    "   - Does NOT rule out genetic cause\n"
                    "   - May need:\n"
                    "     * More comprehensive testing\n"
                    "     * Re-testing in future (new genes discovered)\n"
                    "     * Clinical diagnosis based on phenotype\n\n"
                    "4. FACTORS AFFECTING INTERPRETATION:\n"
                    "   - Patient's symptoms and family history\n"
                    "   - Gene involved (penetrance, variable expressivity)\n"
                    "   - Type of variant (missense, nonsense, splice, etc.)\n"
                    "   - Population frequency\n"
                    "   - Functional evidence\n"
                    "   - Segregation data\n\n"
                    "5. PENETRANCE AND EXPRESSIVITY:\n"
                    "   - Complete penetrance: All with mutation develop disease (Huntington)\n"
                    "   - Incomplete penetrance: Some with mutation do not develop disease\n"
                    "   - Variable expressivity: Severity varies among affected individuals\n\n"
                    "6. MOSAICISM:\n"
                    "   - Some cells have mutation, others do not\n"
                    "   - May not be detected in all tissues\n"
                    "   - May affect severity\n\n"
                    "7. INCIDENTAL FINDINGS:\n"
                    "   - Unexpected findings unrelated to testing indication\n"
                    "   - May have health implications\n"
                    "   - Laboratories have policies on reporting\n\n"
                    "8. FAMILY TESTING:\n"
                    "   - Cascade testing for pathogenic variants\n"
                    "   - Predictive testing for at-risk relatives\n"
                    "   - Do NOT test relatives for VUS\n\n"
                    "9. RECLASSIFICATION:\n"
                    "   - Variants may be reclassified as more data becomes available\n"
                    "   - Some laboratories offer reclassification notifications\n"
                    "   - VUS most likely to be reclassified\n\n"
                    "10. GENETIC COUNSELING:\n"
                    "   - Essential for result interpretation\n"
                    "   - Discuss implications for patient and family\n"
                    "   - Discuss management options\n"
                    "   - Provide psychological support\n\n"
                    "Discuss with Clinical Genetics for result interpretation.\n\n"
                    "Sources: ACMG/AMP Guidelines, BSGM, GeneReviews"
                ),
                confidence=0.90,
                metadata={
                    "category": "test_interpretation",
                    "sources": ["ACMG/AMP Guidelines", "BSGM", "GeneReviews"]
                }
            )

    def _handle_general_genetics_query(self, query: str, context: dict) -> DomainQueryResult:
        """Handle general genetics and genetic counseling queries"""
        return DomainQueryResult(
            domain_name="medical_genetics",
            answer=(
                "MEDICAL GENETICS: General Genetic Counseling\n\n"
                "Medical genetics provides evaluation, diagnosis, and counseling for genetic conditions:\n\n"
                "1. COMMON REASONS FOR GENETICS REFERRAL:\n"
                "   - Family history of genetic condition\n"
                "   - Child with developmental delay/intellectual disability\n"
                "   - Multiple pregnancy losses (miscarriages, stillbirths)\n"
                "   - Known or suspected genetic syndrome\n"
                "   - Prenatal genetic testing counseling\n"
                "   - Hereditary cancer risk assessment\n"
                "   - Adult-onset genetic disorder (e.g., Huntington)\n"
                "   - Carrier screening (before pregnancy)\n"
                "   - Consanguinity\n"
                "   - Abnormal newborn screening\n\n"
                "2. GENETIC COUNSELING PROCESS:\n"
                "   - Detailed family history (three-generation pedigree)\n"
                "   - Risk assessment (recurrence risk, carrier risk)\n"
                "   - Discussion of genetic testing options\n"
                "   - Pre-test counseling (benefits, limitations, risks)\n"
                "   - Coordination of genetic testing\n"
                "   - Post-test counseling (result interpretation, implications)\n"
                "   - Discussion of management options\n"
                "   - Psychological support\n"
                "   - Family communication facilitation\n\n"
                "3. GENETIC TESTING TYPES:\n"
                "   - Single-gene testing (specific disorder)\n"
                "   - Gene panels (multiple related genes)\n"
                "   - Whole exome sequencing (all coding regions)\n"
                "   - Whole genome sequencing (entire genome)\n"
                "   - Chromosomal microarray (deletions/duplications)\n"
                "   - Karyotype (chromosome number/structure)\n"
                "   - FISH (targeted testing)\n"
                "   - Biochemical testing (enzyme levels, metabolites)\n\n"
                "4. INHERITANCE PATTERNS:\n"
                "   - Autosomal dominant (50% risk to each child)\n"
                "   - Autosomal recessive (25% risk if both parents carriers)\n"
                "   - X-linked recessive (sons of carrier mothers affected)\n"
                "   - X-linked dominant (can affect males and females)\n"
                "   - Mitochondrial (maternal inheritance)\n"
                "   - Multifactorial (genetic + environmental factors)\n\n"
                "5. PRENATAL GENETIC SERVICES:\n"
                "   - Preconception counseling\n"
                "   - Carrier screening\n"
                "   - Prenatal diagnostic testing (CVS, amniocentesis)\n"
                "   - Prenatal screening (NIPT, combined test)\n"
                "   - Preimplantation genetic diagnosis (PGD)\n\n"
                "6. CANCER GENETICS:\n"
                "   - Hereditary cancer risk assessment\n"
                "   - BRCA1/BRCA2 testing\n"
                "   - Lynch syndrome testing\n"
                "   - Other hereditary cancer syndromes\n"
                "   - Enhanced surveillance recommendations\n"
                "   - Risk-reducing surgery options\n\n"
                "7. PEDIATRIC GENETICS:\n"
                "   - Developmental delay/intellectual disability evaluation\n"
                "   - Dysmorphology assessment\n"
                "   - Autism spectrum disorder genetics\n"
                "   - Rare disease diagnosis\n"
                "   - Metabolic disorder evaluation\n\n"
                "8. ADULT GENETICS:\n"
                "   - Predictive testing for adult-onset disorders\n"
                "   - Hereditary cancer risk\n"
                "   - Cardiovascular genetics\n"
                "   - Neurogenetic disorders\n\n"
                "9. ETHICAL AND LEGAL CONSIDERATIONS:\n"
                "   - Informed consent for testing\n"
                "   - Confidentiality and privacy\n"
                "   - Genetic discrimination protections\n"
                "   - Right not to know\n"
                "   - Testing of minors\n"
                "   - Reproductive options\n\n"
                "10. GENETIC CONDITIONS SEEN:\n"
                "   - Chromosomal disorders (Down syndrome, Turner, Klinefelter)\n"
                "   - Single-gene disorders (CF, Huntington, muscular dystrophy)\n"
                "   - Multifactorial disorders (diabetes, hypertension)\n"
                "   - Mitochondrial disorders\n"
                "   - Syndromes with genetic cause\n"
                "   - Birth defects\n"
                "   - Hereditary cancer syndromes\n"
                "   - Many others\n\n"
                "Refer to Clinical Genetics for comprehensive evaluation.\n\n"
                "Sources: ACMG Practice Guidelines, BSGM, GeneReviews"
            ),
            confidence=0.90,
            metadata={
                "category": "general_genetics",
                "sources": ["ACMG Practice Guidelines", "BSGM", "GeneReviews"]
            }
        )


def create_medical_genetics_domain():
    """Factory function for MedicalGeneticsDomain"""
    return MedicalGeneticsDomain()


# Domain metadata
DOMAIN_INFO = {
    "name": "Medical Genetics",
    "version": "1.0.0",
    "description": "Medical genetics, genetic counseling, inherited disorders, prenatal genetic testing, pharmacogenomics, cancer genetics",
    "author": "GPDISC",
    "specialty": "Genetics",
    "conditions": [
        "Down syndrome", "Turner syndrome", "Klinefelter syndrome",
        "Cystic fibrosis", "Huntington disease", "Muscular dystrophy",
        "Sickle cell disease", "Thalassemia", "Fragile X syndrome",
        "BRCA-related hereditary breast/ovarian cancer",
        "Lynch syndrome", "Mitochondrial disorders",
        "Many others"
    ],
    "capabilities": [
        "genetic_counseling", "inheritance_risk_assessment", "carrier_screening",
        "prenatal_genetic_testing_guidance", "cancer_genetics_assessment",
        "pharmacogenomics_consultation", "pediatric_genetics_evaluation",
        "adult_onset_genetic_testing", "genetic_test_interpretation",
        "family_history_analysis", "variant_interpretation"
    ],
    "evidence_base": [
        "ACMG Practice Guidelines",
        "British Society for Genetic Medicine (BSGM)",
        "NICE Guidelines",
        "GeneReviews (NIH)",
        "American College of Medical Genetics and Genomics"
    ]
}


__all__ = ["MedicalGeneticsDomain", "create_medical_genetics_domain", "DOMAIN_INFO"]
