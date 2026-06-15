const { run } = require('../database/database');

function recordAudit(action) {
  return run('INSERT INTO audit_logs (action, created_at) VALUES (?, datetime(\'now\'))', [action]);
}

module.exports = { recordAudit };
