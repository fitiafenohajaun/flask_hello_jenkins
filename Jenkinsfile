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
  - name: python
    image: python:3.12-slim
    command: ["cat"]
    tty: true

  - name: kaniko
    image: gcr.io/kaniko-project/executor:v1.23.2-debug
    command: ["cat"]
    tty: true

  - name: kubectl
    image: bitnami/kubectl:latest
    command: ["cat"]
    tty: true
"""
        }
    }

    triggers {
        pollSCM('* * * * *')
    }

    stages {
        stage('Test python') {
            steps {
                container('python') {
                    sh "pip install -r requirements.txt"
                    sh "python test.py"
                }
            }
        }

        stage('Build & Push Image') {
            steps {
                container('kaniko') {
                    sh '''
                        echo "=== Building with Kaniko ==="

                        /kaniko/executor \
                          --context . \
                          --dockerfile Dockerfile \
                          --destination 172.20.0.2:4000/flask_hello:latest \
                          --insecure \
                          --insecure-registry 172.20.0.2:4000 \
                          --verbosity=info
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                container('kubectl') {
                    sh "kubectl apply -f ./kubernetes/deployment.yaml"
                    sh "kubectl apply -f ./kubernetes/service.yaml"
                }
            }
        }
    }
}