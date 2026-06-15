const { config } = require('../config/settings');

function processPayment(cardNumber) {
  if (!cardNumber) {
    return { status: 'DENIED' };
  }
  const status = cardNumber.startsWith('4') ? 'PAID' : 'DENIED';
  console.log(`Processando pagamento com cartão ${maskCard(cardNumber)} usando gateway configurado`);
  return { gateway: config.paymentGatewayKey, status };
}

function maskCard(cardNumber) {
  return `****${String(cardNumber).slice(-4)}`;
}

module.exports = { processPayment };
