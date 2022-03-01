rm -rf submission
rm -rf scores
rm -f scores.zip
rm -f scores.txt
rm -f canvas.txt
mkdir submission
mkdir scores
find . -name '*.zip' -exec sh -c 'unzip -d "submission/${1%.*}" "$1"' _ {} \;

# copy Python files from subdirectories
for i in submission/*/
do
    cd "$i"
    find . -mindepth 2 -name '*.py' -type f -print -exec mv {} . \;
    cd ../..
done

for i in `ls ./submission`
do
    if [ -d ./submission/"$i" ]
    then
        cd ./submission/"$i"
        cp -r ../../test/* .
        printf '\n%s\n' "$i"
        python3 test.py | tee scores.txt
        zip "${i}.zip" *.txt output/*.txt
        cp "${i}.zip" ../../scores/"${i}.zip"
        cd ../..
    fi
done

python3 score.py
zip -r -j scores.zip scores
