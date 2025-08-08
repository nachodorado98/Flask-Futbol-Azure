(function () {
  const url = new URL(window.location.href);
  if (url.searchParams.get("login") === "True") {
    url.searchParams.delete("login");
    const nuevaURL = url.pathname + url.search;
    window.history.replaceState({}, document.title, nuevaURL);
  }
})();