# GPDISC Patient Data Directory

## Purpose

This directory stores all patient medical records and clinical data for the GPDISC system.

## Privacy and Security

⚠️ **IMPORTANT PRIVACY NOTICE**

- This directory contains REAL PATIENT MEDICAL DATA
- All data is stored LOCALLY only - no external transmission
- Protected Health Information (PHI) is stored here
- Ensure appropriate access controls and encryption
- NEVER commit patient data to version control

## Directory Structure

```
patients/
├── README.md                    # This file
├── .gitignore                   # Ensures patient data is not committed to git
├── patient_[hash].json         # Individual patient records
└── [future: encrypted/]        # Encrypted patient data (future feature)
```

## Patient Record Files

Each patient is stored as a JSON file:
- Filename: `patient_[hash].json` where hash is a privacy-preserving identifier
- Format: JSON containing all patient records (demographics, labs, ECG, imaging, medications, allergies, diagnoses, notes)
- Privacy: Patient ID is hashed for confidentiality

## Record Types

1. **Demographics** - Patient identification information
2. **Blood Tests** - Laboratory results with reference ranges
3. **ECG Records** - Electrocardiogram interpretations
4. **Imaging Reports** - Radiology and imaging reports
5. **Medications** - Current and past medications
6. **Allergies** - Drug, food, and environmental allergies
7. **Diagnoses** - ICD-10 coded diagnoses
8. **Clinical Notes** - Consultation and progress notes

## Access and Security

### Recommended Security Practices

1. **File System Permissions**
   - Restrict access to authorized personnel only
   - Use appropriate user/group permissions
   - Consider encrypting the entire directory

2. **Backup**
   - Regular encrypted backups
   - Secure backup storage location
   - Test restoration procedures

3. **Audit Trail**
   - Log access to patient records
   - Track who accessed what and when
   - Monitor for unauthorized access

4. **Data Retention**
   - Follow local regulations for medical record retention
   - Secure deletion when records expire
   - Maintain deletion logs

### Encryption (Future Feature)

Future versions will support:
- Individual file encryption
- AES-256 encryption at rest
- Encrypted folder structure
- Key management system

## Integration with GPDISC

The patient record system is integrated with:
- Medical consultation domains
- Drug interaction checker
- DICOM processor (for imaging)
- Clinical decision support

## Compliance

This storage system is designed to support:
- **HIPAA** (Health Insurance Portability and Accountability Act)
- **GDPR** (General Data Protection Regulation)
- **UK Data Protection Act**
- Local medical record storage regulations

## Maintenance

### Regular Tasks

1. Review access logs
2. Verify backup integrity
3. Check for unusual access patterns
4. Update security protocols as needed
5. Audit data retention compliance

### Troubleshooting

**Problem**: Cannot access patient records
**Solution**: Check file permissions and user access rights

**Problem**: Records not persisting
**Solution**: Verify disk space and write permissions

**Problem**: Slow performance
**Solution**: Consider archive strategy for old records

## Contact

For issues or questions about patient data storage:
- Review GPDISC documentation in User_Manual/
- Check system logs for error messages
- Consult IT security for access issues

---

**© 2026 GPDISC - General Practice Discovery and Intelligence System for Consultation**

**Privacy Commitment**: All patient data stored locally - no external transmission
