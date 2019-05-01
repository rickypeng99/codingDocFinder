# 410 final - Coding doc finder
## Intro
This is the backend implementation of the coding doc finder, which is programmed by node.js(express + mongoose)   
The data are scrapted from the open-source documents and saved on MongoDB  
The text retrieval functionality is realized by the wink-bm25-text-search package on npm  
## Usage
Find 
Run the following command at the root directory of this project: 
```unix 
npm start
```
## Usage of handling databases
Run the following command at the database_assets directory  
Upload:
```unix 
python addFragments.py [languageName]
```
Clear the database:
```unix 
python deleteFragments.py [languageName]
```


