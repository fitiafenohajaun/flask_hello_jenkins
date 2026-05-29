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
    securityContext:
      privileged: true          # Important
      runAsUser: 0              # Exécuter en root
    volumeMounts:
    - mountPath: /var/run/docker.sock
      name: docker-sock
    env:
    - name: DOCKER_HOST
      value: unix:///var/run/docker.sock

  - name: kubectl
    image: bitnami/kubectl:latest
    command: ["cat"]
    tty: true

  volumes:
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
      type: Socket
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
                        echo "=== Docker Debug ==="
                        ls -l /var/run/docker.sock
                        docker info
                        
                        echo "=== Building image ==="
                        docker build -t 172.20.0.2:4000/flask_hello:latest .
                        
                        echo "=== Pushing image ==="
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