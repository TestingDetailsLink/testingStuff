#!/usr/bin/env groovy

properties([
        buildDiscarder(logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '', numToKeepStr: '10')),
        gitLabConnection('192.168.13.102:30009'),
        parameters([
                string(name: 'BRANCH_TO_BUILD', defaultValue: 'master' )   
        ]),
        pipelineTriggers([])
])

node("slave") {
    
    deleteDir()
    def app
    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */

        checkout scm
    }
    
    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */
        app = docker.build("tattiq/kafka_sf")
    }

    stage('Test image') {
        /* Ideally, we would run a test framework against our image. */

        app.inside {
            sh 'echo "pitches"'
        }
    }

    stage('Push image') {
        /* Finally, we'll push the image with two tags:
         * First, the incremental build number from Jenkins
         * Second, the 'latest' tag.
         * Pushing multiple tags is cheap, as all the layers are reused. */
        docker.withRegistry('192.168.13.102:30009') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }
    cleanWs()
}
