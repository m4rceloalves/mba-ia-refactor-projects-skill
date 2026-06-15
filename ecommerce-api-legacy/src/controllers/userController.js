const userModel = require('../models/userModel');
const { AppError } = require('../middlewares/errorHandler');

async function deleteUser(req, res) {
  const deleted = await userModel.deleteUserWithRelations(req.params.id);
  if (!deleted) {
    throw new AppError('Usuário não encontrado', 404);
  }
  res.json({ msg: 'Usuário deletado com matrículas e pagamentos relacionados' });
}

module.exports = { deleteUser };
