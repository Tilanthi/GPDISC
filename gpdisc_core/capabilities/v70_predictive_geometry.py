"""V70 Predictive Information Geometry - Information manifold learning"""
from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
import numpy as np


class ManifoldType(Enum):
    EUCLIDEAN = "euclidean"
    HYPERBOLIC = "hyperbolic"
    SPHERICAL = "spherical"


class DataModality(Enum):
    TEXT = "text"
    IMAGE = "image"
    NUMERICAL = "numerical"


class DistanceMetric(Enum):
    EUCLIDEAN = "euclidean"
    KL_DIVERGENCE = "kl_divergence"
    WASSERSTEIN = "wasserstein"


# Alias for compatibility with __init__.py imports
InformationMetric = DistanceMetric


@dataclass
class InformationPoint:
    data: np.ndarray
    modality: DataModality
    label: Optional[str] = None


@dataclass
class ManifoldRegion:
    center: np.ndarray
    radius: float
    points: List[InformationPoint] = field(default_factory=list)


@dataclass
class GeodesicPath:
    start: InformationPoint
    end: InformationPoint
    path: List[np.ndarray]


@dataclass
class PredictiveRelation:
    source: str
    target: str
    information_gain: float


class InformationManifold:
    def __init__(self, manifold_type: ManifoldType = ManifoldType.EUCLIDEAN):
        self.manifold_type = manifold_type
        self.points: List[InformationPoint] = []
        self.regions: List[ManifoldRegion] = []


class CrossModalPredictor:
    def predict(self, source: InformationPoint, target_modality: DataModality) -> InformationPoint:
        return InformationPoint(data=np.array([]), modality=target_modality)


class InformationCompressor:
    def compress(self, points: List[InformationPoint]) -> List[InformationPoint]:
        return points[:len(points)//2]


class PredictiveInformationGeometry:
    def __init__(self):
        self.manifold = InformationManifold()
        self.predictor = CrossModalPredictor()
        self.compressor = InformationCompressor()


def create_predictive_geometry():
    return PredictiveInformationGeometry()

def create_information_manifold(manifold_type: ManifoldType = ManifoldType.EUCLIDEAN):
    return InformationManifold(manifold_type)


__all__ = ['ManifoldType', 'DataModality', 'DistanceMetric', 'InformationMetric', 'InformationPoint',
           'ManifoldRegion', 'GeodesicPath', 'PredictiveRelation', 'InformationManifold',
           'CrossModalPredictor', 'InformationCompressor', 'PredictiveInformationGeometry',
           'create_predictive_geometry', 'create_information_manifold']
