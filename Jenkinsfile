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

    stages {
        stage('Build & Push') {
            steps {
                container('docker') {
                    sh '''
                        echo "=== DEBUG DIN D ==="
                        echo "Current DOCKER_HOST = $DOCKER_HOST"
                        
                        echo "=== Waiting for dind (15 seconds) ==="
                        sleep 15
                        
                        echo "=== Testing connection ==="
                        nc -z localhost 2375 && echo "Port 2375 is open" || echo "Port 2375 is NOT open"
                        
                        echo "=== Docker info with explicit host ==="
                        docker --host tcp://localhost:2375 info || echo "Docker info FAILED"
                        
                        echo "=== Building image ==="
                        docker --host tcp://localhost:2375 build -t 172.20.0.2:4000/flask_hello:latest .
                        
                        echo "=== Pushing image ==="
                        docker --host tcp://localhost:2375 push 172.20.0.2:4000/flask_hello:latest
                    '''
                }
            }
        }
    }
}