const fs = require('fs');

fs.mkdir('log', (err) => {
    if (err) { console.log(err) }
});
fs.writeFile('log/logger.log', '', function (err) {
    if (err) { throw err; }
});