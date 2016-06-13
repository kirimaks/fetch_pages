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

function group_search(pattern) {
    var my_url = "/group_search/" + pattern;
    console.log(my_url);
    write_tags(my_url, "#tag-cloud");
}

function org_search(name) {
    var my_url = "/org_search/" + name;
    console.log("Request to: " + my_url);
    write_tags(my_url, "#tag-cloud");
}

