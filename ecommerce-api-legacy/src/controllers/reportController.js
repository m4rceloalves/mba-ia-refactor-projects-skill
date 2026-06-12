const reportModel = require('../models/reportModel');

async function financialReport(req, res) {
  const report = await reportModel.financialReport();
  res.json(report);
}

module.exports = { financialReport };
