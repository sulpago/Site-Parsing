function postDownload(loading_progress, basepath, categorypath) {
    console.log("postDownload");
    var formData = new FormData();
    formData.append("basepath", basepath.value);
    formData.append("categoryname", categorypath.value);
    var myRequest = new XMLHttpRequest();
    myRequest.onreadystatechange = function (aEvt) {
        if (myRequest.readyState == 4 && myRequest.status == 200) {
            layoutView(loading_progress, "none");
        }
    }
    layoutView(loading_progress, "block");
    myRequest.open('POST', '/joosohn/image/download', true);
    myRequest.send(formData);

}

function postKeyword(targe_url, loading_progress, result_view, category, keyword, page) {
    console.log("postKeyword");
    var formData = new FormData();
    formData.append("category", category.value);
    formData.append("keyword", keyword.value);
    formData.append("page", page.value);

    var myRequest = new XMLHttpRequest();
    myRequest.onreadystatechange = function (aEvt) {
        if (myRequest.readyState == 4 && myRequest.status == 200) {
            var getResults = this.responseText;
            layoutView(loading_progress, "none");
            remove_quota = getResults.slice(1, -2);
            result_view.innerHTML = remove_quota;
        }
        // layoutView(loading_progress, "none");

    };
    layoutView(loading_progress, "block");
    clearView(result_view);
    myRequest.open('POST', targe_url, true);
    myRequest.send(formData);

}

function clearView(target_view) {
    target_view.innerHTML = ";"
}

function removeImage(target_img) {
    // console.log(target_img.alt);
    target_opacity = target_img.style.opacity;
    if (target_opacity > 0.5) {
        // console.log("Remove");
        target_img.style.opacity = 0.1;
        itemlistControl('/joosohn/image/list', target_img.alt, "DELETE")
    } else {
        // console.log("Add");
        target_img.style.opacity = 1;
        itemlistControl('/joosohn/image/list', target_img.alt, "PUT")
    }
}

function itemlistControl(targe_url, goodscode, actioncode) {
    // console.log("itemlistControl");
    var formData = new FormData();
    formData.append("goodscode", goodscode);
    var myRequest = new XMLHttpRequest();
    myRequest.onreadystatechange = function (aEvt) {

    };
    myRequest.open(actioncode, targe_url, true);
    myRequest.send(formData);
}

function layoutView(target_view, display_action) {
    target_view.style.display = display_action;

}