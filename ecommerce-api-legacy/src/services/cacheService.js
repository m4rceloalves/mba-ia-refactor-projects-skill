const checkoutCache = new Map();

function logAndCache(key, data) {
  console.log(`[LOG] Salvando no cache: ${key}`);
  checkoutCache.set(key, data);
}

module.exports = { logAndCache };
