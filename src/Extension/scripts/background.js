// chrome.webRequest.onCompleted.addListener(
//     function(details)
//     {
//         console.log("potato");
//         console.log(details.requestBody);
//     },
//     {urls: ["https://grade.daconline.unicamp.br/ajax/planejador.php"]},
//     // {urls: ["<all_urls>"]},
//     ['requestBody', 'extraHeaders']
// );

// chrome.webRequest.onCompleted.addListener(
//     function(details) {
//         console.log("potato");
//         console.log(details.responseHeaders);

//         // Extract necessary information from the details object
//         const requestHeaders = details.requestHeaders;
//         const url = details.url;
//         const method = details.method;
//         const initiator = details.initiator;

//         // Re-make the request to get the response body
//         fetch(url, {
//             method: method,
//             headers: requestHeaders
//         })
//         .then(response => response.text())
//         .then(body => {
//             console.log("Response body:", body);
//             // Do whatever you need to do with the response body here
//         })
//         .catch(error => {
//             console.error("Error fetching response body:", error);
//         });
//     },
//     {
//         urls: ["https://grade.daconline.unicamp.br/ajax/planejador.php"]
//     },
//     ['responseHeaders']
// );

// chrome.webRequest.onCompleted.addListener(
//     function(details) {
//         console.log("potato");
//         console.log(details.responseHeaders);

//         // Extract necessary information from the details object
//         const initiator = details.initiator;

//         // Check if the request is initiated by the extension
//         if (initiator && initiator.startsWith("chrome-extension://")) {
//             console.log("Request initiated by the extension. Skipping...");
//             return;
//         }

//         // Extract other necessary information
//         const requestHeaders = details.requestHeaders;
//         const url = details.url;
//         const method = details.method;

//         // Re-make the request to get the response body
//         fetch(url, {
//             method: method,
//             headers: requestHeaders
//         })
//         .then(response => response.text())
//         .then(body => {
//             console.log("Response body:", body);
//             // Do whatever you need to do with the response body here
//         })
//         .catch(error => {
//             console.error("Error fetching response body:", error);
//         });
//     },
//     {
//         urls: ["https://grade.daconline.unicamp.br/ajax/planejador.php"]
//     },
//     ['responseHeaders']
// );

// chrome.webRequest.onCompleted.addListener(
//     function(details) {
//         console.log("potato");
//         console.log(details.responseHeaders);

//         const initiator = details.initiator;
//         // Check if the request is initiated by the extension
//         if (initiator && initiator.startsWith("chrome-extension://")) {
//             console.log("Request initiated by the extension. Skipping...");
//             return;
//         }
//         // Extract necessary information from the details object
//         const requestHeaders = details.requestHeaders;
//         const url = details.url;
//         const method = details.method;

//         // Re-make the request to get the response body
//         fetch(url, {
//             method: method,
//             headers: requestHeaders
//         })
//         .then(response => {
//             const contentType = response.headers.get('content-type');
//             if (contentType && contentType.includes('application/json')) {
//                 return response.json(); // If the response is JSON
//             } else {
//                 return response.text(); // Otherwise, assume it's text
//             }
//         })
//         .then(body => {
//             console.log("Response body:", body);
//             // Do whatever you need to do with the response body here
//         })
//         .catch(error => {
//             console.error("Error fetching response body:", error);
//         });
//     },
//     {
//         urls: ["https://grade.daconline.unicamp.br/ajax/planejador.php"]
//     },
//     ['responseHeaders']
// );

chrome.webRequest.onBeforeSendHeaders.addListener(
    function(details) {
        console.log("potato");
        console.log(details.requestBody);

        const initiator = details.initiator;
        // Check if the request is initiated by the extension
        if (initiator && initiator.startsWith("chrome-extension://")) {
            console.log("Request initiated by the extension. Skipping...");
            return;
        }
        // Extract necessary information from the details object
        const requestHeaders = {};
        for (const header of details.requestHeaders) {
            requestHeaders[header.name] = header.value;
        }

        requestHeaders['Origin'] = 'https://grade.daconline.unicamp.br';
        requestHeaders['Referer'] = 'https://grade.daconline.unicamp.br/planejador/';
        requestHeaders['Sec-Fetch-Site'] = 'same-origin';
        const url = details.url;
        const method = details.method;

        console.log(requestHeaders);
        console.log(url);
        console.log(method);

        fetch(url, {
            method: method,
            mode: 'cors',
            headers: requestHeaders
        })
        .then(response => {console.log(response)});
    },
    {urls: ["https://grade.daconline.unicamp.br/ajax/planejador.php"]},
    ['requestHeaders', 'extraHeaders']
);
