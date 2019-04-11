var secrets = require('../config/secrets');
var Fragment = require('../model/fragment')

module.exports = function (router) {

    var fragmentsIdRoute = router.route('/fragments/:id');

    //GET request
    fragmentsIdRoute.get(function (req, res) {
        Fragment.findById(req.params.id)
        .exec()
        .then((fragment) => {
            if(fragment != null){
                res.status(200).send({data: fragment, message: "Fragment with specific id returned"})
            } else{
                res.status(404).send({data: "404", message: "Couldn't find fragment with specific id"})
            }
        })
        .catch((error) => {
            res.status(500).send({data: "500", message: "Error: findById: " + error})

        })
    });


    //DELETE request
    fragmentsIdRoute.delete(function (req, res) {
        Fragment.findByIdAndRemove(req.params.id)
        .exec()
        .then((fragment) => {
            if(fragment != null){
                res.status(200).send({data: fragment.title, message: "Fragment with specific id deleted"})
            } else{
                res.status(404).send({data: "404", message: "Couldn't find fragment with specific id, thus can't be deleted"})
            }
        })
        .catch((error) => {
            res.status(500).send({data: "500", message: "Error: findByIdAndRemove: " + error})

        })
    });
    return router;
}
