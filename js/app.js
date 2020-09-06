function eval_template(tmpl, dataitem) {
    // this is a pseudo generic templating engine implemented with minimal code 
    // it gets parameterized props from the template and replaces with the values
    // from the json by looking for the same prop name 
    // e.g. <div>${name}</div> gets converted to <div>dataitem["name"]</div> => <div>SomeName</div>
    var regExp = /\$\{(\w+)\}/g;
    var matches = [];
    var match = regExp.exec(tmpl);
    while (match != null) {
        matches.push(match[1]);
        match = regExp.exec(tmpl);
    }
    // now eval template
    for (var j = 0; j < matches.length; j++) {
        tmpl = tmpl.replace("${" + matches[j] + "}", dataitem[matches[j]]);
    }
    return tmpl;
}

window.onload = function() {
    // first fetch stores data from our server endpoint 
    // for simplicity we will use same origin to avoid dealing with CORS
    // in a prod. env (and not only, in any bigger app)  this will most certainly 
    // run at on different hosts or least on different ports
    var req = new XMLHttpRequest();
    req.open("GET", "/data/stores", true);
    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == "200") {
            var storesData = JSON.parse(req.responseText);
            // sort alphabetically by Store "name"
            storesData.sort(function(a, b) {
                a = a.name.toLowerCase();
                b = b.name.toLowerCase();
                return (a < b) ? -1 : (a > b) ? 1 : 0;
            });
            var storeTmpl = document.getElementById("storetemplate").innerHTML;
            var storeHtml = "";
            for (var i = 0; i < storesData.length; i++) {
                if (!storesData[i].latitude || !storesData[i].longitude) {
                    storesData[i].latitude = "Not found";
                    storesData[i].longitude = "Not found"; // e.g. Bagshot GU19 5DG
                }
                var boundItem = eval_template(storeTmpl, storesData[i]);
                storeHtml += boundItem;
            }
            document.getElementById("storeslist").innerHTML = storeHtml;
        }
    };
    req.send(); 
}