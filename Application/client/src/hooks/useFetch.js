import cookies from "js-cookie"

export function useFetch() { 
    async function makeRequest(
        uri,
        method = 'GET',
        body = 'null',
        headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": cookies.get("csrftoken"),
            "Accepct": "applicaiton/json",
        }
    ) {
        const options = {
            method,
            credentials: "same-origin",
            headers,
        }

        if (body) { 
            options.body = JSON.stringify(body || {});
        }

        const response = await fetch(uri, options);

        //Hanlde parsing or errors or both here

        return response;
    }

    return makeRequest
}