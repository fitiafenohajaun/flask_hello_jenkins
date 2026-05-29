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
  serviceAccountName: jenkins

  containers:

  # =========================
  # PYTHON CONTAINER
  # =========================
  - name: python
    image: python:3.12-slim
    command:
      - cat
    tty: true

  # =========================
  # KANIKO CONTAINER
  # =========================
  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    command:
      - /busybox/cat
    tty: true

  # =========================
  # KUBECTL CONTAINER
  # =========================
  - name: kubectl
    image: bitnami/kubectl:latest
    command:
      - cat
    tty: true
"""
        }
    }

    environment {
        IMAGE_NAME = "172.20.0.2:4000/pythontest"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {

        // =========================
        // CHECKOUT
        // =========================
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // =========================
        // TEST PYTHON
        // =========================
        stage('Test Python') {
            steps {
                container('python') {
                    sh '''
                        pip install --no-cache-dir -r requirements.txt

                        if [ -f test.py ]; then
                            python test.py
                        else
                            echo "Aucun test trouvé"
                        fi
                    '''
                }
            }
        }

        // =========================
        // BUILD + PUSH IMAGE
        // =========================
        stage('Build & Push Image') {
            steps {
                container('kaniko') {
                    sh '''
                        /kaniko/executor \
                          --dockerfile=Dockerfile \
                          --context=$(pwd) \
                          --destination=$IMAGE_NAME:$IMAGE_TAG \
                          --destination=$IMAGE_NAME:latest \
                          --insecure \
                          --skip-tls-verify \
                          --insecure-registry=172.20.0.2:4000
                    '''
                }
            }
        }

        // =========================
        // DEPLOY KUBERNETES
        // =========================
        stage('Deploy to Kubernetes') {
            steps {
                container('kubectl') {
                    sh '''
                        kubectl apply -f kubernetes/deployment.yaml
                        kubectl apply -f kubernetes/service.yaml

                        kubectl rollout restart deployment pythontest

                        kubectl rollout status deployment pythontest
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

        always {
            echo 'Fin du pipeline'
        }
    }
}