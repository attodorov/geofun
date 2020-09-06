GET_STORES_URL = "/api/stores";
SEARCH_URL = "/api/searchstores";
ITEMS_PER_PAGE = 3

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

function search() {
    clearInterval(window.timerid);
    window.timerid = setTimeout(searchfunc, 100);    
}

function searchfunc() {
    var q = document.getElementById("search").value;
    // if it's 0 we want to reload the list because we are basically backspacing
    if (q.length == 1)
        return;
    if (window.q != q) {
        window.q = q;
    }
    // reset items container scroll
    document.getElementById("container").scrollTop = 0;
    // search stores
    loadstores(q, ITEMS_PER_PAGE);
}

function lazyLoadItems(e) {
    if (e.target.scrollTop >= (e.target.scrollHeight - e.target.offsetHeight)) {
        if (!window.q || window.q == "") {
            return;
        }
        if (window.currentPage*ITEMS_PER_PAGE > window.storesData.length) {
            return;
        }
        // append more items in the list
        var storeTmpl = document.getElementById("storetemplate").innerHTML;
        for (i = 0; i < ITEMS_PER_PAGE; i++) {
            var index = window.currentPage * ITEMS_PER_PAGE + i;
            if (window.storesData.length > index) {
                var boundItem = eval_template(storeTmpl, window.storesData[index]);
                document.getElementById("storeslist").insertAdjacentHTML( 'beforeend', boundItem);
            }
        }
        // bump page
        window.currentPage++;
    }
}

window.onload = function() {
    loadstores(window.q, 0);
    document.getElementById("container").onscroll = lazyLoadItems;
}

function loadstores(query, renderlimit) {
    window.currentPage = 1;
    // first fetch stores data from our server endpoint 
    // for simplicity we will use same origin to avoid dealing with CORS
    // in a prod. env (and not only, in any bigger app)  this will most certainly 
    // run at on different hosts or least on different ports
    var req = new XMLHttpRequest();
    // we can always use just the same endpoint , that is /api/searchstores with an empty search q
    // but i was doing this incrementally
    var url = GET_STORES_URL;
    if (query && query.trim() != "") {
        url = SEARCH_URL + "?query=" + query;
    }
    req.open("GET", url, true);
    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == "200") {
            window.storesData = JSON.parse(req.responseText);
            // sort alphabetically by Store "name"
            window.storesData.sort(function(a, b) {
                a = a.name.toLowerCase();
                b = b.name.toLowerCase();
                return (a < b) ? -1 : (a > b) ? 1 : 0;
            });
            var storeTmpl = document.getElementById("storetemplate").innerHTML;
            var storeHtml = "";
            // load all on initial load
            if (document.getElementById("search").value == "") {
                renderlimit = 0; // load all. e.g. user is backspacing
            }
            if (renderlimit == 0 || renderlimit > window.storesData.length) {
                renderlimit = window.storesData.length;
            }
            for (var i = 0; i < renderlimit; i++) {
                if (!window.storesData[i].latitude || !window.storesData[i].longitude) {
                    window.storesData[i].latitude = "Not found";
                    window.storesData[i].longitude = "Not found"; // e.g. Bagshot GU19 5DG
                }
                var boundItem = eval_template(storeTmpl, window.storesData[i]);
                storeHtml += boundItem;
            }
            document.getElementById("storeslist").innerHTML = storeHtml;
        }
    };
    req.send(); 
}