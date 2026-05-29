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

  - name: docker
    image: docker:29-cli
    command: ["cat"]
    tty: true
    env:
    - name: DOCKER_HOST
      value: tcp://localhost:2375
    - name: DOCKER_TLS_VERIFY
      value: ""

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

    triggers { pollSCM('* * * * *') }

    stages {
        stage('Test python') {
            steps {
                container('python') {
                    sh "pip install -r requirements.txt"
                    sh "python test.py"
                }
            }
        }

        stage('Build image') {
            steps {
                container('docker') {
                    sh '''
                        echo "Waiting for Docker daemon to be ready..."
                        for i in {1..30}; do
                            if docker info >/dev/null 2>&1; then
                                echo "Docker daemon is ready!"
                                break
                            fi
                            echo "Waiting... ($i/30)"
                            sleep 3
                        done
                        
                        docker build -t 172.20.0.2:4000/flask_hello:latest .
                        docker push 172.20.0.2:4000/flask_hello:latest
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