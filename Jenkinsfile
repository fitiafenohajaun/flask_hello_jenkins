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
    - name: DOCKER_BUILDKIT
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
        stage('Build image') {
            steps {
                container('docker') {
                    sh '''
                        set -x
                        
                        echo "=== Forcing Docker configuration ==="
                        mkdir -p ~/.docker
                        echo "{}" > ~/.docker/config.json
                        
                        echo "=== Environment ==="
                        env | grep -E "DOCKER|PATH"
                        
                        echo "=== Testing connection ==="
                        docker --debug info || echo "Failed to connect"
                        
                        echo "=== Waiting for dind (60 seconds max) ==="
                        timeout=20
                        for i in $(seq 1 $timeout); do
                            if docker info >/dev/null 2>&1; then
                                echo "✅ Docker daemon ready !"
                                break
                            fi
                            sleep 3
                        done
                        
                        echo "=== Building ==="
                        docker build -t 172.20.0.2:4000/flask_hello:latest .
                    '''
                }
            }
        }
    }
}