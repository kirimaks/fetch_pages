function write_tags(json_url, div_id) {
    $.getJSON(json_url, function(results) {
        var words = new Array();
        $.each(results, function(key, val) {
            words[key] = val;
        });

        if (words.length <= 0) {
            console.log("Empty data, clear tags and exit...");
            $(div_id).jQCloud('destroy');
            return;
        }
        console.log("Output length: " + words.length)

        if ($("#tag-cloud").html() == "") {
            console.log("add words");
            $(div_id).jQCloud(words);
        } else {
            console.log("update words");
            $(div_id).jQCloud('update', words);
        }
    });
}

function get_id_and_write_tags(name) {
    var my_url = "/get_id/" + name;
    console.log(my_url);

    $.ajax({
        url: my_url,
        success: function(resp) {
            console.log("ReturnedId: " + resp);

            if (resp >= 0) {
                // Make request.
                var search_url = "/search/" + resp;
                console.log("Request to: ", search_url);
                write_tags(search_url, "#tag-cloud");
            } else {
                // Clear tags.        
                console.log("Negative id recived, clear tags....");
                $("#tag-cloud").jQCloud('destroy');
            }
        },
    });
}

function search_org_and_write_tags(name) {
    var my_url = "/search_by_org/" + name;
    console.log("Request to: " + my_url);
    write_tags(my_url, "#tag-cloud");
}

