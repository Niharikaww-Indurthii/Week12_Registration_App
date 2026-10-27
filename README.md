# Week 12 — Registration App with Selenium

This is a separate project from FindIt. It follows the Week 12 document's Registration app and four Selenium scenarios: empty username, empty password, short password, and valid registration.

## Requirements
- Python 3.10+
- Google Chrome installed for local Selenium tests
- Docker Desktop for container build
- `kubectl` and a running Kubernetes cluster for deployment

## Run locally (PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py -m pytest -v tests/test_registrationapp.py
```

The test fixture starts Flask automatically at `http://127.0.0.1:5000`, then stops it after the tests. Selenium Manager may download/find a compatible ChromeDriver, so the first run needs network access if no driver is cached.

## Run the application manually
```powershell
py app.py
```
Open `http://127.0.0.1:5000`.

## Docker
Replace `YOUR_DOCKERHUB_USERNAME` in `deployment.yaml` and the `DOCKER_IMAGE` environment value in `Jenkinsfile` with your Docker Hub username before running the pipeline.
```powershell
docker build -t YOUR_DOCKERHUB_USERNAME/selenium-registration-app:latest .
docker run --rm -p 5000:5000 YOUR_DOCKERHUB_USERNAME/selenium-registration-app:latest
```

## Jenkins notes
1. Configure Jenkins credential ID `dockerhub-creds` as a Username/Password credential for Docker Hub.
2. Ensure the Jenkins agent can access Docker Desktop and Kubernetes. Update `KUBECONFIG` to the path accessible to the Jenkins service account; the sample path is specific to the current Windows setup.
3. Ensure Chrome is installed and accessible to the Jenkins service account. The Selenium test stage runs in the Jenkins agent environment, before Docker build/deployment.
4. Replace `YOUR_DOCKERHUB_USERNAME` in the Jenkinsfile with the actual Docker Hub username.
5. The Docker login stage uses PowerShell to pipe the credential to `docker login --password-stdin`; if your Jenkins Windows shell configuration differs, adjust that command accordingly.

## Kubernetes
The Service uses NodePort `30188`, so with Docker Desktop Kubernetes enabled the app is typically reachable at `http://localhost:30188` after deployment. This URL is only available once the image is pushed and the deployment rollout succeeds.
