const { run } = require('../database/database');

function createPayment(enrollmentId, amount, status) {
  return run('INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)', [enrollmentId, amount, status]);
}

module.exports = { createPayment };
