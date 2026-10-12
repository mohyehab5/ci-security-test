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
- For stronger supply-chain safety, pin third-party actions to commit SHAs.
