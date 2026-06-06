pipeline {

    agent any

    stages {

        stage('Test Flask') {
            steps {
                script {
                    docker.image('python:3.11').inside('-u root') {
                        sh 'pip install -r requirements.txt'
                        sh 'python test.py'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask_hello:latest .'
            }
        }

        stage('Push Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub_credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker tag flask_hello:latest fitiafenohajaun/flask_hello_jenkins:latest
                    docker push fitiafenohajaun/flask_hello_jenkins:latest
                    '''
                }
            }
        }
    }
}