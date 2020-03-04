#!/bin/bash -e

case $1 in
    init)
        virtualenv venv
        . venv/bin/activate
        pip install -r requirements.txt
        # setup ipysheet for labextension
        jupyter labextension install @jupyter-widgets/jupyterlab-manager
        jupyter labextension install ipysheet
        ;;

    env-setup)
        ipython kernel install --user --name=venv
        ;;

    clean)
        rm -rf venv
        ;;

    *)
        echo available commands: init, env-setup, clean
        exit 1
        ;;
esac
