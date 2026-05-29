pipeline {
    agent {
        kubernetes {
            // Ce label sera le préfixe du nom du pod créé par Jenkins
            label 'jenkins-agent-my-app'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    component: ci
spec:
  containers:
  # Conteneur 1 : pour exécuter les tests Python
  - name: python
    image: python:3.12-slim
    command:
    - cat
    tty: true

  # Conteneur 2 : pour builder et pousser l'image Docker
  - name: docker
    image: docker
    command:
    - cat
    tty: true
    volumeMounts:
    - mountPath: /var/run/docker.sock
      name: docker-sock

  # Conteneur 3 : pour déployer dans Kubernetes avec kubectl
  - name: kubectl
    image: lachlanevenson/k8s-kubectl:v1.17.2
    command:
    - cat
    tty: true

  # Volume partagé : donne accès au socket Docker de la machine hôte
  volumes:
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
"""
        }
    }

    // Déclenche automatiquement le pipeline si le dépôt Git a changé (vérifie toutes les minutes)
    triggers {
        pollSCM('* * * * *')
    }

    stages {

        // STAGE 1 : Lancer les tests unitaires Python
        stage('Test python') {
            steps {
                container('python') {
                    sh "pip install -r requirements.txt"
                    sh "python test.py"
                }
            }
        }

        // STAGE 2 : Construire l'image Docker et la pousser sur le registry local
        stage('Build image') {
            steps {
                container('docker') {
                    sh "docker build -t localhost:4000/pythontest:latest ."
                    sh "docker push localhost:4000/pythontest:latest"
                }
            }
        }

        // STAGE 3 : Déployer l'application dans Kubernetes
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