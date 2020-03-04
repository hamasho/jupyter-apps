#!/bin/bash -e

error() {
    echo "$@"
    exit 1
}

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

    convert)
        infile=$2
        outfile=$3
        [[ -z "$2" || -z "$3" ]] && error "usage: ./script.sh convert MP4_FILE GIF_FILE"
        ffmpeg -i $infile -r 5 $outfile
        ;;

    *)
        error "available commands: init, env-setup, clean, convert"
        ;;
esac
