const auditLogModel = require('../models/auditLogModel');
const courseModel = require('../models/courseModel');
const enrollmentModel = require('../models/enrollmentModel');
const paymentModel = require('../models/paymentModel');
const userModel = require('../models/userModel');
const { AppError } = require('../middlewares/errorHandler');
const { logAndCache } = require('../services/cacheService');
const { processPayment } = require('../services/paymentService');

async function checkout(req, res) {
  const payload = normalizeCheckoutPayload(req.body);
  if (!payload.name || !payload.email || !payload.courseId || !payload.card) {
    throw new AppError('Bad Request', 400);
  }

  const course = await courseModel.findActiveById(payload.courseId);
  if (!course) {
    throw new AppError('Curso não encontrado', 404);
  }

  const userId = await findOrCreateUser(payload);
  const payment = processPayment(payload.card);
  if (payment.status === 'DENIED') {
    throw new AppError('Pagamento recusado', 400);
  }

  const enrollmentId = await enrollmentModel.createEnrollment(userId, payload.courseId);
  await paymentModel.createPayment(enrollmentId, course.price, payment.status);
  await auditLogModel.recordAudit(`Checkout curso ${payload.courseId} por ${userId}`);
  logAndCache(`last_checkout_${userId}`, course.title);

  res.status(200).json({ msg: 'Sucesso', enrollment_id: enrollmentId });
}

function normalizeCheckoutPayload(body) {
  return {
    name: body.usr || body.name,
    email: body.eml || body.email,
    password: body.pwd || body.password || '123456',
    courseId: body.c_id || body.course_id,
    card: body.card,
  };
}

async function findOrCreateUser(payload) {
  const existingUser = await userModel.findByEmail(payload.email);
  if (existingUser) {
    return existingUser.id;
  }
  return userModel.createUser({
    name: payload.name,
    email: payload.email,
    password: payload.password,
  });
}

module.exports = { checkout };
