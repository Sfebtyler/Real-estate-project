#! /bin/bash

PROJECT_NAME="$1"
if [[ -z "${PROJECT_NAME// }" ]]; then
    echo >&2 "Usage: startproject.sh <project_name>"
    exit 1
fi

if ! hash django-admin 2>/dev/null; then
    echo >&2 "The 'django-admin' command is not available."
    exit 1
fi

if ! hash wget curl 2>/dev/null; then
    echo >&2 "The 'wget' command is not available."
    exit 1
fi

# create a temp directory where the script is running from
TEMP_DIR=`mktemp -d -p $(pwd)`

# dowload the template archive, and extract the project_template into $TEMP_DIR
wget -qO- https://dev.izeni.net/izeni/izeni-django-template/repository/archive.tar.gz?ref=no-accounts |tar zx -C $TEMP_DIR --strip-components=2

# invoke django startproject
django-admin startproject \
  --template=$TEMP_DIR/ \
  --extension=py,ini,md,sh,yml --name Dockerfile,run \
  $PROJECT_NAME

# delete the temp directory
rm -rf $TEMP_DIR

# fix permissions for files that should be executable
chmod a+x \
  $PROJECT_NAME/run \
  $PROJECT_NAME/manage.py \
  $PROJECT_NAME/server/django_devserver.sh
