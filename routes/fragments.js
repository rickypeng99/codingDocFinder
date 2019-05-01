var secrets = require('../config/secrets');
var Fragment = require('../model/fragment')
var Retrieval = require('retrieval')
var replaced = ((original, change) => {
    if(change == undefined){
        return original;
    } else{
        return change;
    }
})

var checkInvalid = ((query) => {
    return (query == undefined || query == "");
})

module.exports = function (router) {

    var fragmentsRoute = router.route('/fragments');

    //GET request
    fragmentsRoute.get((req, res) =>{
        //check able to GET request, requires query and choice of language
        if(checkInvalid(req.query.query) || checkInvalid(req.query.language)){
            res.status(404).send({data: "error", message: "Invalid search, please input a query"})

        } else{
            
            var query = req.query.query;
            var language = req.query.language;

            //
            if(query == "all" && language == "all") {
                //returning all fragments
                Fragment.find()
                .exec()
                .then((fragments) => {
                    res.status(200).send({data: fragments, message: "Successfully returned all " + language + " fragments!"})

                })
                .catch((error) => {
                    res.status(500).send({data: "error", message: "Error: getting fragments corresponding to language (all) " + error})
                })
                
            } else if(query == "all" && language != "all"){
                //returning all fragments of a specific programming language
                Fragment.find({"language" : language})
                .exec()
                .then((fragments) => {
                    res.status(200).send({data: fragments, message: "Successfully returned all " + language + " fragments!"})

                })
                .catch((error) => {
                    res.status(500).send({data: "error", message: "Error: getting fragments corresponding to language (all) " + error})
                })
            } else {
                //returning a fragment array of which the texts are like the query
                Fragment.find({"language" : language})
                .exec()
                .then((fragments) => {
                    // //begin text retrieval (initilizing ranker)
                    // //making the texts as inverted indexes
                    // let ranker = new Retrieval(K=1.6, B=0.75);
                    // ranker.index(fragments.map((element) => {
                    //     return element.text;
                    // }));

                    // //ranking documents by texts
                    // let searchResults = ranker.search(req.query.query);
                    
                    // //returning the ranked fragments
                    // var results = [];
                    // for(text in searchResults){
                    //     for(element in fragments){
                    //         if(fragments[element].text == searchResults[text]){
                    //             results.push(fragments[element]);
                    //             break;
                    //         }
                    //     }
                    // }

                    // Load wink-bm25-text-search
                    var bm25 = require( 'wink-bm25-text-search' );
                    // Create search engine's instance
                    var engine = bm25();
                    // Load NLP utilities
                    var nlp = require( 'wink-nlp-utils' );
                    // Load sample data (load any other JSON data instead of sample)
                    var docs = fragments;

                    // Define preparatory task pipe!
                    var pipe = [
                        nlp.string.lowerCase,
                        nlp.string.tokenize0,
                        nlp.tokens.stem,
                        nlp.tokens.propagateNegations
                    ];
                    // Contains search query.
                    // Step I: Define config
                    engine.defineConfig( { fldWeights: { title: 1.5, text: 1 } } );
                    // Step II: Define PrepTasks pipe.
                    engine.definePrepTasks( pipe );

                    // Step III: Add Docs
                    
                    docs.forEach( function ( doc, i ) {
                        engine.addDoc( doc, i );
                    } );

                    // Step IV: Consolidate
                    engine.consolidate();
                    var resultIndex = engine.search( query, 40 );
                    // console.log( '%d entries found.', resultIndex.length );
                    // console.log( docs[ resultIndex[ 0 ][ 0 ] ].text );


                    results = [];
                    for(let i = 0; i < resultIndex.length; i++){
                        results.push(docs[resultIndex[i][0]]);
                    }

                    res.status(200).send({data: results, message: "Successfully returned " + results.length + " entries of " + language + " fragments with a query of " + query})
                })
                .catch((error) => {
                    res.status(500).send({data: "error", message: "Error: getting fragments corresponding to language and query " + error})
                })
            }

            


        }
    });

    //POST request
    //"title" = String
    //"text" = String
    //"codeFragment" = String
    //"language" = String
    fragmentsRoute.post((req, res) => {
        
        var fragment = new Fragment();
        fragment.title = replaced(fragment.title, req.body.title);
        fragment.text = replaced(fragment.text, req.body.text);
        fragment.codeFragment = replaced(fragment.codeFragment, req.body.codeFragment);
        fragment.language = replaced(fragment.language, req.body.language);

        fragment.save()
        .then(() => {
            res.status(200).send({data: fragment, message: "Successfully created a document fragment!"});
        })
        .catch((error) => {
            res.status(500).send({data: "error", message: "Error: creating a new doc fragment " + error});
        })

    });



    return router;
}
