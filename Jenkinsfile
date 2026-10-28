
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'nihaaaa34/selenium-registration-app'
        KUBECONFIG = 'C:\\Users\\harik\\.kube\\config'
        PYTHON = 'C:\\Users\\harik\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Environment') {
            steps {
                bat '''
                    "%PYTHON%" --version
                    if errorlevel 1 exit /b 1

                    docker --version
                    if errorlevel 1 exit /b 1

                    kubectl version --client
                    if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    "%PYTHON%" -m pip install --upgrade pip
                    if errorlevel 1 exit /b 1

                    "%PYTHON%" -m pip install -r requirements.txt
                    if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat '''
                    "%PYTHON%" -m pytest -v tests/test_registrationapp.py
                    if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    docker info
                    if errorlevel 1 exit /b 1

                    docker build -t %DOCKER_IMAGE%:%BUILD_NUMBER% .
                    if errorlevel 1 exit /b 1

                    docker tag %DOCKER_IMAGE%:%BUILD_NUMBER% %DOCKER_IMAGE%:latest
                    if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    bat '''
                        @echo off
                        echo Attempting Docker Hub login for %DOCKER_USER%...
                        echo %DOCKER_PASS%| docker login --username %DOCKER_USER% --password-stdin
                        if errorlevel 1 exit /b 1

                        echo Pushing %DOCKER_IMAGE%:%BUILD_NUMBER%...
                        docker push %DOCKER_IMAGE%:%BUILD_NUMBER%
                        if errorlevel 1 exit /b 1

                        echo Pushing %DOCKER_IMAGE%:latest...
                        docker push %DOCKER_IMAGE%:latest
                        if errorlevel 1 exit /b 1

                        echo Docker push complete. Logging out...
                        docker logout
                    '''
                }
            }
        }

        stage('Check Kubernetes Access') {
            steps {
                bat '''
                    kubectl config current-context
                    if errorlevel 1 exit /b 1

                    kubectl get nodes
                    if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    kubectl apply -f deployment.yaml
                    if errorlevel 1 exit /b 1

                    kubectl set image deployment/selenium-registration-deployment registration-app=%DOCKER_IMAGE%:%BUILD_NUMBER%
                    if errorlevel 1 exit /b 1

                    kubectl apply -f service.yaml
                    if errorlevel 1 exit /b 1

                    kubectl rollout status deployment/selenium-registration-deployment --timeout=180s
                    if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                bat '''
                    kubectl get deployments
                    if errorlevel 1 exit /b 1

                    kubectl get pods
                    if errorlevel 1 exit /b 1

                    kubectl get services
                    if errorlevel 1 exit /b 1

                    kubectl get deployment selenium-registration-deployment -o wide
                    if errorlevel 1 exit /b 1
                '''
            }
        }
    }

    post {
        success {
            echo 'Week 12 Registration Selenium pipeline completed successfully.'
            echo 'Application URL: http://localhost:30188'
        }

        failure {
            echo 'Week 12 pipeline failed. Review the first failed stage and its error.'
        }

        always {
            echo 'Week 12 pipeline execution finished.'
        }
    }
}