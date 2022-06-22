#!/bin/bash

install_poetry() {
    apt update
    apt install -y curl python3 python3-dev python3-pip
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
    echo "source $HOME/.poetry/env" >>~/.bashrc
    source $HOME/.poetry/env
    # set interpreter path on vscode
    # ~/.cache/pypoetry/virtualenvs/<env>/bin/python3.10
}

update_toolchain() {
    poetry update
}

setup() {
    apt update
    apt install -y apt-utils git
    ln -fns /usr/bin/python3 /usr/bin/python
    install_poetry
    source ~/.bashrc
    update_toolchain
    poetry install
}

lint() {
    poetry run mypy .
    poetry run pflake8 .
}

publish_dry() {
    poetry publish \
        --build \
        --username kagemeka \
        --verbose \
        --version \
        -n \
        --dry-run
}

format() {
    poetry run isort .
    poetry run black .
    ./../scripts/pre-commit.sh
}

test() {
    poetry run pytest \
        --asyncio-mode=strict \
        --verbose .

}

clear_cache() {
    poetry cache clear pypi --all
    find . | grep -E "__pycache__$" | xargs rm -rf
}

ci() {
    source ~/.bashrc
    if ! command -v poetry &>/dev/null; then
        echo "command not found"
        setup
    fi

    update_toolchain
    format
    lint
    test

    $@
}

ci $@
