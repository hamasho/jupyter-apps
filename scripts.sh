#!/bin/bash -e

error() {
    echo "$@"
    exit 1
}

help() {
    echo "commands: init, run-note, update-data, lab-setup,"
    echo "          env-setup, clean, convert"
}

case $1 in
    init)
        virtualenv venv
        . venv/bin/activate
        pip install -r requirements.txt
        ;;

    run-note)
        . venv/bin/activate
        set -a
        . .env
        jupyter notebook
        ;;

    update-data)
        . venv/bin/activate
        set -a
        . .env
        python update_data.py
        ;;

    lab-setup)
        jupyter labextension install @jupyter-widgets/jupyterlab-manager
        jupyter labextension install ipysheet
        jupyter lab build
        ;;

    env-setup)
        ipython kernel install --user --name=venv
        jupyter nbextension enable --py --sys-prefix gmaps
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
        help
        exit 1
        ;;
esac
