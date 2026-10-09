const fs = require('fs');

const roomPath = 'Models/GameRoom.cs';
const indexPath = 'Views/Home/Index.cshtml';

let roomContent = fs.readFileSync(roomPath, 'latin1');
roomContent = roomContent.replace(/"El Bot T.*?xico"/g, '"El Bot Tóxico"');
roomContent = roomContent.replace(/"Y-"/g, '"🤖"');
roomContent = roomContent.replace(/"ðŸ¤–"/g, '"🤖"');
// Let's just catch all variations
roomContent = roomContent.replace(/"Y-"/g, '"🤖"');
fs.writeFileSync(roomPath, roomContent, 'utf8');

let indexContent = fs.readFileSync(indexPath, 'latin1');
indexContent = indexContent.replace(/<em>El Bot T.*?xico<\/em>/g, '<em>El Bot Tóxico</em>');
indexContent = indexContent.replace(/pendejo Y-\)/g, 'pendejo 🤖)');
indexContent = indexContent.replace(/pendejo ðŸ¤–\)/g, 'pendejo 🤖)');
fs.writeFileSync(indexPath, indexContent, 'utf8');

console.log('Fixed GameRoom and Index');
