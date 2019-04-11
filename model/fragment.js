//scheme for each documentation fragment

//"title" = String

//"text" = String

//"codeFragment" = String

//"language" = String
var mongoose = require('mongoose');


var fragmentSchema = new mongoose.Schema({
    
    title: {
        type: String,
        required: true
    },
    text: {
        type: String,
        required: true
    },
    codeFragment: {
        type: String,
        default: "unidentified"
    },
    language: {
        type: String,
        required: true
    }
})


module.exports = mongoose.model('Fragment', fragmentSchema);
