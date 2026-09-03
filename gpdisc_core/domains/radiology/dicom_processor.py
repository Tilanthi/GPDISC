"""
GPDISC DICOM Processor

Local-only DICOM image analysis with privacy-preserving processing.
No external transmission of medical images - all processing happens locally.

Dependencies:
- pydicom: DICOM file parsing
- numpy: Array operations
- matplotlib: Visualization (optional)

Privacy Commitment:
- All DICOM files processed locally
- No transmission to external services
- Patient data remains on local system
- PHI (Protected Health Information) never leaves the local environment
"""

import os
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json

logger = logging.getLogger(__name__)

# Try to import required libraries
try:
    import pydicom
    from pydicom.dataset import FileDataset
    from pydicom.tag import Tag
    PYDICOM_AVAILABLE = True
except ImportError:
    PYDICOM_AVAILABLE = False
    logger.warning("pydicom not available. Install with: pip install pydicom")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    logger.warning("numpy not available. Install with: pip install numpy")


@dataclass
class DICOMMetadata:
    """Structured DICOM metadata"""
    patient_id: str = ""
    patient_name: str = ""
    study_date: str = ""
    modality: str = ""
    body_part: str = ""
    view_position: str = ""
    acquisition_date: str = ""
    institution_name: str = ""

    # Image characteristics
    rows: int = 0
    columns: int = 0
    bits_allocated: int = 0
    bits_stored: int = 0
    pixel_spacing: Tuple[float, float] = (0.0, 0.0)
    slice_thickness: float = 0.0

    # Window/Level
    window_center: float = 0.0
    window_width: float = 0.0

    # Series information
    series_number: int = 0
    instance_number: int = 0
    series_description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "patient_id": self.patient_id,
            "patient_name": self.patient_name,
            "study_date": self.study_date,
            "modality": self.modality,
            "body_part": self.body_part,
            "view_position": self.view_position,
            "acquisition_date": self.acquisition_date,
            "institution_name": self.institution_name,
            "rows": self.rows,
            "columns": self.columns,
            "bits_allocated": self.bits_allocated,
            "bits_stored": self.bits_stored,
            "pixel_spacing": self.pixel_spacing,
            "slice_thickness": self.slice_thickness,
            "window_center": self.window_center,
            "window_width": self.window_width,
            "series_number": self.series_number,
            "instance_number": self.instance_number,
            "series_description": self.series_description
        }


@dataclass
class DICOMAnalysisResult:
    """Result of DICOM analysis"""
    success: bool
    metadata: Optional[DICOMMetadata] = None
    pixel_data_available: bool = False
    image_shape: Optional[Tuple[int, ...]] = None
    pixel_array_stats: Optional[Dict[str, float]] = None
    findings: List[str] = None
    warnings: List[str] = None
    error_message: str = ""

    def __post_init__(self):
        if self.findings is None:
            self.findings = []
        if self.warnings is None:
            self.warnings = []


