# Data Mining Project Report: Group 26

## Stack-Exchange Miner

The project aims to analyse data and study interesting insights of various [stackexchange forums](https://stackexchange.com/), ranging from christianity to cryptocurrency, using their data dumps. Since the schema for various stackexchange data dumps is similar, the goal is to develop generic data analysis irrespective of the specific data we examine.

Group Members:
|    | Member Name                                        | Roll Number | Email Id            |
|----|----------------------------------------------------|-------------|---------------------|
| 1. | [Aaryan Srivastava](https://github.com/aaryans941) | 180007      | aaryans@iitk.ac.in  |
| 2. | [Ashwin Shenai](https://github.com/ashwin2802)     | 180156      | ashwins@iitk.ac.in  |
| 3. | [Utkarsh Gupta](https://github.com/utkarshg99)     | 180836      | utkarshg@iitk.ac.in |
| 4. | [Varun Goyal](https://github.com/govarun)          | 180850      | govarun@iitk.ac.in  |

## Project Structure 
\
📦[StackExchange-Miner](.) \
 ┣ 📂[Scraping](Scraping/) \
 ┃ ┣ 📜[main.tsv](Scraping/main.tsv) \
 ┃ ┣ 📜[xmls-v.csv](Scraping/xmls-v.csv) \
 ┃ ┣ 📜[xmls.csv](Scraping/xmls.csv) \
 ┃ ┗ 📜[xmls.json](Scraping/xmls.json) \
 ┣ 📂[Scripts](Scripts/) \
 ┃ ┣ 📜[active_users.py](Scripts/active_users.py) \
 ┃ ┣ 📜[association_rule.py](Scripts/association_rule.py) \
 ┃ ┣ 📜[badges.py](Scripts/badges.py) \
 ┃ ┣ 📜[comments.py](Scripts/comments.py) \
 ┃ ┣ 📜[main.py](Scripts/main.py) \
 ┃ ┣ 📜[main_.py](Scripts/main_.py) \
 ┃ ┣ 📜[map_reduce.py](Scripts/map_reduce.py) \
 ┃ ┣ 📜[posthist.py](Scripts/posthist.py) \
 ┃ ┣ 📜[postlinks.py](Scripts/postlinks.py) \
 ┃ ┣ 📜[posts.py](Scripts/posts.py) \
 ┃ ┣ 📜[question_time.py](Scripts/question_time.py) \
 ┃ ┣ 📜[tags.py](Scripts/tags.py) \
 ┃ ┣ 📜[tag_pred.ipynb](Scripts/tag_pred.ipynb) \
 ┃ ┣ 📜[tag_pred.pkl](Scripts/tag_pred.pkl) \
 ┃ ┣ 📜[tag_prediction.py](Scripts/tag_prediction.py) \
 ┃ ┣ 📜[users.py](Scripts/users.py) \
 ┃ ┣ 📜[utils.py](Scripts/utils.py) \
 ┃ ┣ 📜[votes.py](Scripts/votes.py) \
 ┃ ┣ 📜[voting_reputation.py](Scripts/voting_reputation.py) \
 ┃ ┗ 📜[word_cloud.py](Scripts/word_cloud.py) \
 ┣ 📜[.gitignore](.gitignore) \
 ┣ 📜[index.js](index.js) \
 ┣ 📜[package.json](package.json) \
 ┣ 📜[README.md](README.md) \
 ┣ 📜[requirements.txt](requirements.txt) \
 ┣ 📜[schema.md](schema.md) \
 ┣ 📜[sites.xml](sites.xml) \
 ┗ 📜[start.sh](start.sh)

## Running the Project

## mm

## Data Description
* The data is downloaded using the following [link](https://archive.org/download/stackexchange/).
* Data format: 7zipped
* Schema can be found [here](schema.md) and is also publicly available [here](https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede). 

## Data Mining
- We have automated the entire process (downloading, extracting and pre-processing) via JavaScript, the code is present in the file `index.js`
- We first verify if all the files required for analysis are available for the given stackexchange. If they are available, we download all the 8 required files, namely, `Badges.xml, Comments.xml, PostHistory.xml, PostLinks.xml, Posts.xml, Tags.xml, Users.xml` in form of a .7z archive.
- This archive was then unzipped.
- We then process the extracted files, as follows. 

### Challenges encountered and handled:
- The data source for scraping had some inconsistencies. 
    - For example, some catalogue files were not listed, whereas they were actually available for scraping. 
- To ensure no loss of data, we check all the files by calling API requests separately for all the files. We took note of all the metadata for the file then. 
- Now, the developer could easily choose which database to work on, by looking at the meta data of the database. 

## Data Preprocessing
- The data was available in `.xml` format. We converted the data to `.json` to make it more intuitive. 
- Also for advanced analysis, `json` files are supported by many python libraries. 

## Results and Inferences

## Methodology 

## Description of Insights
