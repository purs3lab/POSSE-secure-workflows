# Actionlint Script
## Run actionlint on every repository in the script's directory. 

### **Quick Start**
Clone this repository. 
```bash
git clone https://github.com/Chloe2330/repo-runner.git
``` 

Install `actionlint` [here](https://github.com/rhysd/actionlint) in the same directory. 

Clone the repositories to run actionlint on.

The following reposities were used to produce the output files in the sample results folder and the sample `output.json` file: 
```bash
git clone https://github.com/abrt/abrt.git
git clone https://github.com/argoproj/argo-cd.git
git clone https://github.com/vmware/govmomi.git
git clone https://github.com/AcademySoftwareFoundation/openexr.git
git clone https://github.com/aliasrobotics/RVD.git
git clone https://github.com/appneta/tcpreplay.git
git clone https://github.com/YetiForceCompany/YetiForceCRM.git
```

If actionlint does not detect any issues with the workflow configuration file, the ouput text file will be empty.

### **Usage**
`./script.py actionlint` runs actionlint on every repository\
`./script.py --json` consolidates all text files in the results directory in an `output.json ` file\
`./script.py --help` prints script usage\
`./script.py --clear` deletes all folders and output files in the results directory

### **Other Features**
`./read_csv.py [csv file name]` reads and downloads repositories from a csv file\
`./read_csv.py --help` prints script usage

### **Work in Progress**
- Fix issues with multiple arguments 

### **Additional Notes**
- `script.py` will run any command on every repository in its directory (i.e. `./script.py "git ls-remote --heads"`).
- `actionlint` is not compatible with workflows that do not use GitHub Actions (error: no project was found in any parent directories of ".").
- `read_csv.py` is only compatible with the csv format shown in `sample.csv`, modify the script based on the csv format that is being used 
