import { CSRF_TOKEN } from "./csrf_token.js";

function handleResponse(response) {
  if (response.status === 204) {
    return "";
  } else if (response.status === 404) {
    return null;
  } else {
    return response.json();
  }
}

async function apiService(endpoint, method, data) {
  const config = {
    method: method || "GET",
    body: data !== undefined ? JSON.stringify(data) : null,
    headers: {
      "content-type": "application/json",
      "X-CSRFTOKEN": CSRF_TOKEN
    }
  };
  return (
    fetch(endpoint, config)
      .then(handleResponse)
      // eslint-disable-next-line no-console
      .catch(error => console.log(error))
  );
}

export { apiService };
