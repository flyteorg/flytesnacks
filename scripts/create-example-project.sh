#!/bin/sh
#
# Usage for default project:
#
# ./scripts/create-example-project.sh <project-name>
#
# For project that doesn't require dependencies:
#
# ./scripts/create-example-project.sh <project-name> 0

project_name="$1"
requires_deps="$2"

if [ -z "$project_name" ]
then
    echo "Please provide a project name"
    exit 1
fi

if [ -z "$requires_deps" ]
then
    requires_deps="1"
fi

cp -R _example_template ./examples/"$project_name"
mv "./examples/$project_name/_example_template" "./examples/$project_name/$project_name"

echo Creating a new project "./examples/$project_name"

if [ "$requires_deps" = "0" ]
then
    echo Removing dependency files
    rm "./examples/$project_name/Dockerfile" ./examples/"$project_name"/requirements.*
fi
