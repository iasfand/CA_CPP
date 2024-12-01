#!/bin/bash

APP_NAME="x23358530_skyport_cpp"

# Get all application versions
VERSION_LABELS=$(aws elasticbeanstalk describe-application-versions --application-name $APP_NAME --query "ApplicationVersions[*].VersionLabel" --output text)

# Loop through and delete versions
for VERSION in $VERSION_LABELS; do
  echo "Deleting version: $VERSION"
  aws elasticbeanstalk delete-application-version --application-name $APP_NAME --version-label $VERSION --delete-source-bundle
done
