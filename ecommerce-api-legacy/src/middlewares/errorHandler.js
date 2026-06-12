class AppError extends Error {
  constructor(message, statusCode = 400) {
    super(message);
    this.statusCode = statusCode;
  }
}

function asyncHandler(handler) {
  return (req, res, next) => Promise.resolve(handler(req, res, next)).catch(next);
}

function notFoundHandler(req, res) {
  res.status(404).json({ error: 'Recurso não encontrado' });
}

function errorHandler(error, req, res, next) {
  const statusCode = error.statusCode || 500;
  const message = statusCode >= 500 ? 'Erro interno' : error.message;
  if (statusCode >= 500) {
    console.error(error);
  }
  res.status(statusCode).json({ error: message });
}

module.exports = { AppError, asyncHandler, errorHandler, notFoundHandler };
