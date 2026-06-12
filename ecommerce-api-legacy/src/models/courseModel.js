const { all, get } = require('../database/database');

function findActiveById(courseId) {
  return get('SELECT id, title, price, active FROM courses WHERE id = ? AND active = 1', [courseId]);
}

function listCourses() {
  return all('SELECT id, title, price, active FROM courses ORDER BY id');
}

module.exports = { findActiveById, listCourses };
