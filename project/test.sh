if [ -e ../data/data.sqlite ]
then
    rm ../data/data.sqlite
fi
python3 ../data/getData.py
if [ -e ../data/data.sqlite ]
then
    echo "Database generated."
else
    echo "Database not found!"
fi

