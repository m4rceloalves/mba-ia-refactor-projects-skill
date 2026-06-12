const sqlite3 = require('sqlite3').verbose();
const { hashPassword } = require('../services/cryptoService');

const db = new sqlite3.Database(':memory:');

function run(sql, params = []) {
  return new Promise((resolve, reject) => {
    db.run(sql, params, function onRun(error) {
      if (error) reject(error);
      else resolve({ lastID: this.lastID, changes: this.changes });
    });
  });
}

function get(sql, params = []) {
  return new Promise((resolve, reject) => {
    db.get(sql, params, (error, row) => {
      if (error) reject(error);
      else resolve(row);
    });
  });
}

function all(sql, params = []) {
  return new Promise((resolve, reject) => {
    db.all(sql, params, (error, rows) => {
      if (error) reject(error);
      else resolve(rows);
    });
  });
}

async function initializeDatabase() {
  await run('PRAGMA foreign_keys = ON');
  await run('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, pass TEXT NOT NULL)');
  await run('CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, price REAL NOT NULL, active INTEGER NOT NULL)');
  await run('CREATE TABLE IF NOT EXISTS enrollments (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, course_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE, FOREIGN KEY(course_id) REFERENCES courses(id))');
  await run('CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY AUTOINCREMENT, enrollment_id INTEGER NOT NULL, amount REAL NOT NULL, status TEXT NOT NULL, FOREIGN KEY(enrollment_id) REFERENCES enrollments(id) ON DELETE CASCADE)');
  await run('CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT NOT NULL, created_at DATETIME NOT NULL)');

  const existing = await get('SELECT COUNT(*) AS total FROM users');
  if (existing.total > 0) return;

  await run('INSERT INTO users (name, email, pass) VALUES (?, ?, ?)', ['Leonan', 'leonan@fullcycle.com.br', hashPassword('123')]);
  await run('INSERT INTO courses (title, price, active) VALUES (?, ?, ?)', ['Clean Architecture', 997.00, 1]);
  await run('INSERT INTO courses (title, price, active) VALUES (?, ?, ?)', ['Docker', 497.00, 1]);
  const enrollment = await run('INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)', [1, 1]);
  await run('INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)', [enrollment.lastID, 997.00, 'PAID']);
}

module.exports = { all, db, get, initializeDatabase, run };
