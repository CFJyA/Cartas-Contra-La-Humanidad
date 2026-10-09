const fs = require('fs');

const playerPath = 'Models/Player.cs';
const managerPath = 'Services/GameManager.cs';

// Read files assuming latin1 to safely get their bytes if they were messed up
// Actually, since I restored them with git, let's just read them as utf-8, they will have '' for invalid characters
// Better yet, let's read as binary and replace.

let playerContent = fs.readFileSync(playerPath, 'latin1');
playerContent = playerContent.replace(/public string Avatar \{ get; set; \} = ".*?";/, 'public string Avatar { get; set; } = "😎";');
fs.writeFileSync(playerPath, playerContent, 'utf8');

let managerContent = fs.readFileSync(managerPath, 'latin1');
managerContent = managerContent.replace(/string\[\] botAvatars = \[.*?\];/, 'string[] botAvatars = ["🤖", "👽", "👾", "🤡", "👻", "💀"];');
managerContent = managerContent.replace(/"El Bot T.*?xico"/, '"El Bot Tóxico"');
managerContent = managerContent.replace(/"T.*?a Pikachu"/, '"Tía Pikachu"');
managerContent = managerContent.replace(/Avatar = string\.IsNullOrWhiteSpace\(avatar\) \? ".*?" : avatar,/, 'Avatar = string.IsNullOrWhiteSpace(avatar) ? "😎" : avatar,');

fs.writeFileSync(managerPath, managerContent, 'utf8');
console.log('Done');
