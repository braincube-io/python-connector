#!/usr/bin/env bash

TO_PUBLISH='documentation'
SITE_NAME=$(grep -oP 'name = "\K[^"]+' pyproject.toml)' documentation'
REPO_URL=$(grep -oP 'repository = "\K[^"]+' pyproject.toml)
if [[ ! -d "gitlabci-commons" ]]
then
    git clone https://gitlab.ipleanware.com/braincube/misc/gitlabci-commons.git
fi

cp -r gitlabci-commons/braincube-pages/docs/* docs
cp -r gitlabci-commons/braincube-pages/custom_theme .
sed -i -e 's|__SITE_NAME__|'"${SITE_NAME}"'|' -e 's|__REPO_URL__|'"${REPO_URL}"'|'  docs/index.md
poetry run mkdocs $1
