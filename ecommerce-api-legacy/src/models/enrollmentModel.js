const { run } = require('../database/database');

async function createEnrollment(userId, courseId) {
  const result = await run('INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)', [userId, courseId]);
  return result.lastID;
}

module.exports = { createEnrollment };
