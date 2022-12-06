pipeline {
    agent any

    environment {
        PATH = "$PATH:/usr/bin"
        GIT_COMMIT_MSG = sh (script: 'git log -1 --pretty=%B ${GIT_COMMIT}', returnStdout: true).trim()
    }

    stages {
        stage("Deploy Prod") {
            when {
                branch "master"
            }

            steps {
                echo "Deploying and Building..."
                sh "sendNotification 'Found new commit `${GIT_COMMIT_MSG}`'"
                sh "sendNotification '#secret_santa 🛠 Building New Container #${BUILD_NUMBER}'"
                sh "docker-compose build"
                sh "sendNotification '#secret_santa 🐳 Upping New Container #${BUILD_NUMBER}'"
                sh "docker-compose up -d"
                echo "Deployed!"
            }
        }
    }

    post {
        success {
            sh "sendNotification '#secret_santa 🥃 Deploy Succeed 😍💕😋😎️'"
        }
        failure {
            sh "sendNotification '#secret_santa 🛑 Deploy Failed  😩😑😖😳'"
        }
    }
}