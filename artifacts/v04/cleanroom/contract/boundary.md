# Clean-room boundary (frozen pre-reveal)

FORBIDDEN_IMPORTS = [python/adversary/*, python/solver/*, python/holdout/h4l_evaluate.py,
  artifacts/v04/development/*, artifacts/v04/validation/*, H4L bank bytes pre-reveal,
  candidate outcomes/failures, solver state]
ALLOWED = [math/theorems/*, schemas/*, input histories, artifacts/v04/cleanroom/contract/*]
CHECK = static import scan in WP-5 seal (any forbidden import fails closed).
