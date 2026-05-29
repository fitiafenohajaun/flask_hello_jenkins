pipeline {
    agent {
        kubernetes {
            label 'jenkins-agent-my-app'

            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    component: ci

spec:
  containers:

  # Conteneur Python pour les tests
  - name: python
    image: python:3.12-slim
    command:
    - cat
    tty: true

  # Conteneur Kaniko pour build et push Docker image
  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    command:
    - /busybox/cat
    tty: true

  # Conteneur kubectl pour le déploiement Kubernetes
  - name: kubectl
    image: bitnami/kubectl:latest
    command:
    - cat
    tty: true
"""
        }
    }

    triggers {
        pollSCM('* * * * *')
    }

    environment {
        IMAGE_NAME = "172.20.0.2:4000/flask_hello:latest"
    }

    stages {

        // =========================
        // STAGE 1 : TESTS PYTHON
        // =========================
        stage('Test Python') {
            steps {
                container('python') {
                    sh '''
                    pip install --no-cache-dir -r requirements.txt
                    python test.py
                    '''
                }
            }
        }

        // =========================
        // STAGE 2 : BUILD + PUSH IMAGE
        // =========================
        stage('Build & Push Image') {
            steps {
                container('kaniko') {
                    sh '''
                    /kaniko/executor \
                      --dockerfile=Dockerfile \
                      --context=$(pwd) \
                      --destination=$IMAGE_NAME \
                      --insecure \
                      --skip-tls-verify
                    '''
                }
            }
        }

        // =========================
        // STAGE 3 : DEPLOIEMENT K8S
        // =========================
        stage('Deploy to Kubernetes') {
            steps {
                container('kubectl') {
                    sh '''
                    kubectl apply -f kubernetes/deployment.yaml
                    kubectl apply -f kubernetes/service.yaml
                    '''
                }
            }
        }

    }

    post {

        success {
            echo 'Pipeline exécuté avec succès ✅'
        }

        failure {
            echo 'Pipeline échoué ❌'
        }

    }
}