current=$(pip list | grep "requests (2")

if [ -z "$current" ]; then

    pip install requests
    echo "Done"

else

    echo "Already installed"

fi
