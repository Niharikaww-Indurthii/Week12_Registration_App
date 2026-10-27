pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'YOUR_DOCKERHUB_USERNAME/selenium-registration-app'
        KUBECONFIG = 'C:\\Users\\harik\\.kube\\config'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'py -m pip install -r requirements.txt'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat 'py -m pytest -v tests/test_registrationapp.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %DOCKER_IMAGE%:%BUILD_NUMBER% .'
                bat 'docker tag %DOCKER_IMAGE%:%BUILD_NUMBER% %DOCKER_IMAGE%:latest'
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    powershell '$env:DOCKER_PASS | docker login -u $env:DOCKER_USER --password-stdin'
                    bat 'docker push %DOCKER_IMAGE%:%BUILD_NUMBER%'
                    bat 'docker push %DOCKER_IMAGE%:latest'
                    bat 'docker logout'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl config current-context'
                bat 'kubectl get nodes'
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
                bat 'kubectl set image deployment/selenium-registration-deployment registration-app=%DOCKER_IMAGE%:%BUILD_NUMBER%'
                bat 'kubectl rollout status deployment/selenium-registration-deployment --timeout=180s'
            }
        }

        stage('Verify Deployment') {
            steps {
                bat 'kubectl get deployments'
                bat 'kubectl get pods'
                bat 'kubectl get services'
            }
        }
    }

    post {
        success { echo 'Week 12 Registration Selenium pipeline completed successfully.' }
        failure { echo 'Pipeline failed. Check the first failed stage in Console Output.' }
        always { echo 'Week 12 pipeline execution finished.' }
    }
}
