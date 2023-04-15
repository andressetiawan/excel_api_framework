FILE=/home/andres/Documents/skripsi/python-bdd/input/test_case.xlsx
if [ -e $FILE ]
then
    rm /home/andres/Documents/skripsi/python-bdd/input/*
fi

if [ $# -eq 0 ]
    then
        echo "Missing one argument. Solution: sh run.sh <filename>"
    else 
        if [ -e $1 ]
            then
                if [ -e /home/andres/Documents/skripsi/python-bdd/log.txt ]; then
                    rm /home/andres/Documents/skripsi/python-bdd/log.txt
                fi

                cp $1 /home/andres/Documents/skripsi/python-bdd/input/test_case.xlsx
                behave ./features/request.feature -f plain >> /home/andres/Documents/skripsi/python-bdd/log.txt
                cat log.txt

                if grep -q Traceback "/home/andres/Documents/skripsi/python-bdd/log.txt"; then
                    echo "\nSomething when wrong. Check file: $1\n"
                else
                    cd output
                    COLOR=1 npm start | cat
                fi

            else
                echo "$1 file not found!"
        fi
fi
