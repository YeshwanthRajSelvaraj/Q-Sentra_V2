"""PQC Scorer using ML model."""
import json
import os
try:
    import joblib # to load xgboost
    import xgboost as xgb
    import shap
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

from .feature_extractor import extract_features

class PQCScorer:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), "pqc_scorer_v1.pkl")
        self.model = None
        self.explainer = None
        if ML_AVAILABLE and os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                self.explainer = shap.TreeExplainer(self.model)
            except Exception:
                pass
        
    def _rule_based_score(self, features: dict) -> dict:
        """Fallback scoring using simple rules."""
        score = 80
        reasons = []

        if features.get("key_size", 2048) <= 2048 and features.get("pk_rsa", 0):
            score = 30
            reasons.append({"feature": "key_size", "contribution": -50, "desc": "Uses RSA-2048 or less for key exchange (vulnerable to quantum attack)"})
        elif features.get("pk_rsa", 0) and features.get("key_size", 2048) >= 4096:
            score = 60
            reasons.append({"feature": "key_size", "contribution": -20, "desc": "Uses RSA-4096 (better but not quantum resistant)"})
        elif features.get("pk_ecdsa", 0):
            score = 60
            reasons.append({"feature": "pk_ecdsa", "contribution": -20, "desc": "Uses ECDSA which is vulnerable to Shor's algorithm"})
            
        if features.get("supports_pqc", 0):
            score = 95
            reasons.append({"feature": "supports_pqc", "contribution": 35, "desc": "Implements Post-Quantum algorithms"})
            
        if features.get("uses_weak_signature", 0):
            score -= 20
            reasons.append({"feature": "uses_weak_signature", "contribution": -20, "desc": "Certificate uses SHA-1 or MD5 signature (deprecated)"})
            
        if features.get("tls_1_3", 0):
            reasons.append({"feature": "tls_1_3", "contribution": 15, "desc": "Supports TLS 1.3 with strong ciphers"})

        return {
            "score": max(0, min(100, score)),
            "confidence": 0.6 if not ML_AVAILABLE else 0.4,
            "model_version": "v1-rules",
            "explanations": sorted(reasons, key=lambda x: abs(x["contribution"]), reverse=True)[:3]
        }

    def score(self, cbom_json: dict) -> dict:
        features = extract_features(cbom_json)
        
        if not self.model:
            return self._rule_based_score(features)
            
        import pandas as pd
        df = pd.DataFrame([features])
        
        try:
            prediction = self.model.predict(df)[0]
            confidence = 0.92
            
            shap_values = self.explainer.shap_values(df)
            
            contributions = []
            for i, feature in enumerate(df.columns):
                val = shap_values[0][i] if isinstance(shap_values, list) else shap_values[0, i]
                if abs(val) > 0.1:
                    contributions.append({
                        "feature": feature,
                        "value": float(df[feature].iloc[0]),
                        "contribution": float(val)
                    })
                    
            contributions = sorted(contributions, key=lambda x: abs(x["contribution"]), reverse=True)[:3]
            
            reasons = []
            for c in contributions:
                fc = c["contribution"]
                f = c["feature"]
                if f == "key_size" and fc < 0:
                    desc = f"Uses RSA-{int(c['value'])} for key exchange (vulnerable to quantum attack)"
                elif f == "uses_weak_signature" and fc < 0:
                    desc = "Certificate uses weak signature (deprecated)"
                elif f == "tls_1_3" and fc > 0:
                    desc = "Supports TLS 1.3 with strong ciphers"
                else:
                    desc = f"Feature {f} contributed to score by {fc:.2f}"
                c["desc"] = desc
                reasons.append(c)
                
            return {
                "score": max(0, min(100, int(prediction))),
                "confidence": confidence,
                "model_version": "v1-xgboost",
                "explanations": reasons
            }
        except Exception:
            return self._rule_based_score(features)
