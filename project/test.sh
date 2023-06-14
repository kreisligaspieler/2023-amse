if [ -e ../data/data.sqlite ]
then
    rm ../data/data.sqlite
fi
python3 ../data/getData.py
if [ -e ../data/data.sqlite ]
then
    echo "Database created."
else
    echo "Database not found!"
    exit(1)
fi
python3 ../data/checkData.py

