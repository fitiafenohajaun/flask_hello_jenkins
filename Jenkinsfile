pipeline {
    agent {
        kubernetes {
            label 'jenkins-agent-my-app'
            inheritFrom ''                    // ← Important : ignore les templates existants
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

  - name: docker
    image: docker:29-cli
    command: ["cat"]
    tty: true
    env:
    - name: DOCKER_HOST
      value: tcp://localhost:2375
    - name: DOCKER_TLS_VERIFY
      value: "0"

  - name: dind
    image: docker:29-dind
    securityContext:
      privileged: true
    command: ["dockerd"]
    args:
    - "--host=tcp://0.0.0.0:2375"
    - "--tls=false"
    - "--insecure-registry=172.20.0.2:4000"
    env:
    - name: DOCKER_TLS_CERTDIR
      value: ""

  - name: kubectl
    image: bitnami/kubectl:latest
    command: ["cat"]
    tty: true
"""
        }
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

        stage('Build & Push') {
            steps {
                container('docker') {
                    sh '''
                        echo "Waiting for DinD daemon..."
                        sleep 12
                        
                        echo "Building image..."
                        docker --host tcp://localhost:2375 build -t 172.20.0.2:4000/flask_hello:latest .
                        
                        echo "Pushing image..."
                        docker --host tcp://localhost:2375 push 172.20.0.2:4000/flask_hello:latest
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