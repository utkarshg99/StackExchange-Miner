const fs = require("fs");
const cheerio = require("cheerio");
const axios = require("axios");
const convert = require('xml-js');
const Seven = require("node-7z");
const Downloader = require('nodejs-file-downloader');

const mainURL = "https://archive.org/download/stackexchange/";
const subBaseURL = "http://ia600107.us.archive.org/view_archive.php?archive=/27/items/stackexchange/";
const FILE_DOWNLOAD_PATH = "Data/";
const FILE_EXTRACT_PATH = "Data/Extracted/";
const SCRAPE_OUTPUT_PATH = "Scraping/";
const SCRAPE_CSV = "xmls.csv";
const VERIFY_CSV = "xmls-v.csv";
const SCRAPE_JSON = "xmls.json";
const SCRAPE_TSV = "main.tsv";
const FILES = ["Badges.xml", "Comments.xml", "PostHistory.xml", "PostLinks.xml", "Posts.xml", "Tags.xml", "Users.xml", "Votes.xml"];

function processMain(){
    let raw_txt = String(fs.readFileSync(SCRAPE_OUTPUT_PATH + SCRAPE_TSV));
    raw_txt = raw_txt.split("\n");
    let arr = [];
    let szs = [];
    for (let i = 0; i < raw_txt.length; i++) {
        ln = raw_txt[i].split("\t");
        sn = ln[0].trim().split(" ")[0];
        szs.push(ln[2].trim());
        arr.push(sn);
    }
    return {"array": arr, "sizes": szs};
}

async function scrapeAll() {
    let meta = processMain();
    let meta_indx = meta["array"];
    let sizes = meta["sizes"];
    let lines = ["StackExchange,Size,Number of XMLs"];
    let scrape = {}
    for (let i = 0; i < meta_indx.length; i++) {
        if (!meta_indx[i].length) continue;
        let resp = await axios.get(subBaseURL + meta_indx[i]);
        let $ = cheerio.load(resp.data);
        let table_ele = $("#maincontent").find('table');
        let data = {
            "caption": table_ele.find("caption").text(),
            "size": sizes[i],
            "xmls": []
        };
        let x_line = `${meta_indx[i]},${sizes[i]},${table_ele.find("a").length-1}`;
        table_ele.find("a").each((index, element) => {
            if($(element).text().length) {
                data.xmls.push({
                    "xml": $(element).text(),
                    "dwd": subBaseURL+meta_indx[i]+"/"+$(element).text()
                })
                x_line += ","+$(element).text();
            }
        });
        scrape[meta_indx[i]] = data;
        lines.push(x_line);
        if(lines.length % 10 == 0) fs.writeFileSync(SCRAPE_OUTPUT_PATH + VERIFY_CSV, lines.join("\n"));
    }
    fs.writeFileSync(SCRAPE_OUTPUT_PATH + VERIFY_CSV, lines.join("\n"));
    return scrape;
}

async function verifyAll() {
    let meta = processMain();
    let meta_indx = meta["array"];
    let sizes = meta["sizes"];
    let lines = ["StackExchange,Size,Number of XMLs"];
    for (let i = 0; i < meta_indx.length; i++) {
        let fpresent = [];
        if (!meta_indx[i].length) continue;
        let x_line = `${meta_indx[i]},${sizes[i]}`;
        for (let j = 0; j < FILES.length; j++) {
            try {
                let resp = await axios.head(mainURL + meta_indx[i] + "/" + FILES[j]);
                if (resp.status / 100 == 2) fpresent.push(FILES[j]);
            }
            catch(e) {console.log(meta_indx[i] + "/" + FILES[j]);}
        }
        x_line += ","+fpresent.length;
        for (let j = 0; j < fpresent.length; j++) x_line += ","+fpresent[j];
        lines.push(x_line);
        fs.writeFileSync(SCRAPE_OUTPUT_PATH + SCRAPE_CSV, lines.join("\n"));
    }
    fs.writeFileSync(SCRAPE_OUTPUT_PATH + SCRAPE_CSV, lines.join("\n"));
    return meta;
}

async function downloadFile(urls) {
    let fnames = [];
    for (let i = 0; i < urls.length; i++){
        let url = urls[i];
        let durl = mainURL + url;
        let fname = url;
        let downloader = new Downloader({
            url: durl,
            directory: FILE_DOWNLOAD_PATH,
            cloneFiles: false,
            maxAttempts: 3
        });
        await downloader.download();
        console.log(fname);
        fnames.push(fname);
    }
    return fnames;
}

async function unzipFiles(fnames) {
    for (let i = 0; i < fnames.length; i++) {
        let name = fnames[i]; 
        let out_f = FILE_EXTRACT_PATH + name.replace(".7z", "");
        if(!fs.existsSync(out_f)) fs.mkdirSync(out_f);
        let unz_prom = new Promise((resolve, reject) => {
            let unz_stream = Seven.extract(FILE_DOWNLOAD_PATH + name, out_f, {
                recursive: true,
                $cherryPick: '*.xml'
            });
            unz_stream.on('end', () => resolve());
            unz_stream.on('error', (error) => reject(error));
        });
        await unz_prom;
        console.log(out_f);
    }
}

async function findData() {
    // let _meta = await scrapeAll(); // Generates the xml record as indicated by the website
    let _meta = await verifyAll(); // Generates the xml record fround by crawling the website
    fs.writeFileSync(SCRAPE_OUTPUT_PATH + SCRAPE_JSON, JSON.stringify(_meta));
}

async function getData() {
    let urls = [
        // "ethereum.stackexchange.com.7z", 
        // "chinese.stackexchange.com.7z", 
        // "emacs.stackexchange.com.7z", 
        // "history.stackexchange.com.7z",
        // "datascience.stackexchange.com.7z",
        // "space.stackexchange.com.7z",
        // "crypto.stackexchange.com.7z",
        "islam.stackexchange.com.7z",
        // "hinduism.stackexchange.com.7z"
    ]; // The stackexchange sub-domains to download data from
    let fnames = await downloadFile(urls);
    await unzipFiles(fnames); // unzip the downloaded tars
    return urls;
}

async function convertJSON(dwd_dat){
    let rawdata, folder, res_json, res;
    for(let i=0; i<dwd_dat.length; i++){
        folder = FILE_EXTRACT_PATH+dwd_dat[i].substring(0, dwd_dat[i].length-3);
        for(let j=0; j<FILES.length; j++){
            rawdata = fs.readFileSync(folder+"/"+FILES[j]);
            res_json = JSON.parse(convert.xml2json(rawdata, {compact: true}));
            delete res_json["_declaration"];
            res = { "data": [] };
            for(let i=0; i<res_json[Object.keys(res_json)[0]]["row"].length; i++){
                res["data"].push(Object.assign({}, res_json[Object.keys(res_json)[0]]["row"][i]["_attributes"]));
            }
            fs.writeFileSync(folder+"/"+FILES[j].substring(0, FILES[j].length-3)+"json", JSON.stringify(res, null, "\t"));
        }
    }
}

async function main() {
    // await findData();
    let dwd_dat = await getData();
    await convertJSON(dwd_dat);
}

main();