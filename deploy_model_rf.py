# deploy_model.py

from azureml.core import Workspace, Environment, Model
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice

# Load your workspace
ws = Workspace.from_config()

# Create or load environment
env = Environment(name="fraud-rf-env")
env.python.conda_dependencies.add_pip_package("scikit-learn")
env.python.conda_dependencies.add_pip_package("joblib")
env.register(workspace=ws)

# Inference config using the new score.py
inference_config = InferenceConfig(
    entry_script="score_rf.py",
    environment=env
)

# Deployment config
deployment_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)

# Deploy the model
service = Model.deploy(
    workspace=ws,
    name="fraud-detection-system-endpoint",
    models=[Model(ws, "fraud_detection_rf_model")],
    inference_config=inference_config,
    deployment_config=deployment_config,
    overwrite=True
)

# Wait for deployment to complete
service.wait_for_deployment(show_output=True)

print(f"✅ Endpoint deployed at: {service.scoring_uri}")
