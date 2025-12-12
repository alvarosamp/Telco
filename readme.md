# Telco Customer Churn

## Visao geral
- Predicao de churn de clientes de telecom com XGBoost, usando o dataset WA_Fn-UseC_-Telco-Customer-Churn.
- Pipeline principal: carga de dados, limpeza leve, treino com MLflow, servico FastAPI/Gradio para previsoes em tempo real.
- Artefatos de modelo ficam em `mlruns/` e sao consumidos no servico via pasta `/app/model` (ou fallback para o ultimo run local).

## Estrutura rapida
- Data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv: base original (versionada via DVC).
- notebooks/EDA.ipynb: exploracao inicial.
- src/data/load_data.py: leitura de CSV com checagem de existencia.
- src/data/preprocess.py: limpeza basica (trim de colunas, remocao de IDs, TODO concluir mapeamento do alvo e NAs).
- src/features/build_features.py: helper para mapear series binarias em 0/1.
- src/models/train.py: `train_model` treina XGBClassifier, loga accuracy/recall e o dataset no MLflow.
- src/models/tune.py: `tune_model` usa Optuna (recall em cross-val) para sugerir hiperparametros.
- src/serving/inference.py: carrega modelo MLflow, aplica as mesmas transformacoes de treino (BINARY_MAP, one-hot com drop_first, alinhamento via `feature_columns.txt`) e devolve "Likely to churn" ou "Not likely to churn".
- src/app/main.py: API FastAPI com `/` health check, `/predict`, e UI Gradio montada em `/ui` usando a mesma funcao de inferencia.
- src/utils/validate_data.py: validacao com Great Expectations (schema, ranges e regras de negocio). src/utils/utils.py: configuracao simples de logger.

## Dados
- Fonte: Data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv (espelhado tambem em Data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv.dvc).
- Alvo esperado: coluna `Churn` (binaria), conforme dataset original da IBM Telco.

## Treino rapido
Exemplo minimo em Python interativo:

```python
from src.data.load_data import load_data
from src.data.preprocess import preprocess_data
from src.models.train import train_model

df = load_data("Data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
df = preprocess_data(df, target_col="Churn")  # limpeza basica (completar conforme necessidade)
train_model(df, target_col="Churn")           # logs em mlruns/
```

## Servico (FastAPI + Gradio)
- Requer o modelo salvo em `/app/model` com `MLmodel`, `model.xgb` e `feature_columns.txt` (ou usa o ultimo run encontrado em `mlruns/*/*/artifacts/model`).
- Subir localmente: `uvicorn src.app.main:app --reload --port 8000`.
- Endpoints: `GET /` (health), `POST /predict` com 18 campos (gender, Partner, Dependents, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod, tenure, MonthlyCharges, TotalCharges).
- UI: Gradio em `/ui`, reutilizando a mesma pipeline de inferencia e exemplos prontos para teste manual.

## Validacao de dados
- Use `validate_telco_data` em src/utils/validate_data.py para checar schema, ranges e regras de negocio antes do treino. Retorna (sucesso, lista_de_falhas).

## Dependencias e setup
- Python 3.11+ sugerido.
- Instale dependencias basicas de notebook: `pip install -r requirements.txt`.
- Dependencias de modelo/serving (caso nao estejam no requirements): `pip install fastapi uvicorn[standard] gradio pandas scikit-learn xgboost optuna mlflow great-expectations`.

## Proximos passos uteis
- Completar `preprocess_data` (mapear `Churn` para 0/1, tratar NAs e codificacao de categoricas).
- Adicionar script/CLI para orquestrar carga -> validacao -> treino -> log do modelo.
- Incluir testes automatizados para o pipeline e para o servico de inferencia.
