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
                    command:
                    - cat
                    tty: true
                  - name: docker
                    image: docker:latest
                    command:
                    - cat
                    tty: true
                    env:
                    - name: DOCKER_HOST
                      value: tcp://localhost:2375
                  - name: dind
                    image: docker:dind
                    securityContext:
                      privileged: true
                    command:
                    - dockerd
                    - --host=tcp://0.0.0.0:2375
                    - --tls=false
                    - --insecure-registry=host.docker.internal:4000
                    env:
                    - name: DOCKER_TLS_CERTDIR
                      value: ""
                  - name: kubectl
                    image: lachlanevenson/k8s-kubectl:v1.17.2
                    command:
                    - cat
                    tty: true
            """.stripIndent()
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

        stage('Build image') {
            steps {
                container('docker') {
                    sh "docker build -t host.docker.internal:4000/pythontest:latest ."
                    sh "docker push host.docker.internal:4000/pythontest:latest"
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