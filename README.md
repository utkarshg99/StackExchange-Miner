# StackExchange-Miner

# Requirements

## Hardware:

* Atleast 8GB of RAM 
* Internet Connectivity

## Software:

* OS: Ubuntu

# Installation Instructions

## Following Frameworks are needed to run the project:

* NodeJS
* Python3
* R

Please follow the official instructions to install them properly. Make sure that the following commands get executed without any errors:
```
node --version
npm --version
python3 --version
pip3 --version
R --version
```
The minimum versions needed are:

| Name    | Minimum Version |
|---------|-----------------|
| NodeJS  | 12.22.6         |
| Python3 | 3.6.9           |
| R       | 4.1.2           |

## Following Libraries are needed to be installed:

### Node
Details mentioned in `dependencies` field of [`package.json`](package.json). Run:
```
npm install package.json
```

### Python3 
Libraries mentioned in [`requirements.txt`](requirements.txt). Run:
```
pip3 install -r requirements.txt
```

### R: 
`arules` package needs to be installed. Run:
```
R
```
Once inside the the R shell execute:
```
install.packages("arules")
```

# Running Instructions

### Once the required Frameworks are installed:

## Run [`start.sh`](start.sh)

```
apt install jq
./start.sh
```

## OR

## Execute:

### To download, extract and convert the datasets:

Make edits to the list of stackexchanges mentioned in [`config.json`](config.json) and run:
```
node --max-old-used-space=12288 index.js
```

### Running the Analysis:

Once the dowloading, extraction and convesion to json is complete, run:

```
cd Scripts
python3 main_.py %%NAME_OF_STACKEXCHANGE_TO_RUN_ANALYSIS_ON%%
```

For example:
```
cd Scripts
python3 main_.py crypto.stackexchange.com
```