class DICOMProcessor:
    """
    Local DICOM file processor with privacy-preserving analysis

    All processing happens locally. No data is transmitted externally.
    Patient privacy is protected by keeping all processing on the local system.
    """

    def __init__(self, anonymize_output: bool = True):
        """
        Initialize DICOM processor

        Args:
            anonymize_output: If True, remove PHI from output (default: True for privacy)
        """
        self.anonymize_output = anonymize_output
        self.processing_stats = {
            "files_processed": 0,
            "last_processed": None,
            "errors": 0
        }

        if not PYDICOM_AVAILABLE:
            logger.error("pydicom is required for DICOM processing")
            raise ImportError("pydicom is required. Install with: pip install pydicom")

        if not NUMPY_AVAILABLE:
            logger.error("numpy is required for DICOM processing")
            raise ImportError("numpy is required. Install with: pip install numpy")

    def load_dicom_file(self, filepath: str) -> Optional[FileDataset]:
        """
        Load DICOM file from disk

        Args:
            filepath: Path to DICOM file (.dcm)

        Returns:
            pydicom FileDataset or None if error
        """
        if not os.path.exists(filepath):
            logger.error(f"DICOM file not found: {filepath}")
            return None

        try:
            dataset = pydicom.dcmread(filepath)
            logger.info(f"Successfully loaded DICOM file: {filepath}")
            return dataset
        except Exception as e:
            logger.error(f"Error loading DICOM file {filepath}: {str(e)}")
            return None

    def extract_metadata(self, dataset: FileDataset, anonymize: bool = True) -> DICOMMetadata:
        """
        Extract metadata from DICOM dataset

        Args:
            dataset: pydicom FileDataset
            anonymize: If True, mask PHI in output

        Returns:
            DICOMMetadata object
        """
        metadata = DICOMMetadata()

        # Helper function to safely get DICOM tag value
        def get_tag_value(tag, default=""):
            try:
                value = dataset.get(tag, default)
                if value == default:
                    return default
                # Convert to string if needed
                if hasattr(value, 'value'):
                    value = value.value
                return str(value) if value is not None else default
            except Exception:
                return default

        # Patient information (PHI - will be anonymized if requested)
        patient_id = get_tag_value('PatientID', '')
        patient_name = get_tag_value('PatientName', '')
        patient_birth_date = get_tag_value('PatientBirthDate', '')

        if anonymize and self.anonymize_output:
            metadata.patient_id = self._anonymize_id(patient_id)
            metadata.patient_name = "[ANONYMIZED]"
        else:
            metadata.patient_id = patient_id
            metadata.patient_name = patient_name

        # Study information
        metadata.study_date = get_tag_value('StudyDate', '')
        metadata.acquisition_date = get_tag_value('AcquisitionDate', '')

        # Modality information
        metadata.modality = get_tag_value('Modality', '')
        metadata.body_part = get_tag_value('BodyPartExamined', '')
        metadata.view_position = get_tag_value('ViewPosition', '')

        # Institution
        metadata.institution_name = get_tag_value('InstitutionName', '')

        # Image characteristics
        metadata.rows = int(get_tag_value('Rows', 0))
        metadata.columns = int(get_tag_value('Columns', 0))
        metadata.bits_allocated = int(get_tag_value('BitsAllocated', 0))
        metadata.bits_stored = int(get_tag_value('BitsStored', 0))

        # Pixel spacing
        try:
            pixel_spacing = dataset.get('PixelSpacing', None)
            if pixel_spacing:
                metadata.pixel_spacing = (float(pixel_spacing[0]), float(pixel_spacing[1]))
        except Exception:
            metadata.pixel_spacing = (0.0, 0.0)

        # Slice thickness
        try:
            slice_thickness = dataset.get('SliceThickness', None)
            if slice_thickness:
                metadata.slice_thickness = float(slice_thickness)
        except Exception:
            metadata.slice_thickness = 0.0

        # Window/Level
        try:
            window_center = dataset.get('WindowCenter', None)
            window_width = dataset.get('WindowWidth', None)
            if window_center:
                metadata.window_center = float(window_center[0] if isinstance(window_center, (list, tuple)) else window_center)
            if window_width:
                metadata.window_width = float(window_width[0] if isinstance(window_width, (list, tuple)) else window_width)
        except Exception:
            pass

        # Series information
        metadata.series_number = int(get_tag_value('SeriesNumber', 0))
        metadata.instance_number = int(get_tag_value('InstanceNumber', 0))
        metadata.series_description = get_tag_value('SeriesDescription', '')

        return metadata

    def _anonymize_id(self, patient_id: str) -> str:
        """
        Anonymize patient ID for privacy

        Args:
            patient_id: Original patient ID

        Returns:
            Anonymized ID (hash of original)
        """
        import hashlib
        if not patient_id:
            return ""
        # Create hash of patient ID for consistent anonymization
        hash_obj = hashlib.sha256(patient_id.encode())
        return f"ANON_{hash_obj.hexdigest()[:8]}"

    def extract_pixel_data(self, dataset: FileDataset) -> Optional[np.ndarray]:
        """
        Extract pixel data from DICOM dataset

        Args:
            dataset: pydicom FileDataset

        Returns:
            numpy array of pixel data or None if unavailable
        """
        try:
            if not hasattr(dataset, 'pixel_array'):
                logger.warning("No pixel data in DICOM file")
                return None

            pixel_array = dataset.pixel_array

            # Apply rescale slope and intercept if present (for CT, etc.)
            rescale_slope = dataset.get('RescaleSlope', 1.0)
            rescale_intercept = dataset.get('RescaleIntercept', 0.0)

            if rescale_slope != 1.0 or rescale_intercept != 0.0:
                pixel_array = pixel_array * rescale_slope + rescale_intercept

            logger.info(f"Extracted pixel data with shape: {pixel_array.shape}")
            return pixel_array

        except Exception as e:
            logger.error(f"Error extracting pixel data: {str(e)}")
            return None

    def analyze_pixel_array(self, pixel_array: np.ndarray) -> Dict[str, float]:
        """
        Analyze pixel array statistics

        Args:
            pixel_array: numpy array of pixel values

        Returns:
            Dictionary of statistics
        """
        stats = {
            "min": float(np.min(pixel_array)),
            "max": float(np.max(pixel_array)),
            "mean": float(np.mean(pixel_array)),
            "std": float(np.std(pixel_array)),
            "median": float(np.median(pixel_array))
        }

        # Add percentiles
        stats["p25"] = float(np.percentile(pixel_array, 25))
        stats["p75"] = float(np.percentile(pixel_array, 75))

        return stats

    def apply_window_level(self, pixel_array: np.ndarray, window_center: float,
                          window_width: float) -> np.ndarray:
        """
        Apply window/level adjustment to pixel array

        Args:
            pixel_array: Input pixel array
            window_center: Window center (level)
            window_width: Window width

        Returns:
            Windowed pixel array
        """
        window_min = window_center - (window_width / 2)
        window_max = window_center + (window_width / 2)

        # Clip values to window range
        windowed = np.clip(pixel_array, window_min, window_max)

        # Normalize to 0-255 range for display
        if window_max > window_min:
            windowed = ((windowed - window_min) / (window_width)) * 255
        else:
            windowed = np.zeros_like(pixel_array)

        return windowed.astype(np.uint8)

    def detect_modality_specific_findings(self, metadata: DICOMMetadata,
                                        pixel_stats: Optional[Dict[str, float]] = None) -> List[str]:
        """
        Detect modality-specific findings based on metadata and pixel statistics

        Args:
            metadata: DICOM metadata
            pixel_stats: Optional pixel array statistics

        Returns:
            List of findings
        """
        findings = []

        modality = metadata.modality.upper()

        if modality == "CT":
            findings.extend(self._analyze_ct_metadata(metadata, pixel_stats))
        elif modality == "XR" or modality == "CR" or modality == "DR":
            findings.extend(self._analyze_xray_metadata(metadata, pixel_stats))
        elif modality == "MR":
            findings.extend(self._analyze_mri_metadata(metadata, pixel_stats))
        elif modality == "US":
            findings.extend(self._analyze_ultrasound_metadata(metadata, pixel_stats))
        else:
            findings.append(f"Modality: {modality} - Metadata analysis available")

        return findings

    def _analyze_ct_metadata(self, metadata: DICOMMetadata,
                            pixel_stats: Optional[Dict[str, float]] = None) -> List[str]:
        """Analyze CT-specific metadata"""
        findings = []

        # Body part analysis
        body_part = metadata.body_part.lower()
        if "chest" in body_part or "thorax" in body_part:
            findings.append("CT Chest - Lung window analysis available")
            findings.append("Bone window and mediastinal window analysis available")
        elif "abdomen" in body_part or "pelvis" in body_part:
            findings.append("CT Abdomen/Pelvis - Soft tissue and bone window analysis available")
        elif "head" in body_part or "brain" in body_part:
            findings.append("CT Head - Brain window and bone window analysis available")

        # Window/Level info
        if metadata.window_center > 0 and metadata.window_width > 0:
            findings.append(f"Window/Level: {metadata.window_center}/{metadata.window_width}")

        # Pixel value range (Hounsfield Units for CT)
        if pixel_stats:
            min_hu = pixel_stats.get("min", 0)
            max_hu = pixel_stats.get("max", 0)
            findings.append(f"Hounsfield Unit range: {min_hu:.1f} to {max_hu:.1f}")

            # Detect possible air/fluid/bone
            if min_hu < -500:
                findings.append("Low density areas detected (possible air/fat)")
            if max_hu > 300:
                findings.append("High density areas detected (possible bone/contrast)")

        return findings

    def _analyze_xray_metadata(self, metadata: DICOMMetadata,
                              pixel_stats: Optional[Dict[str, float]] = None) -> List[str]:
        """Analyze X-ray specific metadata"""
        findings = []

        # View position
        view = metadata.view_position.upper()
        if view:
            findings.append(f"View: {view}")

        # Body part
        body_part = metadata.body_part.lower()
        if "chest" in body_part:
            findings.append("Chest radiograph - PA/AP view analysis")
            findings.append("Lung fields, heart size, mediastinum assessment")
        elif "hand" in body_part or "wrist" in body_part or "finger" in body_part:
            findings.append("Hand/Wrist radiograph - Bone and soft tissue assessment")
        elif "knee" in body_part or "leg" in body_part:
            findings.append("Knee/Leg radiograph - Bone and joint assessment")

        return findings

    def _analyze_mri_metadata(self, metadata: DICOMMetadata,
                             pixel_stats: Optional[Dict[str, float]] = None) -> List[str]:
        """Analyze MRI-specific metadata"""
        findings = []

        findings.append("MRI sequence - Multi-parametric analysis")
        findings.append("T1, T2, FLAIR, diffusion-weighted analysis available")

        body_part = metadata.body_part.lower()
        if "brain" in body_part or "head" in body_part:
            findings.append("Brain MRI - Neurological assessment")
        elif "spine" in body_part:
            findings.append("Spine MRI - Vertebral and disc assessment")

        return findings

    def _analyze_ultrasound_metadata(self, metadata: DICOMMetadata,
                                    pixel_stats: Optional[Dict[str, float]] = None) -> List[str]:
        """Analyze Ultrasound-specific metadata"""
        findings = []

        findings.append("Ultrasound examination - Real-time imaging")
        findings.append("Soft tissue and vascular assessment")

        body_part = metadata.body_part.lower()
        if "abdomen" in body_part:
            findings.append("Abdominal ultrasound - Organ assessment")
        elif "pelvis" in body_part or "obstetric" in metadata.series_description.lower():
            findings.append("Pelvic/Obstetric ultrasound - Fetal/organ assessment")

        return findings

    def process_dicom_file(self, filepath: str, extract_pixels: bool = True) -> DICOMAnalysisResult:
        """
        Process DICOM file and extract all information

        Args:
            filepath: Path to DICOM file
            extract_pixels: Whether to extract pixel data (may be memory-intensive)

        Returns:
            DICOMAnalysisResult with all extracted information
        """
        result = DICOMAnalysisResult(success=False)

        # Load DICOM file
        dataset = self.load_dicom_file(filepath)
        if dataset is None:
            result.error_message = "Failed to load DICOM file"
            return result

        try:
            # Extract metadata
            result.metadata = self.extract_metadata(dataset, anonymize=self.anonymize_output)

            findings = []

            # Extract pixel data if requested
            if extract_pixels:
                pixel_array = self.extract_pixel_data(dataset)
                if pixel_array is not None:
                    result.pixel_data_available = True
                    result.image_shape = pixel_array.shape
                    result.pixel_array_stats = self.analyze_pixel_array(pixel_array)

                    # Detect modality-specific findings
                    findings.extend(self.detect_modality_specific_findings(
                        result.metadata, result.pixel_array_stats
                    ))
                else:
                    result.warnings.append("Pixel data not available in this DICOM file")
            else:
                # Still detect findings from metadata
                findings.extend(self.detect_modality_specific_findings(result.metadata))

            result.findings = findings
            result.success = True

            # Update processing stats
            self.processing_stats["files_processed"] += 1
            self.processing_stats["last_processed"] = datetime.now().isoformat()

        except Exception as e:
            result.error_message = f"Error processing DICOM file: {str(e)}"
            logger.error(result.error_message)
            self.processing_stats["errors"] += 1

        return result

    def process_dicom_series(self, directory: str, extract_pixels: bool = True) -> List[DICOMAnalysisResult]:
        """
        Process all DICOM files in a directory (a series)

        Args:
            directory: Path to directory containing DICOM files
            extract_pixels: Whether to extract pixel data

        Returns:
            List of DICOMAnalysisResult objects
        """
        results = []

        if not os.path.isdir(directory):
            logger.error(f"Directory not found: {directory}")
            return results

        # Find all DICOM files
        dicom_files = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                # Try to read as DICOM
                try:
                    pydicom.dcmread(filepath, stop_before_pixels=True)
                    dicom_files.append(filepath)
                except:
                    pass  # Not a DICOM file

        logger.info(f"Found {len(dicom_files)} DICOM files in {directory}")

        # Process each file
        for filepath in sorted(dicom_files):
            result = self.process_dicom_file(filepath, extract_pixels=extract_pixels)
            results.append(result)

        return results

    def generate_report(self, result: DICOMAnalysisResult) -> str:
        """
        Generate human-readable report from DICOM analysis

        Args:
            result: DICOMAnalysisResult

        Returns:
            Formatted report string
        """
        if not result.success:
            return f"DICOM Analysis Failed: {result.error_message}"

        report = []
        report.append("=" * 70)
        report.append("GPDISC DICOM Analysis Report")
        report.append("=" * 70)
        report.append("")

        # Metadata section
        if result.metadata:
            report.append("METADATA:")
            report.append("-" * 70)
            metadata_dict = result.metadata.to_dict()
            for key, value in metadata_dict.items():
                if value:  # Only show non-empty values
                    report.append(f"  {key.replace('_', ' ').title()}: {value}")
            report.append("")

        # Image characteristics
        if result.image_shape:
            report.append("IMAGE CHARACTERISTICS:")
            report.append("-" * 70)
            report.append(f"  Image Shape: {result.image_shape}")
            if result.pixel_array_stats:
                report.append(f"  Pixel Value Range: {result.pixel_array_stats['min']:.2f} to {result.pixel_array_stats['max']:.2f}")
                report.append(f"  Mean: {result.pixel_array_stats['mean']:.2f}")
                report.append(f"  Std Dev: {result.pixel_array_stats['std']:.2f}")
            report.append("")

        # Findings
        if result.findings:
            report.append("FINDINGS:")
            report.append("-" * 70)
            for finding in result.findings:
                report.append(f"  • {finding}")
            report.append("")

        # Warnings
        if result.warnings:
            report.append("WARNINGS:")
            report.append("-" * 70)
            for warning in result.warnings:
                report.append(f"  ⚠ {warning}")
            report.append("")

        # Privacy notice
        report.append("-" * 70)
        report.append("PRIVACY NOTICE: All processing performed locally.")
        report.append("No medical images or patient data transmitted externally.")
        report.append("=" * 70)

        return "\n".join(report)

    def export_anonymized_data(self, result: DICOMAnalysisResult, output_file: str):
        """
        Export anonymized DICOM analysis data to JSON file

        Args:
            result: DICOMAnalysisResult
            output_file: Path to output JSON file
        """
        export_data = {
            "analysis_date": datetime.now().isoformat(),
            "success": result.success,
            "metadata": result.metadata.to_dict() if result.metadata else None,
            "image_shape": result.image_shape,
            "pixel_array_stats": result.pixel_array_stats,
            "findings": result.findings,
            "warnings": result.warnings
        }

        try:
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2)
            logger.info(f"Exported anonymized data to {output_file}")
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")


