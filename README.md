# Secure CI pipeline (GitHub Actions + Composite Actions)

```
Push / PR -> Checkout -> [pre-test-security] -> pytest -> docker build -> [post-test-security]
```

| Stage | Where | Tools |
|---|---|---|
| Pre-test security | `.github/actions/pre-test-security` (composite) | Gitleaks, Trivy FS, TruffleHog |
| Tests | `ci.yml` | pytest |
| Build | `ci.yml` | docker build |
| Post-test security | `.github/actions/post-test-security` (composite) | Trivy image scan |

## Layout
```
.github/workflows/ci.yml
.github/actions/pre-test-security/action.yml
.github/actions/post-test-security/action.yml
app/main.py          Flask sample app
tests/test_app.py    pytest tests
Dockerfile           non-root, gunicorn
.gitleaks.toml       gitleaks config
.trivyignore         accepted CVEs
```

## Run locally
```bash
pip install -r requirements-dev.txt && pytest
docker build -t secure-pipeline-app .
docker run -p 8000:8000 secure-pipeline-app
```

## Notes
- `fetch-depth: 0` is required so Gitleaks/TruffleHog can scan history.
- Local composite actions can only be used after `actions/checkout`.
- Every `run` step in a composite action needs `shell: bash`.
- Inputs let you tune severity or switch to report-only (`exit-code: "0"`).
- trivy-action is pinned to `v0.35.0` and the Trivy binary to `v0.69.3` because of the March 2026 Trivy supply-chain compromise (GHSA-69fq-xp46-6x23). Older tags like `0.28.0` were deleted. Prefer pinning to a full commit SHA.
