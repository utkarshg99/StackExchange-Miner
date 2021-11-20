mkdir -p Data
mkdir -p Results
mkdir -p Scraping
mkdir -p Data/Extracted

npm install
pip3 install -r requirements.txt

node --max-old-used-space=12288 index.js > logs.dump

cd Scripts

jq -c '.urls[]' config.json | while read i; do
    python3 main_.py $i
done