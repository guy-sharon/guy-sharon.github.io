self.addEventListener("fetch", (event) => {
  event.respondWith(
    (async () => {
      const cache = await caches.open(cacheName);

      try {
        // Try to fetch from network first
        const fetchResponse = await fetch(event.request);
        if (fetchResponse && fetchResponse.ok) {
          // Optionally cache the response
          await cache.put(event.request, fetchResponse.clone());
          return fetchResponse;
        }
      } catch (error) {
        console.log("Network fetch failed: ", error);
      }

      // Fallback to cache
      const cachedResponse = await cache.match(event.request);
      if (cachedResponse) {
        return cachedResponse;
      }

      // Fallback to index.html for navigation requests
      if (event.request.mode === "navigate") {
        return await cache.match("index.html");
      }

      return Response.error();
    })()
  );
});
