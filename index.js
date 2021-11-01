const fs = require("fs");
const cheerio = require("cheerio");
const axios = require("axios");
const pretty = require("pretty");
const { data } = require("cheerio/lib/api/attributes");

const mainURL = "https://archive.org/download/stackexchange";
const subBaseURL = "http://ia600107.us.archive.org/view_archive.php?archive=/27/items/stackexchange/";

function processMain(){
    let raw_txt = String(fs.readFileSync("Scraping/main.tsv"));
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
        let x_line = `${meta_indx[i]},${sizes[i]},${table_ele.find("a").length}`;
        table_ele.find("a").each((index, element) => {
            if($(element).text().length) {
                data.xmls.push({
                    "xml": $(element).text(),
                    "dwd": subBaseURL+meta_indx[i]+"/"+$(element).text()
                })
                x_line += ","+$(element).text();
            }
        });
        lines.push(x_line);
        if(lines.length % 10 == 0) fs.writeFileSync("Scraping/xmls.csv", lines.join("\n"));
    }
    fs.writeFileSync("Scraping/xmls.csv", lines.join("\n"));
}

fs.writeFileSync("Scraping/xmls.json", JSON.stringify(scrapeAll()));