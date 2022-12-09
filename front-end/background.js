// Fetches website URL and responds accordingly
// ALSO in manifest.json, make sure 'tabs' is added to permissions
/*
chrome.tabs.query({
    active: true,
    currentWindow: true
}, function(tabs) {
    var tabURL = tabs[0].url;
    console.log(tabURL);
chrome.tabs.onUpdated.addListener(async function () {
        let url = await getTab()
        console.log(url)
    })
});

*/
async function getTab() {
    let queryOptions = { active: true, currentWindow: true };
    let tabs = await chrome.tabs.query(queryOptions);
    return [tabs[0].url, tabs[0].status];
  }

chrome.tabs.onUpdated.addListener(function () {
    getTab().then(ret => {
        var url = new URL(ret[0]);
        var stat = ret[1];
        if (stat == "complete") {
            var domainname = url.hostname;
            var data = {};
            data.domainname = domainname;
            console.log(data.domainname);
            fetch('http://127.0.0.1:8000/DDS_Server/domainname_check', {
                method: 'POST', // or 'PUT'
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
              })
                .then((response) => response.json())
                .then((data) => {
                  console.log(data.msg);
                  if (data.msg == "true") {
                    chrome.notifications.create(
                        {
                            type: "basic",
                            iconUrl: "images/1392.png",
                            title: "Notification",
                            message: "omg its john cena!",
                            silent: false
                        });
                  }
                })
                .catch((error) => {
                  console.error('Error:', error);
            });
        }
    })
})

