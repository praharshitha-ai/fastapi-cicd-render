# FastAPI CI/CD pipeline with automatic Render deploys

A small prediction service built to practise the full path from a code change to a live deployment. Every push to `main` runs the backend tests in GitHub Actions, and only when they pass does the workflow trigger a deploy to Render.

- **Live app:** https://git-cicd-1-ngtw.onrender.com (Streamlit frontend)
- **Live API:** https://cicd-pipeline-7tcq.onrender.com (FastAPI backend)

Both run on Render's free plan, so the first request after a quiet period can take up to a minute while the service wakes up.

## How it works

```text
git push → GitHub Actions: install deps → import check → pytest
                                   │
                         tests pass? ── no ──→ stop (nothing deployed)
                                   │
                                  yes
                                   ↓
                     Render deploy hook → new API version live
```

- `backend/`: FastAPI app with a health check (`GET /`) and a prediction endpoint (`POST /predict`). It loads a scikit-learn linear regression model from `backend/models/model.pkl`.
- `backend/tests/`: pytest tests for both endpoints, run with FastAPI's `TestClient`.
- `frontend/`: Streamlit app that sends the user's inputs to the live API and shows the predicted price.
- `.github/workflows/backend-ci.yaml`: tests the backend, then calls the Render deploy hook (stored as the `RENDER_DEPLOY_HOOK` repository secret).
- `.github/workflows/frontend-ci.yaml`: install and import checks for the frontend whenever `frontend/` changes.

The model is deliberately simple. It's a linear regression on a five-row toy dataset of house area, bedrooms and price, because the point of the project is the pipeline, not the model.

## Try the API

```bash
curl -X POST https://cicd-pipeline-7tcq.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"area": 1200, "bedrooms": 2}'
```

```json
{"predicted_price": 63448.28}
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
python backend/training.py              # retrain and save backend/models/model.pkl
cd backend && python -m pytest tests/   # run the tests
uvicorn main:app --reload               # API at http://127.0.0.1:8000
```

For the frontend, run `pip install -r frontend/requirements.txt` and then `streamlit run frontend/streamlit_app.py`. It calls the live API by default. Change `API_URL` in `frontend/streamlit_app.py` to point it at a local backend.
