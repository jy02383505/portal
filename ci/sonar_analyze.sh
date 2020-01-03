#!/bin/bash

/usr/local/sonar-scanner/bin/sonar-scanner \
    -X \
  -Dsonar.projectKey=git:master:fusion_nova_portal \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://223.202.202.47:9000/sonar \
  -Dsonar.login=e49f927e0be621bd4365b43c2f5e249c8cf73894
  

if [ $? -eq 0 ]; then
    echo "sonarqube code-publish over."
fi
