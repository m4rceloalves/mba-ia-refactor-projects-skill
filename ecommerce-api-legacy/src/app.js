const express = require('express');
const { config } = require('./config/settings');
const { initializeDatabase } = require('./database/database');
const { registerRoutes } = require('./views/routes');
const { errorHandler, notFoundHandler } = require('./middlewares/errorHandler');

function createApp() {
  const app = express();
  app.use(express.json());
  registerRoutes(app);
  app.use(notFoundHandler);
  app.use(errorHandler);
  return app;
}

async function start() {
  await initializeDatabase();
  const app = createApp();
  app.listen(config.port, () => {
    console.log(`Frankenstein LMS rodando na porta ${config.port}...`);
  });
}

if (require.main === module) {
  start().catch((error) => {
    console.error('Erro ao iniciar aplicação', error);
    process.exit(1);
  });
}

module.exports = { createApp, start };
