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

    triggers { pollSCM('* * * * *') }

    stages {
        stage('Build image') {
            steps {
                container('docker') {
                    sh '''
                        set -x  # Active le debug
                        
                        echo "=== Environment variables ==="
                        env | grep DOCKER
                        
                        echo "=== Checking Docker connection ==="
                        docker info || echo "Docker info failed"
                        
                        echo "=== Waiting for dind daemon (max 60s) ==="
                        for i in {1..20}; do
                            if docker info > /dev/null 2>&1; then
                                echo "✅ Docker daemon is ready!"
                                break
                            fi
                            echo "Waiting... ($i/20)"
                            sleep 3
                        done
                        
                        echo "=== Building image ==="
                        docker build -t 172.20.0.2:4000/flask_hello:latest .
                        
                        echo "=== Pushing image ==="
                        docker push 172.20.0.2:4000/flask_hello:latest
                    '''
                }
            }
        }
    }
}