const checkoutController = require('../controllers/checkoutController');
const reportController = require('../controllers/reportController');
const userController = require('../controllers/userController');
const { asyncHandler } = require('../middlewares/errorHandler');

function registerRoutes(app) {
  app.post('/api/checkout', asyncHandler(checkoutController.checkout));
  app.get('/api/admin/financial-report', asyncHandler(reportController.financialReport));
  app.delete('/api/users/:id', asyncHandler(userController.deleteUser));
}

module.exports = { registerRoutes };
