r"""
HEXAD CHRONOS: Time-Series Numerical Forecasting & Crisis Anticipation Engine.
Inspired by Google Research TimesFM (Time Series Foundation Model, 2024) and Autoregressive Trend Projection.

Mathematical Foundations:
1. Autoregressive State Transition:
   \hat{y}_{t+h} = \sum_{k=0}^{K-1} \alpha_k y_{t-k} + \beta \cdot \text{Trend}(t)
2. Time-To-Criticality (TTC):
   TTC = \min \{ h \in [1, H] \mid \hat{y}_{t+h} \ge \Theta_{\text{critical}} \}
3. Operational Health Index (OHI):
   OHI(t) = \exp( - ( w_{\text{cpu}} \hat{u}_{\text{cpu}} + w_{\text{ram}} \hat{u}_{\text{ram}} + w_{\text{err}} \hat{\lambda}_{\text{err}} ) )
"""

import math
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class ForecastHorizonResult:
    metric_name: str
    historical_points: int
    forecast_values: List[float]
    time_to_criticality_steps: Optional[int]
    status: str
    critical_threshold: float
    confidence_interval: Tuple[float, float]


@dataclass
class ChronosHealthVerdict:
    healthy: bool
    operational_health_index: float
    time_to_saturation_steps: Optional[int]
    primary_warning: Optional[str]
    forecasts: Dict[str, ForecastHorizonResult]


class ChronosEngine:
    """
    Motore CHRONOS: Previsione Numerica Temporale e Meteo di Sistema.
    Monitora le serie temporali dei parametri di CORIS e LUNAR, predicendo saturazioni e crash.
    """

    DEFAULT_THRESHOLDS = {
        "ram_used_pct": 90.0,
        "cpu_load_pct": 92.0,
        "metabolic_pressure": 0.85,
        "error_frequency": 3.0,
        "token_velocity": 120.0
    }

    def __init__(self, history_window: int = 20, default_horizon: int = 5):
        self.history_window = history_window
        self.default_horizon = default_horizon
        self.series_store: Dict[str, List[float]] = {
            "ram_used_pct": [],
            "cpu_load_pct": [],
            "metabolic_pressure": [],
            "error_frequency": [],
            "token_velocity": []
        }

    def record_telemetry_point(self, telemetry: Dict[str, float]):
        """Registra un punto campionario nella serie temporale storica."""
        for metric, val in telemetry.items():
            if metric not in self.series_store:
                self.series_store[metric] = []
            self.series_store[metric].append(float(val))
            if len(self.series_store[metric]) > self.history_window * 2:
                self.series_store[metric].pop(0)

    def _forecast_linear_momentum(
        self,
        series: List[float],
        horizon: int,
        threshold: float
    ) -> ForecastHorizonResult:
        """Calcola la proiezione a momento e derivata prima (compatibile TimesFM zero-shot)."""
        if not series:
            return ForecastHorizonResult(
                metric_name="unknown",
                historical_points=0,
                forecast_values=[0.0] * horizon,
                time_to_criticality_steps=None,
                status="NO_DATA",
                critical_threshold=threshold,
                confidence_interval=(0.0, 0.0)
            )

        n = len(series)
        last_val = series[-1]

        if n == 1:
            forecasts = [round(last_val, 2)] * horizon
            trend = 0.0
        else:
            # Calcolo del gradiente medio sugli ultimi campioni
            k = min(n, 5)
            recent = series[-k:]
            deltas = [recent[i] - recent[i - 1] for i in range(1, len(recent))]
            avg_delta = sum(deltas) / len(deltas)
            # Smorzamento esponenziale del trend futuro (decay del momentum)
            forecasts = []
            cur = last_val
            for step in range(1, horizon + 1):
                cur += avg_delta * (0.85 ** (step - 1))
                forecasts.append(round(max(0.0, cur), 2))

        # Calcolo del Time-To-Criticality (TTC)
        ttc = None
        for step_idx, f_val in enumerate(forecasts, 1):
            if f_val >= threshold:
                ttc = step_idx
                break

        status = "CRITICAL" if (ttc is not None and ttc <= 2) else ("WARNING" if ttc is not None else "STABLE")
        variance = 0.05 * last_val
        conf_int = (round(max(0.0, last_val - variance), 2), round(last_val + variance, 2))

        return ForecastHorizonResult(
            metric_name="",
            historical_points=n,
            forecast_values=forecasts,
            time_to_criticality_steps=ttc,
            status=status,
            critical_threshold=threshold,
            confidence_interval=conf_int
        )

    def forecast_system_trajectory(
        self,
        current_telemetry: Optional[Dict[str, float]] = None,
        horizon: Optional[int] = None
    ) -> ChronosHealthVerdict:
        """
        Prevede l'andamento del sistema nei prossimi H passi.
        Ritorna l'Indice di Salute Operativa (OHI) e avvisi precoci.
        """
        h = horizon or self.default_horizon
        if current_telemetry:
            self.record_telemetry_point(current_telemetry)

        forecasts: Dict[str, ForecastHorizonResult] = {}
        min_ttc: Optional[int] = None
        warning_msg: Optional[str] = None
        penalty_sum = 0.0

        for metric, threshold in self.DEFAULT_THRESHOLDS.items():
            vals = self.series_store.get(metric, [])
            res = self._forecast_linear_momentum(vals, h, threshold)
            res.metric_name = metric
            forecasts[metric] = res

            # Controlla Time-To-Criticality
            if res.time_to_criticality_steps is not None:
                if min_ttc is None or res.time_to_criticality_steps < min_ttc:
                    min_ttc = res.time_to_criticality_steps
                    warning_msg = (
                        f"Allerta imminente: '{metric}' supererà la soglia critica ({threshold}) "
                        f"entro {res.time_to_criticality_steps} passi operativi."
                    )

            # Contributo al decadimento della salute operativa
            if res.forecast_values:
                ratio = res.forecast_values[-1] / max(1.0, threshold)
                penalty_sum += max(0.0, ratio - 0.70)

        # Calcolo Operational Health Index (OHI) in [0.0, 1.0]
        ohi = round(math.exp(-0.8 * penalty_sum), 3)
        healthy = ohi >= 0.70 and (min_ttc is None or min_ttc > 2)

        return ChronosHealthVerdict(
            healthy=healthy,
            operational_health_index=ohi,
            time_to_saturation_steps=min_ttc,
            primary_warning=warning_msg,
            forecasts=forecasts
        )


# Singleton esportato
chronos = ChronosEngine()
