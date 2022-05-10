#!/bin/bash


Help()
{
    # Display Help
    echo "A helper function for simulation"
    echo
    echo "E.g. simulation -s"
    echo "options:"
    echo "-s   Sets up the environment for the simulation"
    echo "-c   Removes the venv"
    echo "-b   Builds venv"
    echo "-r   Runs the simulation"
    echo "-h   Displays this help message"
    echo
}

CheckPython()
{
    echo "============= Checking Python version ============="
    # Check if python is installed
    if ! [ -x "$(command -v python)" ]; then
        echo "Error: python is not installed" >&2
        exit 1
    fi
    # Get python version
    python_version=$(python3 -V 2>&1 | cut -d' ' -f2)
    echo "Python version: $python_version"
    # Check if python version is greater than 3.9
    if [ "$python_version" \< "3.8.0" ]; then
        echo "Error: python version needs to be equal or greater than 3.9.10" >&2
        exit 1
    fi

}

Check_venv()
{
    echo "============= Checking venv ============="
     # Check if $VIRTUAL_ENV is set
    if [ -z "$VIRTUAL_ENV" ]; then
        echo "Error: venv is not set. Set it up with -s" >&2
        exit 1
    fi
}


Build(){
    echo "============= Building venv ============="
   Check_venv
    pip install -r requirements.txt
}
Clean(){
    echo "============= Cleaning venv ============="
    # Check if need to deactivate venv
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate
    fi
    rm -rf venv
}
Setup(){
    echo "============= Setting up simulation ============="
    # Create venv

    Clean
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    Build
}

Run(){
    echo "============= Running simulation ============="
    Check_venv
    source venv/bin/activate
    python main.py
    
}

CheckPython
while getopts "scbrh:" option; do
    echo $option
    case $option in
        h) # display Help
            Help
        exit;;
        s) # setup the environment
            Setup
        exit;;
        c) # clean the environment
            Clean
        exit;;
        b) # build the environment
            Build
        exit;;
        r) # run the simulation
            Run
        exit;;
        
        \?) # incorrect option
            echo "Error: Invalid option"
        exit;;
    esac
done

echo "Hello world!"


# version=$(python -V 2>&1 | grep -Po '(?<=Python )(.+)')
# if [[ -z "$version" ]]
# then
#     echo "Please install Python 3.9.10"
# fi