const fs = require('fs');

let roomPath = 'Models/GameRoom.cs';
let roomContent = fs.readFileSync(roomPath, 'utf8');
roomContent = roomContent.replace(/El Bot T.xico/g, 'El Bot Tóxico');
// Remove any weird character in the emoji spot
roomContent = roomContent.replace(/AddBot\("El Bot Tóxico", ".*?"\)/g, 'AddBot("El Bot Tóxico", "🤖")');
fs.writeFileSync(roomPath, roomContent, 'utf8');

let indexPath = 'Views/Home/Index.cshtml';
let indexContent = fs.readFileSync(indexPath, 'utf8');
indexContent = indexContent.replace(/El Bot T.xico/g, 'El Bot Tóxico');
indexContent = indexContent.replace(/pendejo .*?\)/g, 'pendejo 🤖)');
fs.writeFileSync(indexPath, indexContent, 'utf8');

console.log('Fixed GameRoom.cs and Index.cshtml');
