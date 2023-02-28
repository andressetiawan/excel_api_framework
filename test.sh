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
                cp $1 /home/andres/Documents/skripsi/python-bdd/input/test_case.xlsx
                behave ./features/request.feature -f plain
                cd output
                npm run start
            else
                echo "$1 file not found!"
        fi
fi
