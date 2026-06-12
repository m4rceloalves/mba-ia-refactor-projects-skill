const { get, run } = require('../database/database');
const { hashPassword } = require('../services/cryptoService');

async function findByEmail(email) {
  return get('SELECT id, name, email, pass FROM users WHERE email = ?', [email]);
}

async function createUser({ name, email, password }) {
  const result = await run('INSERT INTO users (name, email, pass) VALUES (?, ?, ?)', [
    name,
    email,
    hashPassword(password),
  ]);
  return result.lastID;
}

async function deleteUserWithRelations(userId) {
  await run('BEGIN TRANSACTION');
  try {
    await run('DELETE FROM payments WHERE enrollment_id IN (SELECT id FROM enrollments WHERE user_id = ?)', [userId]);
    await run('DELETE FROM enrollments WHERE user_id = ?', [userId]);
    const result = await run('DELETE FROM users WHERE id = ?', [userId]);
    await run('COMMIT');
    return result.changes;
  } catch (error) {
    await run('ROLLBACK');
    throw error;
  }
}

module.exports = { createUser, deleteUserWithRelations, findByEmail };
