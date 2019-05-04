var secrets = require('../config/secrets');
var Fragment = require('../model/fragment')

var replaced = ((original, change) => {
    if(change == undefined){
        return original;
    } else{
        return change;
    }
})

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
                res.status(404).send({data: "error", message: "Couldn't find fragment with specific id"})
            }
        })
        .catch((error) => {
            res.status(500).send({data: "error", message: "Error: findById: " + error})

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
                res.status(404).send({data: "error", message: "Couldn't find fragment with specific id, thus can't be deleted"})
            }
        })
        .catch((error) => {
            res.status(500).send({data: "error", message: "Error: findByIdAndRemove: " + error})

        })
    });

    //PUT request, only for adding the similar contexts
    fragmentsIdRoute.put((req, res) => {
        Fragment.findById(req.params.id)
        .exec()
        .then((fragment) => {
            fragment.similar = replaced(fragment.similar, req.body.similar);
            fragment.save()
            .then((response) => {
                res.status(200).send({data: response, message: "Fragments added similarity"})
            })
            .catch((error) => {
                res.status(404).send({data: "error", message: "Couldn't find fragment with specific id, thus can't be updated " + error})
            })
        })
        .catch(error => {
            res.status(500).send({data: "error", message: "Error: update findById: " + error})

        })

    })
    return router;
}