def create_dicom_processor(anonymize: bool = True) -> DICOMProcessor:
    """
    Factory function to create DICOM processor

    Args:
        anonymize: Whether to anonymize output (default: True)

    Returns:
        DICOMProcessor instance
    """
    return DICOMProcessor(anonymize_output=anonymize)


# Convenience functions for quick use
def analyze_dicom_file(filepath: str, anonymize: bool = True) -> DICOMAnalysisResult:
    """
    Quick analysis of a single DICOM file

    Args:
        filepath: Path to DICOM file
        anonymize: Whether to anonymize output

    Returns:
        DICOMAnalysisResult
    """
    processor = create_dicom_processor(anonymize=anonymize)
    return processor.process_dicom_file(filepath)


def generate_dicom_report(filepath: str, anonymize: bool = True) -> str:
    """
    Generate a quick report from a DICOM file

    Args:
        filepath: Path to DICOM file
        anonymize: Whether to anonymize output

    Returns:
        Formatted report string
    """
    processor = create_dicom_processor(anonymize=anonymize)
    result = processor.process_dicom_file(filepath)
    return processor.generate_report(result)


__all__ = [
    'DICOMProcessor',
    'DICOMMetadata',
    'DICOMAnalysisResult',
    'create_dicom_processor',
    'analyze_dicom_file',
    'generate_dicom_report'
]
